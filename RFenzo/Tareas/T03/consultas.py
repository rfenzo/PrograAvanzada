from collections import Iterable, OrderedDict
from funciones import handle_error, factorial, return_type, signos
from funciones import check_range, tipo_dato, comparacion, operacion
from funciones import operandos, rango_intervalo, replace_variables
from funciones import replace_stack, csv_reader
from functools import reduce
from datetime import datetime as dt
from matplotlib import pyplot as plt
import itertools
import math
import csv
import numpy as np
from datetime import datetime as dt

stack_anidados = OrderedDict()
variables = {}


def normal(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Numero", "Numero"])
    if args[1] < 0:
        raise Exception("Imposible procesar")
    def funcion(x):
        constante = (1/(2*math.pi*(args[1]**2)))**0.5
        elevado = -0.5*((x-args[0])/args[1])**2
        return constante*math.exp(elevado)
    return funcion


def gamma(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Numero", "Numero"])
    def funcion(x):
        if x < 0:
            raise Exception("Imposible procesar")
        constante = (args[0]**args[1])/factorial(args[1]-1)
        equiz = x**(args[1]-1)
        exp = math.exp(-args[0]*x)
        return constante*equiz*exp
    return funcion


def exponencial(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Numero"])
    if args[0] <= 0:
        raise Exception("Imposible procesar")
    def funcion(x):
        if x < 0:
            raise Exception("Imposible procesar")
        return args[0]*math.exp(-args[0]*x)
    return funcion


def asignar(*args):
    args = replace_stack(args, stack_anidados)
    handle_error(args, ["str", "any"])
    if args[0] not in dict_commands and args[0] not in modelos:
        variables[args[0]] = args[1]
    else:
        raise Exception("Imposible procesar")
    return None


def crear_funcion(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ['modelo', 'nNumeros'],)
    if args[0] not in modelos:
        raise Exception("Imposible procesar")
    return modelos[args[0]](*args[1:])


def graficar(*args):
    titulo = args
    args = list(args)
    mostrar = args.pop(0)
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ['Columna', 'str or Columna'])
    args[0] = list(args[0])
    length = len(args[0])
    if isinstance(args[1], str):
        boolean, a, b, c = check_range(args[1])
        if boolean:
            x = rango_intervalo(a, b, c)
            if len(x) < length:
                raise Exception("Imposible procesar")
            else:
                x = x[:length]
        elif args[1] == "numerico":
            x = [x for x in range(0, length)]
        elif args[1] == "normalizado":
            norma = reduce(lambda x, y: x+y, args[0])**(-1)
            x = [x*norma for x in range(length)]
        else:
            raise Exception("Imposible procesar")

    elif len(args[1]) == length:
        x = args[1]
    else:
        raise Exception("Imposible procesar")

    if mostrar:
        plt.plot(x, args[0])
        plt.title(str(titulo[1])+' '+str(titulo[2]))
        plt.show()

    return None


def extraer_columna(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["str", "str"])
    header, gen_lineas = csv_reader(args[0])
    return (tipo_dato(dato[args[1]], header[args[1]]) for dato in gen_lineas)


def filtrar(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna", "str", "Numero"])
    if args[1] not in signos:
        raise Exception("Imposible procesar")
    return (x for x in args[0] if comparacion(x, args[1], args[2]))


def operar(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna", "str", "Numero"])
    if (args[1] == ">=<" and args[2] < 0) or args[1] not in operandos:
        raise Exception("Imposible procesar")
    elif args[1] == "/" and args[2] == 0:
        raise Exception("Error matematico")
    return (operacion(x, args[1], args[2]) for x in args[0])


def evaluar(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Funcion", "Numero", "Numero", "Numero"])
    return (args[0](x) for x in rango_intervalo(args[1], args[2], args[3]))


def LEN(*args):
    agrs = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna"])
    return sum(1 for i in args[0])


def PROM(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna"])
    args[0], b = itertools.tee(args[0])
    length = LEN(b)
    if length == 0:
        raise Exception("Error matematico")
    return reduce(lambda x, y: x+y, args[0])/length


def DESV(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna"])
    args[0], b, c = itertools.tee(args[0], 3)
    n1 = LEN(args[0])-1
    if n1 == 0:
        raise Exception("Error matematico")
    promedio = PROM(b)
    suma_individual = map(lambda x: (x-promedio)**2, c)
    suma = reduce(lambda x, y: x+y, suma_individual)
    return (suma/n1)**0.5


def MEDIAN(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna"])
    lista = [i for i in args[0]]
    length = len(lista)
    if not length % 2:
        gen = (lista[x] for x in [int((length/2)-1), int((length/2))])
        return PROM(gen)
    else:
        return lista[int((length//2))]


def VAR(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna"])
    return DESV(args[0])**2


def comparar_columna(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Columna", "str", "str", "Columna"])
    if args[2] not in comandos_comparar:
        raise Exception("Imposible procesar")
    n1 = comandos_comparar[args[2]](args[0])
    n2 = comandos_comparar[args[2]](args[3])

    return comparacion(n1, args[1], n2)


def comparar(*args):
    args = replace_stack(args, stack_anidados)
    args = replace_variables(args, variables)
    handle_error(args, ["Numero", "str", "Numero"])
    if args[1] not in signos:
        raise Exception("Imposible procesar")
    return comparacion(args[0], args[1], args[2])


def do_if(*args):
    dict_commands2 = {"asignar": asignar, "crear_funcion": crear_funcion,
                      "graficar": graficar, "extraer_columna": extraer_columna,
                      "filtrar": filtrar, "operar": operar, "evaluar": evaluar,
                      "LEN": LEN, "PROM": PROM, "DESV": DESV, "MEDIAN": MEDIAN,
                      "VAR": VAR, "comparar_columna": comparar_columna,
                      "comparar": comparar}
    args = list(args)
    args[1] = replace_stack([args[1]], stack_anidados)[0]
    args = replace_variables(args, variables)
    handle_error(args, ["Consulta", "bool", "Consulta"])

    def ejec(consulta, graficar=True):
        if "graficar" in consulta:
            if graficar:
                resultado = dict_commands2[consulta[0]](True, *consulta[1:])
            else:
                resultado = dict_commands2[
                    consulta[0]](False, *consulta[1:])
        else:
            resultado = dict_commands2[consulta[0]](*consulta[1:])
            stack_anidados[str(consulta)] = resultado

        return consulta[0] if resultado == None else resultado

    return ejec(args[0]) if args[1] else ejec(args[2])


dict_commands = {"asignar": asignar, "crear_funcion": crear_funcion,
                 "graficar": graficar, "extraer_columna": extraer_columna,
                 "filtrar": filtrar, "operar": operar, "evaluar": evaluar,
                 "LEN": LEN, "PROM": PROM, "DESV": DESV, "MEDIAN": MEDIAN,
                 "VAR": VAR, "comparar_columna": comparar_columna,
                 "comparar": comparar, "do_if": do_if}

modelos = {"normal": normal, "gamma": gamma, "exponencial": exponencial}
comandos_comparar = {"LEN": LEN, "PROM": PROM, "DESV": DESV, "MEDIAN": MEDIAN,
                     "VAR": VAR}


def comandos_anidados(consulta, anidados):
    # es solo una consulta, y por tanto consulta es una anidados
    if anidados == []:
        anidados.append(consulta)
    listas = list(filter(lambda x: isinstance(x, list), consulta))
    comandos = list(filter(lambda x: x[0] in dict_commands, listas))
    if len(comandos) != 0:
        anidados.extend([i for i in comandos])
        [comandos_anidados(x, anidados) for x in comandos]
    return anidados


def get_anidados(consulta):
    return comandos_anidados(consulta, [])[::-1]


def ej_no_anidado(graficar, consulta):
    try:
        if "graficar" in consulta:
            if graficar:
                resultado = dict_commands[consulta[0]](True, *consulta[1:])
            else:
                resultado = dict_commands[consulta[0]](False, *consulta[1:])
        else:
            resultado = dict_commands[consulta[0]](*consulta[1:])
            stack_anidados[str(consulta)] = resultado

        return consulta[0] if resultado == None else resultado
    except Exception as Error:
        return 'Error de consulta: ' + str(consulta)+'\nCausa: '+str(Error)


def ej_anidado(graficar, comando):
    antes = dt.now()
    resultados = [ej_no_anidado(graficar, x) for x in get_anidados(comando)]
    if any([isinstance(n, str) for n in resultados]):
        error = list(filter(lambda x: isinstance(x, str), resultados))[0]
        return error, (dt.now()-antes).total_seconds()
    return resultados[-1], (dt.now()-antes).total_seconds()


def ejecutar(graficar, lista_comandos):
    resultytiempo = [ej_anidado(graficar, x) for x in lista_comandos]
    results = [x[0] for x in resultytiempo]
    tiempos = [x[1] for x in resultytiempo]
    return list(zip(lista_comandos, results, tiempos))
