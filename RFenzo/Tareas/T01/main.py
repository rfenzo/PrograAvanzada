import os

from Clases.Personas import Persona
from Clases.Recursos import Recurso
from Funciones.date import ingresar_fecha, filter_by_date
from Clases.Menu import Menu

from Clases.Incendios import Incendio
from Funciones.custom_csv import csv_to_dict

if not os.path.exists("Reportes Estrategias de Extinción"):
    os.makedirs("Reportes Estrategias de Extinción")
    print("Creando carpeta Reportes Estrategias de Extinción," +
          " reinicia el script")
    quit()

recursos = [Recurso(x) for x in csv_to_dict("recursos.csv")]

while True:
    users = csv_to_dict('usuarios.csv')
    username = input('Nombre usuario:\n')
    succesful = False
    for user in users:
        if user["nombre"] == username:
            password = input('Password:\n')
            if user["contraseña"] == password:
                print('Ingreso satisfactorio!')
                succesful = True
            break

    if not succesful:
        print('Nombre de usuario o password incorrecta\n')
        continue

    cerrar_sesion = False

    while True:
        if cerrar_sesion:
            break

        fecha = ingresar_fecha()
        persona = Persona(user["recurso_id"], user["nombre"], fecha)

        while True:
            if persona.id_recurso == "":
                menu = Menu("Ver o modificar base de datos", 'Consultar',
                            'Planificar estrategia de extincion',
                            "Cambiar tiempo y fecha", "Cerrar sesión")
                menu.display()
                incendios = [Incendio(x, fecha) for x in filter_by_date(
                    csv_to_dict("incendios.csv"), fecha)]

                if menu == 1:
                    menu2 = Menu("Ver recursos.csv", "Ver usuarios.csv",
                                 "Ver incendios.csv",
                                 "Crear nuevos usuarios",
                                 "Agregar pronóstico meteorológico",
                                 "Agregar incendio")
                    menu2.display()
                    if menu2 == 1:
                        persona.ver("recursos.csv")
                    elif menu2 == 2:
                        persona.ver("usuarios.csv")
                    elif menu2 == 3:
                        persona.ver("incendios.csv")
                    elif menu2 == 4:
                        persona.modificar_archivo("usuarios.csv")
                    elif menu2 == 5:
                        persona.modificar_archivo("meteorologia.csv")
                    else:
                        persona.modificar_archivo("incendios.csv")

                elif menu == 2:

                    menu3 = Menu("Incendio por id", "Recurso por id",
                                 'Incendios activos',
                                 'Incendios apagados',
                                 'Recursos mas utilizados',
                                 'Recursos mas efectivos')
                    menu3.display()
                    if menu3 == 1:
                        menu9 = Menu()
                        for j in incendios:
                            menu9.append(j.id, "Incendio id {}".format(j.id))
                        menu9.display()

                        for j in incendios:
                            if int(j.id) == menu9:
                                print(j)

                    elif menu3 == 2:
                        menu10 = Menu()
                        for j in recursos:
                            menu10.append(j.id, "Recurso id {}".format(j.id))
                        menu10.display()

                        for j in recursos:
                            if int(j.id) == menu10:
                                print(j)

                    elif menu3 == 3:
                        for j in incendios:
                            if j.puntos_poder > 0:
                                print('Id: {}, fecha inicio: {}, recursos' +
                                      ' utilizados {}, ' +
                                      'porcentaje extincion: {}'
                                      .format(j.id,
                                              j.fecha_inicio,
                                              j.recursos_utilizados,
                                              j.porcentaje_extincion))
                        print("\n")

                    elif menu3 == 4:
                        for j in incendios:
                            if j.puntos_poder == 0:
                                print('Id: {}, fecha inicio: {}, ' +
                                      'fecha termino: {}, ' +
                                      'recursos utilizados {}'
                                      .format(j.id,
                                              j.fecha_inicio,
                                              j.fecha_termino,
                                              j.recursos_utilizados))
                        print("\n")
                    elif menu3 == 5:  # falta! pag 5
                        pass
                    elif menu3 == 6:  # falta! pag 5
                        pass

                elif menu == 3:
                    recursos = [Recurso(x)
                                for x in csv_to_dict("recursos.csv")]

                    menu4 = Menu()
                    for j in incendios:
                        menu4.append(j.id, "  Porcentaje extincion: {}".format(
                            j.porcentaje_extincion))
                    menu4.display()

                    menu5 = Menu("Cantidad recursos",
                                 "Tiempo extinción", "Costo económico")
                    menu5.display()

                    objetivo = None
                    for j in incendios:
                        if int(j.id) == menu4:
                            objetivo = j
                    if not objetivo:
                        print(
                            "El id ingresado no corresponde a ningún" +
                            " incendio activo presente hasta la fecha.")
                        continue

                    if menu5 == 1:  # por nro de recursos
                        """             ESTO ESTARIA ACTIVO SI PUDIERA SIMULAR
                        recursos2 = recursos
                        activo = True
                        tiempo = fecha

                        while activo:
                            recursos_prueba = []
                            for p in recursos2:
                                p.incendio = objetivo
                                p._fecha_actual = p.incendio._fecha_actual
                                recursos_prueba.append(p)

                            recurso = max(recursos_prueba, key = lambda  p:
                             p.check_puntos_extincion_por_salida)
                            objetivo.agregar_recurso(recurso)

                            #if geq(recurso.fecha_llegada_incendio,tiempo):
                             #permite adelantarnos al instante en que llega 
                             al incendio
                            #    tiempo = recurso.fecha_llegada_incendio

                            activo = objetivo.update(tiempo)


                            tiempo = convertir_a_fecha(convertir_a_horas(
                            tiempo)+1)
                        """

                elif menu == 4:
                    break
                elif menu == 5:
                    cerrar_sesion = True
                    break

            else:
                print(
                    "---------BARRA DE ESTADO----------------------\n")
                print(persona.recurso)
                menu = Menu("Ver incendios.csv", "Ver recursos.csv",
                            "Cambiar tiempo y fecha", "Cerrar sesión")
                menu.display()
                if menu == 1:
                    persona.ver("incendios.csv")
                elif menu == 2:
                    persona.ver("recursos.csv")
                elif menu == 3:
                    break
                elif menu == 4:
                    cerrar_sesion = True
                    break
