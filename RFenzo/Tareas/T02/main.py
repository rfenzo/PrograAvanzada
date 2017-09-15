import math
import random

from Clases.Menu import Menu
from Clases.Pais import Pais

from Archivos import connections_generator
from Clases.Infeccion import Infeccion
from EstructurasDeDatos.DiccionarioOrdenado import DiccionarioOrdenado
from EstructurasDeDatos.MiLista import MiLista
from ManejoDeArchivos.custom_csv import csv_to_dict_of_dicts, airports_to_dict
from ManejoDeArchivos.custom_csv import borders_to_dict, mundo_to_csv
from ManejoDeArchivos.custom_csv import load_to_mundo

connections_generator.generate_connections()

menupartida = Menu("Iniciar partida nueva", "Cargar partida")
menupartida.display()
# mundo se cargará con informacion nueva o de una aprtida anterior, segun
# corresponda
mundo = DiccionarioOrdenado()


if menupartida == 1:
    dia = 0
    connections_generator.generate_connections()
    grafo_tierra = borders_to_dict()
    grafo_aire = airports_to_dict()
    pais_poblacion = csv_to_dict_of_dicts("population.csv")

    # se crean todos los paises con sus respectivos habitantes y fronteras.
    # (estado inicial)
    for pais, informacion in pais_poblacion:
        mundo.append(pais, Pais(nombre=pais, habitantes=int(informacion[
                     "Poblacion"]), frontera=grafo_tierra[pais],
            aeropuerto=grafo_aire[pais]))
    menupais = Menu()
    x = MiLista()
    i = 1
    for key, _ in pais_poblacion:
        x.append(menupais.append(str(i), key))
        i += 1

    nombre_pais_inicio = menupais.display()  # string
    pais_inicio = mundo[nombre_pais_inicio]  # pais
    menuinfeccion = Menu("Virus", "Bacteria", "Parásito")
    infeccion = menuinfeccion.display()  # string
    pais_inicio.inicio_infeccion(infeccion, dia)
    # ahora el mundo tiene todos los paises con condicion inicial y un pais
    # con la infeccion
    mundo[nombre_pais_inicio] = pais_inicio
    dia_descubrimiento_infeccion = None
    dia_descubrimiento_cura = None
    progreso_al_dia = 0
    poseedores_de_cura = MiLista()
    cola_propuestas = DiccionarioOrdenado()
else:
    a, b, c, d, e, f = load_to_mundo()
    mundo = a
    dia_descubrimiento_infeccion = b
    dia_descubrimiento_cura = c
    progreso_al_dia = d
    poseedores_de_cura = e
    cola_propuestas = f
    dia = mundo.get_by_position(0).dia_actual

poblacion_mundial_inicial = 0
infeccion = None
paises_infectados = MiLista()
for n_p, c_p in mundo:
    poblacion_mundial_inicial += int(c_p.habitantes)
    if c_p.estado == "infectado":
        paises_infectados.append(n_p)
        if not infeccion:
            infeccion = Infeccion(c_p.infeccion)

infectados_por_dia = DiccionarioOrdenado()
muertos_por_dia = DiccionarioOrdenado()
paises_infectados_por_dia = DiccionarioOrdenado()
aeropuertos_cerrados_por_dia = DiccionarioOrdenado()
fronteras_cerrados_por_dia = DiccionarioOrdenado()
tasa_vida_por_dia = DiccionarioOrdenado()
mascarillas_por_dia = DiccionarioOrdenado()

