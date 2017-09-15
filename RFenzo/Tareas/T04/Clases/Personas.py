import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Utilidades.Generadores import hour_gen, nota_gen
from Datos.datos import dif, ponderacion, materias, parametros
from random import uniform, random, randint, sample, choice
from Utilidades.Funciones import perso_tareas, perso, dia_semana
from Clases.MyDict import MyDict
from numpy import mean


class Alumno:
    '''
    Todo alumno del curso sera representado mediante un objeto de esta clase
    '''
    # para poder graficar despues
    mem_semana = MyDict()

    def __init__(self, nombre, seccion, confianza_inicial,
                 prob_visitar_profesor, creditos, imprimir):
        '''
        param nombre: Nombre del alumno | tipo: str
        param seccion: Seccion del alumno  | tipo: str
        param confianza_inicial : Conf. inicial generada random  | tipo: float
        param personalidad: Personalidad del alumno  | tipo: str
        param prob_visitar_profesor: prob_visitar_profesor | tipo: float
        param creditos: Nro creditos del alumno  | tipo: int

        var horas_disp: horas_disp semanales del alumno, cambia cada semana
        | tipo: float

        var progreso: almacena el ultimo progreso de cada tipo de 
        evaluacion  | tipo: dict

        var notas_esperadas: almacena temporalmente las notas esperadas, 
        una vez que se calcula la confianza relacionada a una entrega de 
        notas, se quita del diccionario, funciona como una fila | tipo: MyDict

        var notas: almacena todas las notas de cada tipo de evaluacion  
        | tipo: MyDict

        var semana: semana actual de la simulacion  | tipo: int
        var botar: True significa que el alumno boto el ramo  | tipo: bool

        var S_dict: almacena semana a semana el manejo de contenido  
        | tipo: dict

        var S_bonus_dict: almacena los bonus semanales al manejo de 
        contenidos, como por ejemplo el haber escuchado al profesor en clases 
        | tipo: float

        var Ht_dict: almacena Ht semanalmente  | tipo: dict
        var Hs_dict: almacena Hs semanalmente  | tipo: dict

        var Ht_perdido: almacena Ht perdido semanalmente, por ejemplo al 
        jugar futbol  | tipo: dict

        var Hs_perdido: almacena Hs perdido semanalmente, por ejemplo al ir 
        a una fiesta  | tipo: dict

        var P_dict: almacena P semanalmente | tipo: dict

        var C_dict: almacena semana a semana la confianza | tipo: dict

        var C_notas: almacena la confianza generada por una nota recien entregada | tipo: float

        var reunion_dict: almacena las semanas en que se reunio con el profesor | tipo: dict

        var fiesta_dict: almacena las semanas en que fue a fiesta | tipo: dict
        var futbol_dict: almacena las semanas en que jugo futbol | tipo: dict
        '''
        self.nombre = nombre
        self.seccion = seccion
        self.confianza_inicial = confianza_inicial
        self.personalidad = choice(["Eficiente", "Artistico", "Teorico"])
        self.creditos = creditos
        self.horas_disp = hour_gen(creditos)
        self.prob_visitar_profesor = prob_visitar_profesor
        self.i = imprimir
        self.progreso = {}

        self.notas_esperadas = MyDict()

        self.notas = MyDict()
        self.notas["Actividad"] = []
        self.notas["Control"] = []
        self.notas["Tarea"] = []
        self.notas["Examen"] = []

        self.semana = 0
        self.botar = False

        # manejo contenidos
        # key son semanas
        self.S_dict = {}
        self.S_bonus_dict = dict((i, 1) for i in range(20))

        # horas estudio
        # key son semanas
        self.Ht_dict = {}
        self.Hs_dict = {}

        self.Hs_perdido = dict((i, 0) for i in range(20))
        self.Ht_perdido = dict((i, 0) for i in range(20))

        # nivel programacion
        # key son semanas
        self.P_dict = {}
        self.P_bonus_dict = dict((i, 1) for i in range(20))

        # confianza
        # key son semanas
        self.C_dict = {}
        self.C_notas = 0

        # fiesta, futbol y reuniones
        self.reunion_dict = {}
        self.fiesta_dict = {}
        self.futbol_dict = {}

    def refresh(self, dia_semana, dia, semana):
        '''
        actualiza el dia y dia de semana, y si es una semana diferente a la 
        anterior guarda todos los datos de la semana pasada en diccionarios 
        del init, guarda la semana actual y genera una nueva cantidad de horas 
        disponibles

        param dia_semana: desde Simulacion.py decibe el dia de semana de la 
        simulacion | tipo: int

        param dia: desde Simulacion.py decibe el dia de la 
        simulacion | tipo: int

        param semana: desde Simulacion.py decibe la semana de la 
        simulacion | tipo: int

        return None
        return tipo: None
        '''
        self.dia = dia
        self.dia_semana = dia_semana

        if semana != self.semana:
            self.S_dict[self.semana] = self.S_sem
            self.Hs_dict[self.semana] = self.Hs_sem
            self.Ht_dict[self.semana] = self.Ht_sem
            self.P_dict[self.semana] = self.P
            self.C_dict[self.semana] = self.C

            self.semana = semana
            # la confianza de esta semana parte con la confianza pasada
            self.C_dict[self.semana] = self.C_dict[self.semana-1]

            self.horas_disp = hour_gen(self.creditos)

    @property
    def materia_actual(self):
        '''
        calcula la materia actual segun la semana actual y el diccionario 
        materias almacenado en datos.py.

        return materia actual
        return tipo: string
        '''
        if self.semana > 11:
            return materias[11]
        return materias[self.semana]

    @property
    def promedio_final(self):
        '''
        calcula el promedio del alumno, en caso de que la nota de examen ya 
        este disponible, entrega el promedio final utilizando las 
        ponderaciones almacenadas en datos.py

        return promedio final
        return tipo: float
        '''
        if self.notas['Examen'] == []:
            return self.promedio
        act = mean(self.notas['Actividad'])*ponderacion['Actividad']
        tarea = mean(self.notas['Tarea'])*ponderacion['Tarea']
        ctrl = mean(self.notas['Control'])*ponderacion['Control']
        examen = self.notas['Examen'][0]*ponderacion['Examen']

        return round(act+tarea+ctrl+examen, 2)

    @property
    def Ht_sem(self):
        '''
        calcula las horas semanales disponibles para dedicar a la tarea, 
        incluyendo los descuentos por fiestas y otras cosas

        return horas semanales disponibles para tarea
        return tipo: float
        '''
        return 0.7*self.horas_disp - self.Ht_perdido[self.semana]

    @property
    def Hs_sem(self):
        '''
        calcula las horas semanales disponibles para dedicar a estudio, 
        incluyendo los descuentos por fiestas y otras cosas

        return horas semanales disponibles para estudio
        return tipo: float
        '''
        return 0.3*self.horas_disp - self.Hs_perdido[self.semana]

    @property
    def S_sem(self):
        '''
        calcula el manejo de contenidos semanal, 
        incluyendo los bonus por preguntas al ayudante y otras cosas

        return manejo de contenidos semanal
        return tipo: float
        '''
        bonus = self.S_bonus_dict[self.semana]
        return (self.Hs_sem/dif[self.materia_actual])*bonus

    # INICIO NIVEL DE PROGRAMACION P, FIESTAS, FUTBOL Y REUNION
    @property
    def P(self):
        '''
        calcula el nivel de programacion semanal, considerando los efectos de 
        reunion y fiesta

        return nivel de programacion semanal
        return tipo: float 
        '''

        if self.semana == 0:
            lim_sup = int(parametros['lim_sup_random_p_inicial'])
            lim_inf = int(parametros['lim_inf_random_p_inicial'])
            return uniform(lim_inf, lim_sup)
        else:
            return 1.05*(1+self.efecto_reunion +
                         self.efecto_fiesta)*self.P_dict[self.semana-1]

    def reunion(self):
        '''
        agrega a reunion_dict[semana actual], el dia de la semana en que se 
        visita al profesor

        return None
        return tipo: None
        '''
        self.reunion_dict[self.semana] = self.dia_semana

    def fiesta(self):
        '''
        agrega a fiesta_dict[semana actual], el dia de la semana en que va a
         una fiesta y se agregan dias perdidos de horas de estudio

        return None
        return tipo: None
        '''
        self.fiesta_dict[self.semana] = self.dia_semana
        self.Hs_perdido[self.semana] += 2

    def futbol(self):
        '''
        agrega a futbol_dict[semana actual], el dia de la semana en que juega
        futbol y se agregan dias perdidos de horas de estudio y de tarea

        return None
        return tipo: None
        '''
        self.futbol_dict[self.semana] = self.dia_semana
        self.Ht_perdido[self.semana] += self.Ht_sem/7
        # si juegan futbol hasta del jueves, pierden tiempo estudio
        if self.dia_semana <= 4:
            self.Hs_perdido[self.semana] += self.Hs_sem/7

    @property
    def efecto_reunion(self):
        '''
        Es utilizado para calcular el nivel de programacion (P).

        return 0,08 si se reunio con el profesor esa semana,0 si no
        return tipo: float 
        '''
        if self.semana in self.reunion_dict:
            return 0.08
        return 0

    @property
    def efecto_fiesta(self):
        '''
        Es utilizado para calcular el nivel de programacion (P).

        return 0,08 si fue a fiesta esa semana,0 si no
        return tipo: float 
        '''
        if self.semana in self.fiesta_dict:
            return 0.15
        return 0

    @property
    def promedio(self):
        '''
        Es un promedio simple de notas, para cuando aun no se tiene examen

        return promedio simple
        return tipo: float 
        '''
        promedio = 0
        for tipo, notas in self.notas.items():
            if notas != []:
                promedio += mean(notas)/4
            else:
                promedio += 1.0/4

        return promedio

    @property
    def solicitar_reunion(self):
        '''
        Si el alumno tiene promedio menor a 5, solicita una reunion con el 
        profesor, si no, tien 20% de prob de solicitarla.

        return True si solicita la reunion
        return tipe: bool
        '''
        if self.promedio <= 5:
            pass
        elif random() >= self.prob_visitar_profesor:
            return False
        return True

    # FINAL NIVEL DE PROGRAMACION P, FIESTAS, FUTBOL Y REUNION

    # INICIO CONFIANZA C Y RECIBIR NOTA
    @property
    def C(self):
        '''
        calcula la confianza del alumno de acuerdo a la confianza de la semana 
        anterior y la confianza de las nota que le entregan esta semana

        return la confianza hasta el dia de hoy.
        return tipe: float
        '''
        if self.semana == 0:
            return self.confianza_inicial + self.C_notas
        else:
            self.C_dict[self.semana] += self.C_notas
            return self.C_dict[self.semana]

    def recibir_nota(self, nota, tipo):
        '''
        al recibir una nota, modifica su nivel de confianza segun la nota, 
        ademas se encarga de botar el ramo en el momento dado

        param nota: nota entregada por el coordinador | tipo: float
        param tipo: tipo de nota entregada por el coordinador | tipo: string

        return none
        return tipo: none
        '''
        self.notas.append(tipo, nota)
        if len(self.notas["Actividad"]) == 4 and self.check_botar_ramo():
            self.botar = True
        self.C_notas = self.calc_confianza(nota, tipo)

    def check_botar_ramo(self):
        '''
        revisa si debe botar el ramo o no segun la suma de las notas actuales
         y su confianza actual.

        return True si bota, False en otro caso
        return tipe: bool
        '''
        notas = 0
        for tipo, lista in self.notas.items():
            for nota in lista:
                notas += nota
        if self.C*0.8 + notas*0.2 < 20:
            texto = "suma de notas {:>5} y confianza {:<5}".format(round(
                notas, 2), round(self.C, 2))
            if self.i:
                print("{:>21} botó el ramo con {:>15}".format(
                    self.nombre, texto))
            return True
        return False

    def calc_confianza(self, nota, tipo):
        '''
        data una nota y tipo calcula en cuanto afecta a la confianza actual 
        debido a la diferencia con la nota esperada.

        param nota: nota entregada por el coordinador | tipo: float
        param tipo: tipo de nota entregada por el coordinador | tipo: string

        return k*(nota-nota_esp) doned k es una constante que depende del tipo
        return tipo: float
        '''
        ca = float(parametros['cte_conf_notas_act'])
        ct = float(parametros['cte_conf_notas_tarea'])
        cc = float(parametros['cte_conf_notas_ctrl'])

        nota_esp = self.notas_esperadas[tipo].pop(0)
        if tipo == "Actividad":
            return ca*(nota - nota_esp)
        elif tipo == "Tarea":
            return ct*(nota - nota_esp)
        elif tipo == "Control":
            return cc*(nota - nota_esp)
        return 0

    # FINAL CONFIANZA C Y RECIBIR NOTA

    def rendir_evaluacion(self, tipo):
        '''
        dado un tipo de evaluacion, se procede a calcular el progreso de
        aquella evaluacion y su nota esperada

        param tipo: tipo entregado desde Simulacion.py frente a un evento de 
        actividad, control o entrega de tarea. | tipo: string

        return None
        return tipo: none
        '''

        S = self.dia_semana*self.S_sem/7

        if tipo == "Actividad":
            pep8 = 0.7*S+0.2*self.P+0.1*self.C
            func = 0.3*S+0.6*self.P+0.1*self.C
            content = 0.7*S+0.2*self.P+0.1*self.C

        elif tipo == "EntregaTarea":
            perso_pep8, perso_func, perso_content = perso_tareas(
                self.personalidad)

            # porque se publican los viernes y las horas semanales cambian
            H1 = self.Ht_dict[self.semana-2]*2/7
            H2 = self.Ht_dict[self.semana-1]
            H3 = 0.7*self.horas_disp*5/7
            Ht = H1+H2+H3

            pep8 = perso_pep8*(0.5*Ht+0.5*self.P)
            func = perso_func*(0.7*S+0.1*self.P+0.2*Ht)
            content = perso_content*(0.5*S+0.1*self.P+0.4*Ht)

        elif tipo == "Control":
            func = 0.3 * S+0.2*self.P+0.5*self.C
            content = 0.7 * S + 0.05*self.P+0.25*self.C

        elif tipo == "Examen":
            func = 0.3 * S+0.2*self.P+0.5*self.C
            content = 0.5 * S+0.1*self.P+0.4*self.C

        if tipo == "Actividad":
            self.progreso[tipo] = 0.4*(func + content) + 0.2*pep8
        elif tipo == 'EntregaTarea':
            self.progreso['Tarea'] = 0.4*(func + content) + 0.2*pep8
        else:
            self.progreso[tipo] = 0.3*func + 0.7*content

        if tipo != 'EntregaTarea':

            Hs = self.Hs_sem*self.dia_semana/7
            self.notas_esperadas.append(
                tipo, nota_gen(Hs, self.materia_actual))
        else:
            H1 = self.Hs_dict[self.semana-1]
            H2 = self.Hs_dict[self.semana-2]*2/7 + 0.3*self.horas_disp*5/7
            nota = (nota_gen(H2, self.materia_actual) +
                    nota_gen(H1, materias[self.semana-1]))/2

            self.notas_esperadas.append('Tarea', nota)


