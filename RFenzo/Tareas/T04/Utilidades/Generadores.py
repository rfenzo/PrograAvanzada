import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


from random import random, choice, randint, sample, uniform
import csv
from Datos.datos import dif, parametros
from Clases.MyDict import MyDict


def credit_gen(prob_40, prob_50, prob_55, prob_60):
    '''
    Dadas las probabilidades de tener X creditos, entrega el nro de creditos

    param prob_40: probabilidad de tener 40 creditos | tipo: float
    param prob_50: probabilidad de tener 50 creditos | tipo: float
    param prob_55: probabilidad de tener 55 creditos | tipo: float
    param prob_60: probabilidad de tener 60 creditos | tipo: float

    return nro de creditos
    return tipo: int
    '''
    prob = random()
    if prob <= prob_40:
        return 40
    elif prob > prob_40 and prob <= prob_50+prob_40:
        return 50
    elif prob > prob_50+prob_40 and prob <= prob_55+prob_40+prob_50:
        return 55
    else:
        return 60


def hour_gen(creditos):
    '''
    Dado un numero de creditos, entrega el numero de horas disponibles
     semanales

    param creditos: nro de creditos del alumno | tipo: int

    return nro de horas disponibles (aleatoria)
    return tipo: int
    '''

    sup_40 = int(parametros['lim_sup_random_hour_40'])
    inf_40 = int(parametros['lim_inf_random_hour_40'])
    sup_50 = int(parametros['lim_sup_random_hour_50'])
    inf_50 = int(parametros['lim_inf_random_hour_50'])
    sup_55 = int(parametros['lim_sup_random_hour_55'])
    inf_55 = int(parametros['lim_inf_random_hour_55'])
    sup_60 = int(parametros['lim_sup_random_hour_60'])
    inf_60 = int(parametros['lim_inf_random_hour_60'])

    if creditos == 40:
        return randint(inf_40, sup_40)
    elif creditos == 50:
        return randint(inf_50, sup_50)
    elif creditos == 55:
        return randint(inf_55, sup_55)
    else:
        return randint(inf_60, sup_60)


def controls_gen():
    '''
    Retorna un generador que entrega semanas en las cuales se produce un 
    control, respentando de que no pueden haber mas de dos seguidos.

    return generador de semanas de controles
    return tipo: generator
    '''
    semanas = []
    while len(semanas) < 5:
        i = choice(range(0, 12))
        if i not in semanas:
            if i+1 and i-1 not in semanas or i-1 and i-2 not in semanas \
                    and i+1 and i+2 not in semanas:
                semanas.append(i)

    return (i for i in sorted(semanas))


def semanal_gen(dia):
    '''
    Retorna un generador que entrega dias de cada semana en que se genera un 
    evento. Ej: si dia es 5 (viernes), entonces el generador retorna 5(
    viernes),12 (viernes), 19 (viernes), ...

    param dia: dia en que se genera el evento | tipo: int

    return generador de semanas de controles
    return tipo: generator
    '''
    return (7*i+dia for i in range(0, 12))


def half_month_gen(dia):
    '''
    Retorna un generador que entrega dias de cada dos semanas en que se genera 
    un evento. Ej: si dia es 5 (viernes), entonces el generador retorna 5(
    viernes),19 (viernes), 33 (viernes), ...

    param dia: dia en que se genera el evento | tipo: int

    return generador de semanas de evaluacion
    return generator
    '''
    return (14*i+dia for i in range(0, 6))


def person_gen(prob_atraso_notas, prob_40, prob_50, prob_55, prob_60,
               conf_inf, conf_sup, Alumno, Ayu_Tareas, Ayu_Docencia, Profesor,
               Coordinador, prob_visitar_profesor, imprimir):
    '''
    Dado ciertos parametros y probabilidades, genera Alumnos,Ayudantes de 
    tarea o docencia, profesores y un coordinador a medida que va leyendo el
    archivo 'integrantes.csv'

    param prob_atraso_notas: probabilidad de que el coordinador atrase las
    notas | tipo: float

    param prob_40: probabilidad de tener 40 creditos | tipo: float
    param prob_50: probabilidad de tener 50 creditos | tipo: float
    param prob_55: probabilidad de tener 55 creditos | tipo: float
    param prob_60: probabilidad de tener 60 creditos | tipo: float
    param conf_inf: rango inferior para generar la confianza | tipo: int
    param conf_sup: rango superior para generar la confianza | tipo: int
    param Alumno: clase Alumno | tipo: Alumno
    param Ayu_Tareas: clase Ayu_Tareas | tipo: Ayu_Tareas
    param Ayu_Docencia: clase Ayu_Docencia | tipo: Ayu_Docencia
    param Profesor: clase Profesor | tipo: Profesor
    param Coordinador: clase Coordinador | tipo: Cordinador

    return cuatro (4) listas y un objeto de coordinador. Las lista son de
    alumnos, profesores, ayudantes de docencia,ayudantes de tareas.
    return tipo: list(Alumno),list(Profesor),list(Ayu_Tarea),list(Ayu_Docencia)
    ,Coordinador
    '''

    with open('integrantes.csv', 'r', encoding='utf-8') as f:
        alumnos, profesores, docencia, tareas = [], [], [], []

        for line in csv.reader(f, delimiter=','):
            nombre, tipo, seccion = line[0], line[1], line[2]

            if tipo == "Alumno":
                creditos = credit_gen(prob_40, prob_50,
                                      prob_55, prob_60)

                alumnos.append(Alumno(
                    nombre, seccion, uniform(conf_inf, conf_sup),
                    prob_visitar_profesor,
                    creditos, imprimir))

            elif tipo == "Profesor":
                dia_consulta = randint(1, 5)
                profesores.append(Profesor(nombre, seccion, dia_consulta,
                                           imprimir))

            elif tipo == "Docencia":
                docencia.append(Ayu_Docencia(nombre, sample(list(dif), 3)))

            elif tipo == 'Tareas':
                tareas.append(Ayu_Tareas(nombre))
            else:
                coordinador = Coordinador(nombre, prob_atraso_notas)

    return alumnos, profesores, docencia, tareas, coordinador


