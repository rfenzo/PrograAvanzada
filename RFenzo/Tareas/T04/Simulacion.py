import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Utilidades.Generadores import (credit_gen, controls_gen, nota_gen,
                                    hour_gen, person_gen, semanal_gen,
                                    half_month_gen, escenarios_gen)
from Utilidades.Funciones import (check_event, sort_dict_key,
                                  dia_semana, responder_dudas, prom)
from Clases.Personas import (Alumno, Ayu_Docencia, Ayu_Tareas, Profesor,
                             Coordinador)
from Datos.datos import materias, dif, parametros
from Clases.Menu import Menu
from Clases.MyDict import MyDict

from collections import OrderedDict
from math import ceil
from random import expovariate, uniform, choice, sample, random
from matplotlib import pyplot as plt
from numpy import mean


class Simulacion:
    '''
    esta es la clase que se encarga de realizar la simulacion, generando los
    eventos, ejecutandolos, etc.
    '''

    def __init__(self, imprimir, prob_40_creditos, prob_50_creditos,
                 prob_55_creditos, prob_60_creditos,
                 prob_visitar_profesor, prob_atraso_notas_Mavrakis,
                 porcentaje_progreso_tarea_mail, fiesta_mes,
                 partido_futbol_mes, nivel_inicial_confianza_inferior,
                 nivel_inicial_confianza_superior):
        '''
        todos los parametros ingresados al init son autoexplicativos, ademas
        de tener un tipo de datos explicito luego del '='.

        var dia: es el tiempo de simulacion | tipo:int

        var fin_simulacion: marca el fin de la simulacion cuando la nota del
        examen es publciada| tipo: bool

        var eventos: almacena un evento por cada tipo de evento | tipo: MyDict

        var ayu,tar,ctrl,cat,act : almacenan el nro de evaluacion  actual
        para cada tipo | tipo:int,int,int,int,int

        var gen_ctrl: es el generador de controles aleatorio | tipo:generator
        var gen_cat: es el generador de catedras | tipo:generator
        var gen_ayu: es el generador de ayudantias | tipo:generator
        var gen_ract: es el generador de actividades | tipo:generator
        var gen_tarea: es el generador de tareas | tipo:generator

        var alumnos_iniciales, profesores, ayu_docencia, ayu_tareas,
        coordinador: son generados por person_gen de Generadores.py.
        Son listas con objetos de Alumnos,Profesores, etc, segun lo que salga
        en integrantes.csv
        '''
        self.i = imprimir
        self.fiesta = fiesta_mes
        self.futbol = partido_futbol_mes

        self.porcent_progreso_tarea_mail = porcentaje_progreso_tarea_mail

        self.dia = 1
        self.fin_simulacion = False

        self.eventos = MyDict()
        self.ayu, self.tar, self.ctrl, self.cat, self.act = 1, 1, 1, 1, 1

        # generador de controles
        self.gen_ctrl = controls_gen()
        self.gen_cat = semanal_gen(4)
        self.gen_ayu = semanal_gen(2)
        self.gen_ract = semanal_gen(1)
        self.gen_tarea = half_month_gen(5)

        # generamos las personas
        self.alumnos_iniciales, self.profesores, self.ayu_docencia,\
            self.ayu_tareas, self.coordinador = \
            person_gen(prob_atraso_notas_Mavrakis, prob_40_creditos,
                       prob_50_creditos, prob_55_creditos, prob_60_creditos,
                       nivel_inicial_confianza_inferior,
                       nivel_inicial_confianza_superior, Alumno, Ayu_Tareas,
                       Ayu_Docencia, Profesor, Coordinador,
                       prob_visitar_profesor, self.i)

        self.aprob_dict = {}

    @property
    def semana(self):
        '''
        calcula la semana actual, dependiendo del atributo dia

        return semana actual
        return tipo: int
        '''
        return self.dia//7

    @property
    def mes(self):
        '''
        calcula el mes actual, dependiendo del atributo semana

        return mes actual
        return tipo: int
        '''
        return self.semana//4

    @property
    def materia_actual(self):
        '''
        calcula la materia actual, dependiendo del atributo semana y a
        materias que se obtiene de datos.py

        return materia actual
        return tipo: str
        '''
        if self.semana > 11:
            return materias[11]
        return materias[self.semana]

    @property
    def d(self):
        '''
        calcula el dia de la semana actual

        return nro de dia de la semana
        return tipo: int
        '''
        return self.dia-(ceil(self.dia/7)-1)*7

    @property
    def alumnos(self):
        '''
        calcula los alumnos que aun no han botado el ramo

        return alumno activos
        return tipo: list(Alumno)
        '''
        return [i for i in self.alumnos_iniciales if not i.botar]

    def gen_eventos(self):
        '''
        generara los siguientes eventos dependiendo de los eventos que
        actualemente estan esperando en self.eventos y finalmente los ordena
        segun su key, es decil, el dia en que sucede.

        return none
        return tipo: none
        '''

        if check_event("Ayudantia", self.eventos):  # todos los martes
            try:
                self.eventos.append(next(self.gen_ayu),
                                    "Ayudantia-"+str(self.ayu))
                self.ayu += 1
            except StopIteration:
                pass

        if check_event("Catedra", self.eventos):  # todos los jueves
            try:
                self.eventos.append(next(self.gen_cat),
                                    "Catedra-"+str(self.cat))
                self.cat += 1
            except StopIteration:
                pass

        if check_event("Control", self.eventos):  # algunos jueves
            try:
                self.eventos.append(7*next(self.gen_ctrl)+4,
                                    "Control-"+str(self.ctrl))
                self.ctrl += 1
            except StopIteration:
                pass

        if check_event("ReunionTarea", self.eventos):  # viernes por medio
            try:
                self.eventos.append(
                    next(self.gen_tarea), "ReunionTarea-"+str(self.tar))
                self.tar += 1
            except StopIteration:
                pass

        if check_event("ReunionAct", self.eventos):  # todos los lunes
            try:
                self.eventos.append(next(self.gen_ract),
                                    "ReunionAct-"+str(self.act))
                self.act += 1
            except StopIteration:
                pass

        if check_event("Fiesta", self.eventos):  # aleatorio
            if self.fiesta != 0:
                self.eventos.append(
                    ceil(self.dia+7+expovariate(self.fiesta)), "Fiesta")

        if check_event("Futbol", self.eventos):  # aleatorio
            if self.futbol != 0:
                self.eventos.append(ceil(
                    self.dia+7+expovariate(self.futbol)), "Futbol")

        if check_event("CorteAgua", self.eventos):  # aleatorio
            self.eventos.append(
                ceil(self.dia+7+expovariate(1/21)), "CorteAgua")

        for profesor in self.profesores:
            apellido = profesor.nombre.split(' ')[1]
            if check_event("Consultas-"+apellido, self.eventos):
                self.eventos.append(
                    ceil((self.semana+1)*7+profesor.dia_consulta),
                    "Consultas-" + apellido)

        # los ordenamos por día
        self.eventos = sort_dict_key(self.eventos)

    def ejecutar_evento(self, evento):
        '''
        ejecuta un evento especifico llamando a las funciones correspondientes

        param evento: evento que se ejecutara | tipo: string

        return none
        return tipo: none
        '''

        if "Ayudantia" in evento:  # faltan preguntas en ayudantia
            evento, nro_evento = evento.split('-')
            elejidos = sample(self.ayu_docencia, 2)
            # si alguno de los dos conoce de la materia, entonces se daran tips

            if self.materia_actual in elejidos[0].dominios or \
                    self.materia_actual in elejidos[1].dominios:
                for alumno in self.alumnos:
                    alumno.S_bonus_dict[self.semana] += 0.1
            if self.i:
                print("Semana: {} | Día: {:^9} | Ayudantia {}: {} alumnos"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              nro_evento, len(self.alumnos)))

        elif "Catedra" in evento:
            evento, nro_evento = evento.split('-')
            for alumno in self.alumnos:
                # 50% de haber escuchado
                if random() < 0.5:
                    alumno.S_bonus_dict[self.semana] += 0.1
            if self.i:
                print("Semana: {} | Día: {:^9} | Cátedra {}: {} alumnos"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              nro_evento, len(self.alumnos)))

        elif evento.split('-')[0] in ["Actividad", "Control",
                                      "EntregaTarea", "Examen"]:
            if '-' in evento:
                evento, nro_evento = evento.split('-')
            else:
                nro_evento = ''

            if evento == "Actividad":
                for i in range(len(self.profesores)):
                    nro = i+1
                    s = [x for x in self.alumnos if x.seccion == str(nro)]
                    responder_dudas(self.ayu_docencia[
                                    3*(nro-1):3*nro], s, self.semana)

            for alumno in self.alumnos:
                alumno.rendir_evaluacion(evento)

            # para graficar despues
            Alumno.mem_semana.append(evento, self.semana)

            if evento != "EntregaTarea":
                self.eventos.append(
                    self.dia+14, evento+"|NotaCoord-"+nro_evento)
            else:
                self.eventos.append(self.dia+14, "Tarea|NotaCoord-"+nro_evento)

            if self.i:
                print("Semana: {} | Día: {:^9} | {} {}: {} alumnos"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              evento, nro_evento, len(self.alumnos)))

            if evento == "Actividad" and self.i:
                for ayu in self.ayu_docencia[:9]:
                    print("Ayudante {} contestó {} dudas durante actividad"
                          .format(ayu.nombre, ayu.ayudados[self.semana]))

        elif "ReunionTarea" in evento:
            evento, nro_evento = evento.split('-')
            lim_sup = int(parametros['lim_sup_random_exigencia'])
            lim_inf = int(parametros['lim_inf_random_exigencia'])
            Ayu_Tareas.exigencia = round(
                7 + uniform(lim_inf, lim_sup)/dif[self.materia_actual], 3)

            self.eventos.append(self.dia+14, "EntregaTarea-"+nro_evento)

            if self.i:
                print("Semana: {} | Día: {:^9} | ReunionTarea {}: exigencia {}"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              nro_evento, Ayu_Tareas.exigencia))

        elif "ReunionAct" in evento:
            evento, nro_evento = evento.split('-')
            lim_sup = int(parametros['lim_sup_random_exigencia'])
            lim_inf = int(parametros['lim_inf_random_exigencia'])
            Ayu_Docencia.exigencia = round(
                7 + uniform(lim_inf, lim_sup)/dif[self.materia_actual], 3)

            self.eventos.append(self.dia+3, "Actividad-"+nro_evento)
            if self.i:
                print("Semana: {} | Día: {:^9} | ReunionAct {}: exigencia {}"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              nro_evento, Ayu_Docencia.exigencia))

        elif 'NotaCoord' in evento:
            tipo = evento.split('|')[0]
            nro_evento = evento.split('-')[1]

            if tipo != "Tarea":
                retraso_publicacion = Ayu_Docencia.corregir(self.alumnos,
                                                            tipo,
                                                            self.coordinador,
                                                            self.materia_actual
                                                            )
            else:
                retraso_publicacion = Ayu_Tareas.corregir(self.alumnos,
                                                          self.coordinador)

            self.eventos.append(self.dia+retraso_publicacion,
                                tipo+"|PublNotas-"+nro_evento)

            texto1 = "Semana: {} | Día: {:^9} | Ayudantes:".format(
                str(self.semana).zfill(2), dia_semana(self.d))
            texto2 = " notas de {} {} al cordinador".format(tipo, nro_evento)
            if self.i:
                print(texto1+texto2)

            if retraso_publicacion > 0 and self.i:
                print()
                print("El coordinador retrasa la entrega de {} {} en {} días"
                      .format(tipo, nro_evento, retraso_publicacion))
                print()

        elif 'PublNotas' in evento:
            tipo = evento.split('|')[0]
            nro_evento = evento.split('-')[1]

            self.fin_simulacion, promedio = self.coordinador.publicar_notas(
                self.alumnos, tipo)

            t1 = ("Semana: {} | Día: {:^9} | Notas {} {}: "
                  .format(str(self.semana).zfill(2), dia_semana(self.d), tipo,
                          nro_evento, Ayu_Docencia.exigencia))
            t2 = "Promedio {}".format(promedio)
            if self.i:
                print(t1+t2)

            if tipo == "Tarea" and nro_evento == "6":
                self.eventos.append(self.dia+5, "Examen")

        elif evento == "Fiesta":
            elejidos = sample(self.alumnos, min(len(self.alumnos), 50))
            for alumno in elejidos:
                alumno.fiesta()
            if self.i:
                print("Semana: {} | Día: {:^9} | Fiesta: {} alumnos"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              len(elejidos)))

        elif evento == "CorteAgua":
            for profe in self.profesores:
                profe.nro_consultas = 6
            if self.i:
                print("Semana: {} | Día: {:^9} | Corte de agua"
                      .format(str(self.semana).zfill(2), dia_semana(self.d)))

        elif evento == "Futbol":
            elejidos = sample(self.alumnos, round(0.8*len(self.alumnos)))
            for alumno in elejidos:
                alumno.futbol()
            Ayu_Tareas.exigencia *= 1.2
            if self.i:
                print("Semana: {} | Día: {:^9} | Futbol: {} alumnos"
                      .format(str(self.semana).zfill(2), dia_semana(self.d),
                              len(elejidos)))

        elif "Consultas" in evento:
            apellido = evento.split('-')[1]
            for profe in self.profesores:
                if apellido in profe.nombre:
                    profe.atender(self.semana)

    def run(self):
        '''
        metodo principal de la simulacion, es donde se produce la iteracion
        hasta el fin del curso.

        Algoritmo:

        0. check fin_simulacion
        1. genera los eventos que falten
        2. saca el primer evento de self.eventos
        3. actualiza el dia (tanto para simulacion.py como para alumnos)
        4. se ejecuta el evento
        5. Go to 0

        return none
        return tipo:none
        '''

        while not self.fin_simulacion:
            # se generan los proximos eventos
            self.gen_eventos()

            # se actualiza el dia y se atienden los eventos del dia
            semana_anterior = self.semana
            mes_anterior = self.mes
            self.dia, eventos = self.eventos.popitem(last=False)
            semana_posterior = self.semana
            mes_posterior = self.mes

            if mes_anterior != mes_posterior:
                self.aprob_dict[mes_anterior] = self.aprobacion

            for alumno in self.alumnos:
                alumno.refresh(self.d, self.dia, self.semana)

                for profe in self.profesores:
                    if semana_anterior != semana_posterior:
                        profe.nro_consultas = 10

                    profe.check_consulta(alumno, self.semana)

            for evento in eventos:
                self.ejecutar_evento(evento)

        return self.aprobacion

    def graficar(self):
        '''
        metodo para graficar las notas promedio del curso

        return none
        return tipo: none
        '''
        x_c = Alumno.mem_semana['Control']
        y_c = self.coordinador.promedios['Control']
        x_t = Alumno.mem_semana['EntregaTarea']
        y_t = self.coordinador.promedios['Tarea']
        x_a = Alumno.mem_semana['Actividad']
        y_a = self.coordinador.promedios['Actividad']
        x_e = Alumno.mem_semana['Examen']
        y_e = self.coordinador.promedios['Examen']

        plt.plot(x_c, y_c, label='Controles')
        plt.plot(x_t, y_t, label='Tareas')
        plt.plot(x_a, y_a, label='Actividades')
        plt.plot(x_e, y_e, label='Examen', marker='o', markersize=3)
        plt.title('Notas promedio v/s semanas')
        plt.xlabel('Semana')
        plt.ylabel('Notas promedio')
        plt.legend()
        plt.show()

    def nro_botar_ramo(self):
        '''
        calcula el numero de alumnos que botaron el ramo

        return numero de desertores
        return tipo: int
        '''
        return len(self.alumnos_iniciales)-len(self.alumnos)

    def c_iniciales(self):
        '''
        calcula la confianza inicial promedio del curso

        return promedio confianza inicial
        return tipo: float
        '''
        x = [i.confianza_inicial for i in s.alumnos_iniciales]
        return round(mean(x), 2)

    def c_finales(self):
        '''
        calcula la confianza final promedio de los alumnos activos

        return promedio confianza final de quienes no botaron el ramo
        return tipo: float
        '''
        x = [i.C for i in s.alumnos]
        return round(mean(x), 2)

    def c_finales_todos(self):
        '''
        calcula la confianza final promedio del curso, incluyendo los
        desertores

        return promedio confianza final total
        return tipo: float
        '''
        x = [i.C for i in s.alumnos_iniciales]
        return round(mean(x), 2)

    @property
    def aprobacion(self):
        '''
        calcula el numero de alumno que aprobaron el curso

        return nro aprobados
        return tipo:
        '''
        al_inic = self.alumnos_iniciales
        iniciales = 100*len([None for i in al_inic
                             if i.promedio_final >= 3.95])/len(al_inic)
        activos = 100*len([None for i in self.alumnos
                           if i.promedio_final >= 3.95]) / len(self.alumnos)
        return (iniciales, activos, self)