class Ayu_Tareas:
    '''
    Todo ayudante de tareas del curso sera representado mediante un objeto de
    esta clase
    '''

    exigencia = 0

    def __init__(self, nombre):
        '''
        param nombre: nombre del ayudante | tipo: string
        '''
        self.nombre = nombre

    def corregir(alumnos, coordinador):
        '''
        llamado desde Simulacion.py, recibe todos los alumnos y el coordinador,
        calcula la nota de cada alumno segun su progreso en la tarea y se las
        entrega al coordinador

        param alumnos: lista de los alumnos activos del curso 
        | tipo: list(Alumnos)

        param coordinador: objeto del coordinador | tipo: Coordinador

        return al entregarle las notas al coordinador, este retorna cuando
        dias se retrasa la entrega, y esta funcion vuleve a retornar este 
        retraso
        return tipo: int
        '''
        notas = {}

        for alumno in alumnos:
            #print('tareas', alumno.progreso['Tarea'], Ayu_Tareas.exigencia)
            notas[alumno.nombre] = min(max(
                (7 * alumno.progreso['Tarea']/Ayu_Tareas.exigencia),
                1), 7)

        retraso_publicacion = coordinador.recibir_notas('Tarea', notas)
        return retraso_publicacion


class Ayu_Docencia:
    '''
    Todo ayudante de docencia del curso sera representado mediante un objeto de
    esta clase
    '''

    exigencia = 0

    def __init__(self, nombre, dominios):
        '''
        param nombre: nombre del ayudante | tipo: string

        param dominios: lista de tres materias del curso en los cuales se 
        maneja el ayudante  | tipo: list()

        var ayudados: almacena por cada semana el numero de alumnos ayudados 
        en la actividad de la semana  | tipo: dict()
        '''
        self.nombre = nombre
        self.dominios = dominios
        self.ayudados = dict((i, 0) for i in range(20))

    def corregir(alumnos, tipo, coordinador, materia):
        '''
        llamado desde Simulacion.py, recibe todos los alumnos, coordinador,
        la materia y el tipo de evaluacion que se corregira, calcula la nota
        de cada alumno segun su progreso en la evaluacion y se las entrega al
        coordinador

        param alumnos: lista de los alumnos activos del curso 
        | tipo: list(Alumnos)

        param coordinador: objeto del coordinador | tipo: Coordinador
        param tipo: tipo de evaluacion | tipo: string
        param materia: materia de la evaluacion | tipo: string

        return al entregarle las notas al coordinador, este retorna cuando
        dias se retrasa la entrega, y esta funcion vuleve a retornar este 
        retraso
        return tipo: int
        '''
        notas = {}

        for alumno in alumnos:
            #print(tipo, alumno.progreso[tipo], Ayu_Docencia.exigencia)
            adicional = perso(alumno.personalidad, materia, tipo)
            notas[alumno.nombre] = min(max(
                (7 * alumno.progreso[tipo]/Ayu_Docencia.exigencia)+adicional,
                1), 7)

        retraso_publicacion = coordinador.recibir_notas(tipo, notas)
        return retraso_publicacion

    def ayudar(self, alumno, semana):
        '''
        agrega un bonus de manejo de contenidos al alumno y se suma uno (1) al
        nro de ayudados de esa semana

        param alumno: objeto de alumno que sera ayudado en la actividad 
        | tipo: Alumno

        param semana: semana actual | tipo: int

        return none
        return tipo: none
        '''
        alumno.S_bonus_dict[semana] += 0.01
        self.ayudados[semana] += 1


