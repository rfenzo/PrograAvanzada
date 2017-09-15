import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Clases.MyDict import MyDict

'''
Otros archivos que contienen clases, o incluso la misma simulacion, ocupara estos datos entregados por enunciado, los cuales son leidos desde parametros.csv y almacenados aqui, en datos.py.
'''


def get_defaults():
    '''
    permite leer el archivo defaults.csv para obtener en un diccionario
    los parametros por default de la simulacion

    return diccionario con parametros default
    return tipo: dict
    '''
    parametros = {}
    with open('Datos/defaults.csv', 'r', encoding=('utf-8')) as f:
        for line in f:
            parametro, valor = line.strip().split(',')
            parametros[parametro] = valor

    return parametros

defaults = get_defaults()


def parametrizador():
    '''
    permite leer el archivo parametros.csv y entregarlo como un diccionario

    return diccionario con los parametros y sus valores
    return tipo: dict
    '''
    parametros = {}
    with open('Datos/parametros.csv', 'r', encoding=('utf-8')) as f:
        for line in f:
            parametro, valor = line.strip().split(',')
            if valor == '-':
                valor = defaults[parametro]
            parametros[parametro] = valor
    return parametros

parametros = parametrizador()

materias = MyDict()
materias[0] = "OOP"
materias[1] = "Herencia"
materias[2] = "EDD"
materias[3] = "Arbol"
materias[4] = "Funcional"
materias[5] = "Metaclases"
materias[6] = "Simulacion"
materias[7] = "Threading"
materias[8] = "Int.Graf"
materias[9] = "Bytes"
materias[10] = "Networking"
materias[11] = "Webservices"

dif = MyDict()
dif["OOP"] = int(parametros['dif_OOP'])
dif["Herencia"] = int(parametros['dif_Herencia'])
dif["EDD"] = int(parametros['dif_EDD'])
dif["Arbol"] = int(parametros['dif_Arbol'])
dif["Funcional"] = int(parametros['dif_Funcional'])
dif["Metaclases"] = int(parametros['dif_Metaclases'])
dif["Simulacion"] = int(parametros['dif_Simulacion'])
dif["Threading"] = int(parametros['dif_Threading'])
dif["Int.Graf"] = int(parametros['dif_IntGraf'])
dif["Bytes"] = int(parametros['dif_Bytes'])
dif["Networking"] = int(parametros['dif_Networking'])
dif["Webservices"] = int(parametros['dif_Webservices'])

ponderacion = MyDict()
ponderacion["Actividad"] = 0.25
ponderacion["Tarea"] = 0.4
ponderacion["Control"] = 0.2
ponderacion["Examen"] = 0.15
