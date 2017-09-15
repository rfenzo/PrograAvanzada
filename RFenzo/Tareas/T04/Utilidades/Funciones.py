import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from random import randint, shuffle, choice
from numpy.random import triangular
from numpy import mean
from Clases.MyDict import MyDict


def dia_semana(dia):
    '''
    dado un numero, se retorna el string correspondiente a ese dia

    param dia: dia a convertir| tipo: int

    return dia de la semana
    return tipo: string
    '''
    x = {1: "lunes", 2: "martes", 3: "miercoles", 4: "jueves",
         5: "viernes", 6: "sabado", 7: "domingo"}
    return x[dia]


def sort_dict_key(x):
    '''
    recibe un diccionario y retorna otro ordenado segun sus keys

    param x: diccionario a ser ordenado | tipo: dict

    return Diccionario ordenado por keys
    return tipo: MyDict
    '''
    return MyDict(sorted(x.items(), key=lambda x: x[0]))


def prom(dict):
    '''
    dado un diccionario, retorna el promedio de sus valores

    param dict: diccionario del cual se obtendra el promedio

    return el promedio
    return tipo: float
    '''
    return round(mean([i for k, i in dict.items()]), 2)


def check_event(evento, eventos):
    '''
    dado un evento y el diccionario de eventos actuales, se revisa si ya existe un evento del mismo tipo

    param evento: nombre del evento a revisar| tipo: str
    param eventos: diccionario con los eventos generados pero no ejecutados
    | tipo: MyDict

    return True si no esta
    return tipo: bool

    '''
    for _, value in eventos.items():
        for x in value:
            if evento in x:
                return False
    return True


def perso(perso, materia, tipo):
    '''
    dada una personalidad, materia y tipo de evaluacion, se decide si se
    recibira un bono en la nota final de la evaluacion

    param perso: personalidad de un alumno | tipo: str
    param materia: materia a ser evaluada | tipo: str
    param tipo: tipo de evaluacion a ser evaluada | tipo: str

    return 1 si se dara el bono de 1 punto, 0 en otro caso
    return tipo: int
    '''
    if tipo == "Actividad":
        if perso == 'Eficiente' and materia in ["Funcional", "Threading"]:
            return 1
        elif perso == 'Artistico' and materia in ["Int.Graf", "Webservices"]:
            return 1
        elif perso == 'Teorico' and materia == "Metaclases":
            return 1
    elif tipo == "Examen":
        return 1
    return 0


def perso_tareas(perso):
    '''
    dada una personalidad, se decide si se
    recibira un bono en los progresos de la evaluacion

    param perso: personalidad de un alumno | tipo: str

    return los multiplicandos par apep8,func, y content
    return tipo: float,float,float
    '''
    pep8, fuc, content = 1, 1, 1

    if perso == 'Eficiente':
        pep8 *= 1.1
        fuc *= 1.1
        content *= 1.1
    elif perso == 'Artistico':
        pep8 *= 1.2
    elif perso == 'Teorico':
        pep8 *= 0.9
        fuc *= 0.9
        content *= 0.9

    return pep8, fuc, content


def responder_dudas(ayudantes, alumnos, semana):
    '''
    esta funcion simula la interaccion entre ayudantes y alumnos durante una
    actividad, donde los ayudantes responden las dudas, ejecutando el metodo
    ayudar de cada ayudante

    param ayudantes: lista con los ayudantes | tipo: list(Ayu_Docencia)
    param alumnos: lista de los alumnos activos | tipo: list(Alumno)
    param semana: semana actual | tipo: int

    return none
    return tipo: none
    '''
    ayu1, ayu2, ayu3 = ayudantes
    cola_dudas = []
    for alumno in alumnos:
        for i in range(int(triangular(1, 3, 10))):
            cola_dudas.append(alumno)

    shuffle(cola_dudas)
    breaker = False
    for alumno in cola_dudas:
        ayu = choice([ayu1, ayu2, ayu3])
        i = 1
        while ayu.ayudados[semana] >= 200:
            ayu = choice(ayu1, ayu2, ayu3)
            i += 1
            if i == 4:
                breaker = True
                break

        if breaker:
            break

        ayu.ayudar(alumno, semana)