class Profesor:
    '''
    Todo profesor del curso sera representado mediante un objeto de
    esta clase
    '''

    def __init__(self, nombre, seccion, dia_consulta, imprimir):
        '''
        param nombre: nombre del profesor | tipo: str
        param seccion: seccion del profesor | tipo: str
        param dia_consulta: dia en que el profesor recibe consultas | tipo: int

        var nro_consultas: nro de consultas que recibe el profesor | tipo: int

        var alumnos_recibidos: guarda los alumnos que ha atentido semanalmente
        | tipo: MyDict

        var cola_semanal: guarda los alumnos que desean ser atendidos, pero no
        necesariemente todos seran atendidos | tipo: list()

        var semana: semana actual | tipo: int

        '''
        self.nombre = nombre
        self.seccion = seccion
        self.dia_consulta = dia_consulta
        self.nro_consultas = 10
        self.alumnos_recibidos = MyDict()
        self.cola_semanal = []
        self.semana = 0
        self.i = imprimir

    def agregar_cola(self, semana, alumno):
        '''
        dado un alumno que desea ser atendido, se revisa si ya fue antendido
        la semana anterior, si no fue atendido, entonces se agrega a la cola

        param semana: semana actual | tipo: int
        param alumno: alumno que desea ser atendido | tipo: Alumno

        return none
        return tipo: none
        '''
        if semana >= 1 and semana-1 in self.alumnos_recibidos:
            if alumno.nombre not in self.alumnos_recibidos[semana-1]:
                self.cola_semanal.append(alumno)
        else:
            self.cola_semanal.append(alumno)

    def atender(self, semana):
        '''
        selecciona de cola_semanal nro_consultas alumnos al azar y los
        atiende, llamando a la funcion reunion() del alumno. finalmente se 
        vacia la cola semanal.

        param semana: semana actual | tipo: int

        return none
        return tipo: none
        '''
        elejidos = sample(self.cola_semanal, min(
            len(self.cola_semanal), self.nro_consultas))
        for alumno in elejidos:
            self.alumnos_recibidos.append(semana, alumno.nombre)
            alumno.reunion()

        if len(elejidos) != 0 and self.i:
            print("Semana: {} | Día: {:^9} | {} atendío a {} alumnos"
                  .format(str(semana).zfill(2), dia_semana(self.dia_consulta),
                          self.nombre, len(elejidos)))

        self.cola_semanal = []

    def check_consulta(self, alumno, semana):
        '''
        revisa si el alumno que genero la consulta pertenece a la seccion del 
        profesor, si lo es, entonces llama a la funcion agregar_cola.

        param alumno: objeto de alumno que recibe | tipo: Alumno
        param semana: semana actual | tipo: int

        return none
        return tipo: none
        '''
        if alumno.solicitar_reunion and alumno.seccion == self.seccion:
            self.agregar_cola(self.semana, alumno)