def my_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

simulaciones = {}
while True:

    sim = Menu("Realizar una simulacion", "Realizar multiples simulaciones",
               "Mostrar escenario que maximiza el porcentaje de aprobación")
    sim.display()

    if sim == 1:
        # se cargan los parametros de parametros.csv
        prob_40_creditos = float(parametros['prob_40_creditos'])
        prob_50_creditos = float(parametros['prob_50_creditos'])
        prob_55_creditos = float(parametros['prob_50_creditos'])
        prob_60_creditos = float(parametros['prob_60_creditos'])
        prob_visitar_profesor = float(parametros['prob_visitar_profesor'])
        prob_atraso_notas_Mavrakis = float(
            parametros['prob_atraso_notas_Mavrakis'])
        porcentaje_progreso_tarea_mail = float(
            parametros['porcentaje_progreso_tarea_mail'])
        fiesta_mes = float(parametros['fiesta_mes'])
        partido_futbol_mes = float(parametros['partido_futbol_mes'])
        nivel_inicial_confianza_inferior = int(
            parametros['nivel_inicial_confianza_inferior'])
        nivel_inicial_confianza_superior = int(
            parametros['nivel_inicial_confianza_superior'])

        s = Simulacion(True, prob_40_creditos, prob_50_creditos,
                       prob_55_creditos,
                       prob_60_creditos, prob_visitar_profesor,
                       prob_atraso_notas_Mavrakis,
                       porcentaje_progreso_tarea_mail, fiesta_mes,
                       partido_futbol_mes, nivel_inicial_confianza_inferior,
                       nivel_inicial_confianza_superior)
        s.run()

        while True:
            estad = Menu("Volver al menu anterior", "Gráfico",
                         "Estadísticas Personales", "Estadísticas Finales")
            estad.display()
            if estad == 1:
                break
            elif estad == 2:
                s.graficar()

            elif estad == 3:
                print()
                print("ESTADÍSTICAS PERSONALES")

                persona = None
                while not persona:
                    nombre = input("Ingrese el nombre del alumno\n")
                    for alumno in s.alumnos_iniciales:
                        if alumno.nombre == nombre:
                            persona = alumno

                while True:
                    ep = Menu("Volver al menu anterior",
                              "Ver sus cualidades",
                              "Notas de cada evaluacion y su promedio final")
                    ep.display()
                    if ep == 1:
                        break
                    elif ep == 2:
                        print("Nivel de programacion promedio: {}"
                              .format(prom(persona.P_dict)))
                        print('Confianza promedio: {} | Confianza final: {}'
                              .format(prom(persona.C_dict),
                                      round(persona.C, 2)))
                        print('Manejo cont prom: {} | Manejo cont final: {}'
                              .format(prom(persona.S_dict),
                                      round(persona.S_sem, 2)))
                    elif ep == 3:
                        print('Notas de cada evaluacion')
                        for tipo, notas in persona.notas.items():
                            notas = ['Nota:' + str(round(i, 2)) for i in notas]
                            notas = enumerate(notas, 1)
                            for nro, nota in notas:
                                print(tipo, nro, nota)

                        print()
                        print('Promedio final')
                        print(round(persona.promedio_final, 2))

            elif estad == 4:
                while True:
                    print()
                    print("ESTADÍSTICAS FINALES")
                    ef = Menu("Volver al menu anterior",
                              "Cantidad total de alumnos que quisieron" +
                              " botar el ramo",
                              "Promedio de confianza al inicio y" +
                              " al final del ramo",
                              "Mes con más aprobación que tuvo el ramo",
                              "Tareas, actividades y " +
                              "examen aprobados v/s reprobados",
                              "Porcentaje de alumnos que " +
                              "aumentaron su confianza " +
                              "y cuantos la disminuyeron")
                    ef.display()
                    if ef == 1:
                        break
                    elif ef == 2:
                        print()
                        print('{} alumnos decidieron botar el ramo'
                              .format(s.nro_botar_ramo()))
                    elif ef == 3:
                        print('Promedio confianza inicial: {}'
                              .format(s.c_iniciales()))
                        print('Promedio confianza final aprobados: {}'
                              .format(s.c_finales()))
                        print('Promedio confianza final de todos: {}'
                              .format(s.c_finales_todos()))
                    elif ef == 4:
                        print()
                        print("Segun aprobacion del total de alumnos")
                        maximo = max(s.aprob_dict.items(),
                                     key=lambda x: x[1][0])
                        print("Mes: {} | Aprobacion: {}%"
                              .format(maximo[0], round(maximo[1][0]), 2))
                        print()
                        print("Segun aprobacion de los alumnos activos")
                        maximo = max(s.aprob_dict.items(),
                                     key=lambda x: x[1][1])
                        print("Mes: {} | Aprobacion: {}%"
                              .format(maximo[0], round(maximo[1][1]), 2))
                        print()
                    elif ef == 5:
                        print('Porcentajes aprobados v/s reprobados:')
                        print()
                        for tipo, p in s.coordinador.aprob_reprob.items():
                            p = enumerate(p, 1)
                            for nro, string in p:
                                print(tipo, nro, string)

                    elif ef == 6:
                        print('NO IMPLEMENTADO')

    elif sim == 2:
        escenarios = escenarios_gen()

        for numero, params in escenarios.items():
            my_print("Comenzando simulacion " + str(numero) + "\n")
            si = Simulacion(False, **params)
            aprobacion = si.run()
            simulaciones[numero] = aprobacion
            my_print("Simulacion " + str(numero) + " terminada!"+"\n")
            my_print("\n")

    elif sim == 3:
        if simulaciones == {}:
            print('Primero realiza una simulacion de multiples escenarios')
        else:
            print()
            print("Maximizacion segun total de alumnos:\n")
            maximo = max(simulaciones.items(),
                         key=lambda x: x[1][0])
            texto = ("Aprobacion del total de alumnos {}%"
                     .format(round(maximo[1][0], 2)))
            print("Escenario {}: {} | {}".format(maximo[0], texto, texto2))
            print("Los parametros utilizados fueron los siguientes:")

            for key, value in vars(maximo[2][2]).items():
                print(key, value)
            print()
            print("Maximizacion segun alumnos activos:\n")
            maximo = max(simulaciones.items(),
                         key=lambda x: x[1][1])
            texto2 = ("Aprobacion de los alumnos activos {}%"
                      .format(round(maximo[1][1], 2)))
            print("Escenario {}: {} | {}".format(maximo[0], texto, texto2))
            print("Los parametros utilizados fueron los siguientes:")

            for key, value in vars(maximo[2][2]).items():
                print(key, value)