while True:
    print("Estamos en el día: {}".format(dia))
    menu_principal = Menu("Pasar de dia", "Estadísticas",
                          "Guardar estado", "Salir")
    menu_principal.display()

    # recuento

    muertos = 0
    infectados = 0
    for nombre_p, clase_p in mundo:
        if clase_p.estado == "infectado" and nombre_p not in paises_infectados:
            paises_infectados.append(nombre_p)
        else:
            if nombre_p in paises_infectados and clase_p.estado != "infectado":
                paises_infectados.remove(nombre_p)
        infectados += clase_p.infectados
        muertos += clase_p.muertos
    sanos = poblacion_mundial_inicial - infectados - muertos

    # fin recuento

    if menu_principal == 1:
        # avazar dia

        infectados_por_dia[dia] = 0
        muertos_por_dia[dia] = 0
        tasa_vida_por_dia[dia] = 0

        for nombre_p, clase_p in mundo:
            clase_p.avanzar_dia()

        # fin avanzar dia

        # respecto a la cura

        if not dia_descubrimiento_cura:
            prob_descubrimiento = max(
                0.003, (infeccion.visibilidad * infectados*(muertos**2)) /
                ((poblacion_mundial_inicial)**3))
            if random.random() < prob_descubrimiento:
                dia_descubrimiento_infeccion = dia
                #print("descubrieron la infeccion!")

            if dia_descubrimiento_infeccion:
                progreso_al_dia += (sanos/(2*poblacion_mundial_inicial))
                #print(progreso_al_dia,"progreso al dia",dia)

            if math.floor(progreso_al_dia) >= 1:
                dia_descubrimiento_cura = dia
                #print("descubrieron la cura!")
                nombre_elejido = random.choice(mundo.keys)
                #print("pais elejido de la cura", nombre_elejido)
                mundo[nombre_elejido].cura = True
                poseedores_de_cura.append(mundo[nombre_elejido].nombre)

        else:
            nuevas_conexiones = MiLista()
            for p_cura in poseedores_de_cura:
                # curamos 25% infectados de cada pais
                # si infectados queda en 0, pais, automaticamente modifica su
                # estado a limpio.
                mundo[p_cura].infectados = int(
                    mundo[p_cura].infectados * 0.25 *
                    infeccion.resistencia_a_medicina)
                # entregamos la cura a todos sus conexiones aereas
                for conexion_aeropuerto in mundo[p_cura].aeropuerto:
                    if (conexion_aeropuerto not in poseedores_de_cura and
                            mundo[conexion_aeropuerto].estado_aeropuerto and
                            not mundo[conexion_aeropuerto].estado == "muerto"):
                        mundo[conexion_aeropuerto].cura = True
                        mundo[conexion_aeropuerto].estado_frontera = True
                        mundo[conexion_aeropuerto].estado_aeropuerto = True
                        # print(p_cura,"transpasó la cura a",conexion_aeropuert
                        nuevas_conexiones.append(conexion_aeropuerto)
            for j in nuevas_conexiones:
                poseedores_de_cura.append(j)

        # fin respecto a la cura

        for nombre_pais, clase_pais in mundo:

            # solo hago cambios si el pais está infectado
            # and clase_pais.dia_inicio_infeccion != dia:
            if clase_pais.estado == "infectado":

                # update de infectados y muertos
                if (dia-int(clase_pais.dia_inicio_infeccion) > 10 and
                        clase_pais.infectados < 5 and
                        clase_pais.infectados > 0):
                    muertes = random.randint(1, clase_pais.infectados)
                else:
                    muertes = int(clase_pais.infectados *
                                  clase_pais.prob_muerte)
                clase_pais.muertos += muertes
                if clase_pais.estado == "muerto":
                    clase_pais.cura = False
                    poseedores_de_cura.remove(nombre_pais)
                    #print("muerte de", nombre_pais)

                clase_pais.infectados -= muertes
                nuevos_infectados = min(
                    int(random.randint(0,
                                       6 * clase_pais.infectados) *
                        clase_pais.efecto_mascarilla
                        * clase_pais.infeccion.contagiosidad),
                    clase_pais.sanos)
                clase_pais.infectados += nuevos_infectados
                muertos_por_dia[dia] += muertes
                infectados_por_dia[dia] += nuevos_infectados

                # fin update de infectados y muertos

                # contagio

                prob_contagio = 0
                if clase_pais.habitantes != clase_pais.muertos:
                    total_conexiones = len(
                        clase_pais.frontera) + len(clase_pais.aeropuerto)
                    if total_conexiones != 0:
                        prob_contagio = 0.3

                # contagiar por frontera

                if (len(clase_pais.frontera) != 0 and
                        clase_pais.estado_frontera and
                        ((clase_pais.infectados / clase_pais.habitantes)
                            > 0.2)):
                    for pais_fronterizo in clase_pais.frontera:
                        if (mundo[pais_fronterizo].estado_frontera and
                                random.random() <= prob_contagio and
                                not mundo[pais_fronterizo].infeccion):
                            print(pais_fronterizo, "contagiado por frontera")
                            paises_infectados_por_dia.append(
                                dia, pais_fronterizo)
                            mundo[pais_fronterizo].inicio_infeccion(
                                infeccion, dia)

                # contagiar por aeropuerto
                if (len(clase_pais.aeropuerto) != 0 and
                        clase_pais.estado_aeropuerto and
                        ((infectados / poblacion_mundial_inicial) > 0.04)):
                    for pais_aeropuerto in clase_pais.aeropuerto:
                        if (mundo[pais_aeropuerto].estado_aeropuerto
                                and random.random() <= prob_contagio and
                                not mundo[pais_aeropuerto].infeccion):
                            print(pais_aeropuerto, "contagiado por aeropuerto")
                            paises_infectados_por_dia.append(
                                dia, pais_aeropuerto)
                            mundo[pais_aeropuerto].inicio_infeccion(
                                infeccion, dia)

                # fin contagio

                # propuestas

                cerrar_frontera = ((clase_pais.infectados > 0.5 *
                                    clase_pais.habitantes) or
                                   (clase_pais.muertos > 0.25 *
                                    clase_pais.habitantes))
                if (cerrar_frontera and len(clase_pais.frontera) != 0 and
                        clase_pais.estado_frontera):
                    suma_porcentaje = 0
                    for pais_fronterizo in clase_pais.frontera:
                        x = mundo[pais_fronterizo].infectados / \
                            mundo[pais_fronterizo].habitantes
                        suma_porcentaje += x
                    cola_propuestas[nombre_pais + ",cerrar_frontera"] = round(
                        ((suma_porcentaje/100) *
                            clase_pais.infectados)/clase_pais.habitantes, 4)

                cerrar_aeropuertos = (clase_pais.infectados > 0.8 *
                                      clase_pais.habitantes) or (
                    clase_pais.muertos > 0.2 * clase_pais.habitantes)
                if (cerrar_aeropuertos and len(clase_pais.aeropuerto) != 0
                        and clase_pais.estado_aeropuerto and
                        not clase_pais.cura):
                    x = nombre_pais + ",cerrar_aeropuertos"
                    cola_propuestas[x] = round(
                        0.8*clase_pais.infectados/clase_pais.habitantes, 4)

                entregar_mascarillas = clase_pais.infectados > (
                    clase_pais.habitantes / 3)
                if entregar_mascarillas and not clase_pais.mascarilla:
                    x = nombre_pais + ",entregar_mascarillas"
                    cola_propuestas[x] = round(
                        0.5*clase_pais.infectados/clase_pais.habitantes, 4)

                abrir_frontera = (not clase_pais.estado_frontera and
                                  not cerrar_frontera) or clase_pais.cura
                abrir_aeropuertos = (not clase_pais.estado_frontera and
                                     not cerrar_aeropuertos) or clase_pais.cura

                a = nombre_pais + ",abrir_frontera"
                b = nombre_pais + ",abrir_aeropuerto"
                if clase_pais.cura:
                    y = round(clase_pais.infectados/clase_pais.habitantes, 4)
                    if abrir_frontera and not clase_pais.estado_frontera:
                        cola_propuestas[a] = y
                    if abrir_aeropuertos and not clase_pais.estado_aeropuerto:
                        cola_propuestas[b] = y
                else:
                    y = round(0.7*clase_pais.infectados /
                              clase_pais.habitantes, 4)
                    if abrir_frontera and not clase_pais.estado_frontera:
                        cola_propuestas[a] = y
                    if abrir_aeropuertos and not clase_pais.estado_aeropuerto:
                        cola_propuestas[b] = y

                # fin propuestas

        # nuevo recuento
        tasa_vida_por_dia[dia] = (
            infectados - muertos_por_dia[dia]) / infectados
        muertos = 0
        infectados = 0
        for nombre_p, clase_p in mundo:
            infectados += clase_p.infectados
            muertos += clase_p.muertos

        # fin nuevo recuento

        # ejecutar las 3 propuestas
        if len(cola_propuestas) != 0:
            # las ordeno de mayor a menor prioridad
            cola_propuestas.sort_values()
            for i in range(0, min(3, len(cola_propuestas))):
                accion, prioridad = cola_propuestas.pop()
                n_pais, accion = accion.split(",")
                # print(n_pais,"ocupo",accion)
                if accion == "entregar_mascarillas":
                    mascarillas_por_dia.append(dia, n_pais)
                    mundo[n_pais].mascarilla = True
                elif accion == "cerrar_frontera":
                    fronteras_cerrados_por_dia.append(dia, n_pais)
                    mundo[n_pais].estado_frontera = False
                elif accion == "cerrar_aeropuertos":
                    aeropuertos_cerrados_por_dia.append(dia, n_pais)
                    mundo[n_pais].estado_aeropuerto = False
                elif accion == "abrir_frontera":
                    mundo[n_pais].estado_frontera = True
                else:
                    mundo[n_pais].estado_aeropuerto = True

            # fin ejecutar las 3 propuestas
        dia += 1

    elif menu_principal == 2:
        menu_estadisticas = Menu("Resumen del dia", "Por Pais", "Global",
                                 "Muertes e infecciones por dia",
                                 "Promedio muertes e infecciones")
        menu_estadisticas.display()
        if menu_estadisticas == 1:

            print("Gente infectada el dia {} : {}\n".format(
                dia-1, infectados_por_dia[dia-1]))
            print("Gente que murio el dia {} : {}\n".format(
                dia-1, muertos_por_dia[dia-1]))
            print("Paises que se infectaron el dia {} : {}\n".format(
                dia - 1, paises_infectados_por_dia[dia - 1]))
            print("Paises que entregaron mascarillas el dia {} : {}\n".format(
                dia - 1, mascarillas_por_dia[dia - 1]))
            print("Fronteras que se cerraron el dia {} : {}\n".format(
                dia - 1, fronteras_cerrados_por_dia[dia - 1]))
            print("Aeropuertos que se cerraron el dia {} : {}\n".format(
                dia - 1, aeropuertos_cerrados_por_dia[dia - 1]))

        elif menu_estadisticas == 2:
            menupais2 = Menu()
            x = MiLista()
            i = 1
            for np, cp, in mundo:
                x.append(menupais2.append(str(i), np))
                i += 1
            nombre_pais_datos = menupais2.display()

            print("Datos de", nombre_pais_datos, "\n")
            print("Vivos: {} , Infectados: {} , Muertos: {}\n".format(
                mundo[nombre_pais_datos].sanos +
                mundo[nombre_pais_datos].infectados,
                mundo[nombre_pais_datos].infectados,
                mundo[nombre_pais_datos].muertos))

            propuestas_pais = MiLista()
            for key, _ in cola_propuestas:
                if nombre_pais_datos == key.split(",")[0]:
                    propuestas_pais.append(key.split(",")[1])

            print("Propuestas de {}: {}".format(
                nombre_pais_datos, propuestas_pais))

        elif menu_estadisticas == 3:
            print("Poblacion total viva: {} , Poblacion total muerta: {} ,"
                  " Poblacion total infectada: {} , "
                  "Poblacion total sana: {}\n".format(
                      poblacion_mundial_inicial-muertos, infectados, muertos,
                      poblacion_mundial_inicial-infectados-muertos))
            menu_mundo = Menu("Mostrar paises limpios",
                              "Mostrar paises infectados",
                              "Mostrar paises muertos")
            menu_mundo.display()
            x = ""
            for np, cp in mundo:
                if cp.estado == "limpio" and menu_mundo == 1:
                    x += np+", "
                elif cp.estado == "infectado" and menu_mundo == 2:
                    x += np+", "
                elif cp.estado == "muerto" and menu_mundo == 3:
                    x += np+", "
            print(x[:-2])

        elif menu_estadisticas == 4:
            if len(muertos_por_dia) == 0:
                print(
                    "Esta informacion es se guarda al guardar la partida,"
                    " solo a medida de avance de dias")

            for diax, valor in muertos_por_dia:
                print("Dia {} : Infectados {} , Muertos {}\n".format(
                    diax, infectados_por_dia[diax], valor))

        else:
            tasa_vida_promedio = 0
            for diax, valor in tasa_vida_por_dia:
                tasa_vida_promedio += valor
                print("Dia {} : Tasa de vida {} , Tasa de muerte {}\n".format(
                    diax, valor, 1-valor))
            print("Tasa de vida promedio: {} , "
                  "Tasa de muerte promedio: {}\n".format(
                      tasa_vida_promedio/len(tasa_vida_por_dia),
                      1-tasa_vida_promedio/len(tasa_vida_por_dia)))

    elif menu_principal == 3:  # menu guardar
        mundo_to_csv(mundo, dia_descubrimiento_infeccion,
                     dia_descubrimiento_cura,
                     progreso_al_dia, poseedores_de_cura, cola_propuestas)
        print("Partida guardada satisfactoriamente!")
    else:
        break