class Coordinador:
    '''
    El coordinador del curso sera representado mediante un objeto de
    esta clase
    '''

    def __init__(self, nombre, prob_atraso):
        '''
        param nombre: nombre del coordinador | tipo: str
        param prob_atraso: prob de atrasar la entrega de notas | tipo: float
        var notas: almacena las ultimas notas de cada tipo de evaluacion
        | tipo: list

        var promedios: guarda los promedios  del curso de cada evaluacion
        | tipo: MyDict

        var aprob_reprob: guarda el numero de aprob y reprobados de cada 
        evaluacion | tipo: MyDict
        '''
        self.nombre = nombre
        self.notas = {}
        self.prob_atraso = prob_atraso
        self.promedios = MyDict()
        self.aprob_reprob = MyDict()

    def recibir_notas(self, tipo, notas):
        '''
        param tipo: tipo de notas | tipo: str
        param notas: notas que se reciben | tipo: dict

        recibe las notas entregadas por los ayudantes y las guarda en notas. 
        Ademas decide si va a retrasar la publicacion de notas.

        return el retraso aleatorio
        return tipo: int
        '''
        self.notas[tipo] = notas
        retraso = 0
        if random() <= self.prob_atraso:
            retraso = randint(2, 5)
        return retraso

    # falta hacer lo del descuento
    def publicar_notas(self, alumnos, tipo):
        '''
        entrega a los alumnos las notas de una evaluacion, ademas calcula el 
        promedio del curso,los reprobados y reprobados de la actividad y los 
        guarda los atributos del coordinador.

        param alumnos: Alumnos activos del curso | tipo: list(Alumno)
        param tipo: tipo de evaluacion de las notas | tipo: str

        return True si el tipo es examen, y retorna tambien el promedio, lo
         del examen se ocupa para saber cuando terminar la simulacion

        return tipo: tuple(bool,float)
        '''

        for alumno in alumnos:
            alumno.recibir_nota(self.notas[tipo][alumno.nombre], tipo)

        notas = [value for key, value in self.notas[tipo].items()]

        promedio = round(mean(notas), 1)
        self.promedios.append(tipo, promedio)

        largo = len(self.notas[tipo])

        porcent_a = round(100*len([i for key, i in self.notas[
            tipo].items() if i >= 3.95])/largo, 1)

        porcent_r = round(100-porcent_a, 1)
        texto = 'Aprobados: {}% | Reprobados: {}%'.format(porcent_a, porcent_r)
        self.aprob_reprob.append(tipo, texto)

        if tipo == "Examen":
            return True, promedio
        else:
            return False, promedio