def escenarios_gen():
    '''
    Mediante la lectura de 'escenarios.csv', genera un diccionario de diccionarios con los parametros contenidos en el archivo. El diccionario que retorna se ve de la siguiente forma:

    parametros = {1:{prob_40_creditos: 0.6313654496143601, prob_50_creditos : 0.24664511039389303, etc..}, 2:{...}, 3: {...}}

    donde 1: {algo} es lo relacionado a la primera simulacion.
    '''
    with open('escenarios.csv', 'r', encoding='utf-8') as f:
        header = False
        headers = {}
        parametros = {}
        for line in csv.reader(f, delimiter=','):
            if not header:
                header = True
                for h in line:
                    nombre, tipo = h.split(":")
                    headers[nombre] = tipo
            else:
                x = [float(i) for i in line[1:]]
                parametros[line[0]] = x

        x = MyDict()

        for var, numeros in parametros.items():
            i = 0
            for nro in numeros:
                x.append(i, (var, nro))
                i += 1

        escenarios = {}
        for nro, variables in x.items():
            escenarios[nro] = {}
            for nombre, numero in variables:
                escenarios[nro][nombre] = numero

        return escenarios


def nota_gen(horas, materia):
    '''
    Dado un numero de horas estudiadas (Hs) y un tipo de materia, se genera una nota esperada por el alumno, estos datos son sacados de datos.py, que a su vez los saca de parametros.csv.

    param horas: horas de estudio | tipo: float
    param materia: materia a evaluar | tipo: string

    return un numero perteneciente a una distribucion uniforme
    return tipo: float
    '''
    if materia == "OOP":
        if horas < 2:
            return uniform(1.1, 3.9)
        elif horas < 4:
            return uniform(4.0, 5.9)
        elif horas < 6:
            return uniform(6.0, 6.9)
    elif materia == "Herencia":
        if horas < 3:
            return uniform(1.1, 3.9)
        elif horas < 6:
            return uniform(4.0, 5.9)
        elif horas < 7:
            return uniform(6.0, 6.9)
    elif materia == "EDD":
        if horas < 1:
            return uniform(1.1, 3.9)
        elif horas < 4:
            return uniform(4.0, 5.9)
        elif horas < 6:
            return uniform(6.0, 6.9)
    elif materia == "Arbol":
        if horas < 2:
            return uniform(1.1, 3.9)
        elif horas < 5:
            return uniform(4.0, 5.9)
        elif horas < 7:
            return uniform(6.0, 6.9)
    elif materia == "Funcional":
        if horas < 3:
            return uniform(1.1, 3.9)
        elif horas < 7:
            return uniform(4.0, 5.9)
        elif horas < 8:
            return uniform(6.0, 6.9)
    elif materia == "Metaclases":
        if horas < 4:
            return uniform(1.1, 3.9)
        elif horas < 7:
            return uniform(4.0, 5.9)
        elif horas < 9:
            return uniform(6.0, 6.9)
    elif materia == "Simulacion":
        if horas < 3:
            return uniform(1.1, 3.9)
        elif horas < 6:
            return uniform(4.0, 5.9)
        elif horas < 8:
            return uniform(6.0, 6.9)
    elif materia == "Threading":
        if horas < 2:
            return uniform(1.1, 3.9)
        elif horas < 5:
            return uniform(4.0, 5.9)
        elif horas < 7:
            return uniform(6.0, 6.9)
    elif materia == "Int.Graf":
        if horas < 1:
            return uniform(1.1, 3.9)
        elif horas < 4:
            return uniform(4.0, 5.9)
        elif horas < 6:
            return uniform(6.0, 6.9)
    elif materia == "Bytes":
        if horas < 4:
            return uniform(1.1, 3.9)
        elif horas < 7:
            return uniform(4.0, 5.9)
        elif horas < 9:
            return uniform(6.0, 6.9)
    elif materia == "Networking":
        if horas < 2:
            return uniform(1.1, 3.9)
        elif horas < 5:
            return uniform(4.0, 5.9)
        elif horas < 7:
            return uniform(6.0, 6.9)
    elif materia == "Webservices":
        if horas < 2:
            return uniform(1.1, 3.9)
        elif horas < 7:
            return uniform(4.0, 5.9)
        elif horas < 8:
            return uniform(6.0, 6.9)

    return 7
