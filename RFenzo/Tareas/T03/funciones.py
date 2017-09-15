from collections import Iterable, OrderedDict
from operadores import igual, mayor, menor, menori, mayori, distinto
from operadores import mas, menos, por, div, aprox
from types import GeneratorType as generador
import itertools

modelos = ["normal", "gamma", "exponencial"]
signos = {"==": igual, ">": mayor, "<": menor, ">=": mayori,
          "<=": menori, "!=": distinto}
operandos = {"+": mas, "-": menos, "*": por, "/": div, ">=<": aprox}
commands = ["asignar", "crear_funcion",
            "graficar", "extraer_columna",
            "filtrar", "operar", "evaluar",
            "LEN", "PROM", "DESV", "MEDIAN",
            "VAR", "comparar_columna",
            "comparar", "do_if"]


def csv_reader(file):
    with open(file + '.csv', 'r') as f:
        x = f.readline().replace(' ', '').strip().split(';')

    header = OrderedDict((key, tipo)
                         for key, tipo in [j.split(':') for j in x])
    gen_lineas = (OrderedDict(zip(header.keys(), x.strip().split(";"))) for x
                  in open(file+'.csv', 'r'))
    next(gen_lineas)

    return header, gen_lineas


def return_type(dato):
    if callable(dato):
        return "Funcion"
    elif isinstance(dato, bool):
        return "bool"
    elif isinstance(dato, (int, float)):
        return "Numero"
    elif isinstance(dato, str):
        if dato in modelos:
            return "modelo"
        else:
            return "str"
    elif isinstance(dato, itertools._tee) or isinstance(dato, generador):
        return "Columna"
    elif isinstance(dato, Iterable):
        if len(dato) > 0:
            if dato[0] in commands:
                return "Consulta"


def handle_error(args, parametros):
    if parametros == ['modelo', 'nNumeros']:  # para crear funcion
        parametros = ['modelo']+['Numero']*(len(args)-1)
    elif parametros == ['Columna', 'str or Columna']:  # para graficar
        if return_type(args[1]) == 'str' or return_type(args[1]) == 'Columna':
            parametros[1] = return_type(args[1])
        else:
            raise Exception("Error de tipo")

    if len(parametros) != len(args):
        raise Exception("Argumento invalido")

    aux_param, aux_args = filter_anys(parametros, list(args))
    tipos_argumentos = [return_type(x) for x in aux_args]

    if aux_param != tipos_argumentos:
        dif_y_str = list(filter(lambda x: x[0] != x[1] and x[0] ==
                                "str", zip(tipos_argumentos, aux_param)))
        if len(dif_y_str) > 0:
            raise Exception("Referencia invalida")
        raise Exception("Error de tipo")


# ocupan copias de generador, no el original.


def replace_variables(args, variables):
    return [gen_tee(x, variables) for x in args]

# ocupan copias de generador, no el original.


def replace_stack(args, stack):
    return [gen_tee(x, stack) for x in args]

# genera la copia del generador


def gen_tee(x, varstack):
    if str(x) in varstack:
        if (isinstance(varstack[str(x)], generador) or
                isinstance(varstack[str(x)], itertools._tee)):
            varstack[str(x)], b = itertools.tee(varstack[str(x)])

            return b
        return varstack[str(x)]
    return x


def filter_anys(deseado, realidad):

    positions = [nro for nro, x in enumerate(deseado) if x == "any"]
    list(map(lambda x: deseado.pop(x), positions))
    list(map(lambda x: realidad.pop(x), positions))
    return deseado, realidad


def factorial(n):
    if n < 2:
        return 1
    return range_prod(1, n)


def range_prod(lo, hi):
    if lo+1 < hi:
        mid = (hi+lo)//2
        return range_prod(lo, mid) * range_prod(mid+1, hi)
    if lo == hi:
        return lo
    return lo*hi


def check_range(string):
    string = string.replace(' ', '')
    comas = string.count(',')
    doble_punto = string.count(':')
    dos = len(string.split(':'))
    tres = len(string.split(','))
    cinco = len(string.split(':')[0])
    rango = string.split(':')[0]
    x = string.find(':')+1
    y = string.find(',')
    a = string[x:y]
    string = string[y+1:]
    y = string.find(',')
    b = string[:y]
    c = string[y+1:]

    if (comas != 2 or doble_punto != 1 or dos != 2 or tres != 3
            or cinco != 5 or rango != "rango" or "." in a or "." in b):
        return False, None, None, None
    try:
        if ((int(a) >= int(b) and float(c) < 0) or
                (int(a) <= int(b) and float(c) > 0)):
            return True, int(a), int(b), float(c)
        else:
            return False, None, None, None
    except Exception:
        raise Exception("Imposible procesar")


def tipo_dato(dato, string_tipo):
    if string_tipo == "float":
        return float(dato)
    elif string_tipo == "int":
        return int(dato)


def comparacion(a, signo, b):
    return signos[signo](a, b)


def operacion(a, operador, b):
    return operandos[operador](a, b)


def rango_intervalo(a, b, c):
    if c == 0:
        raise Exception("Error matematico")
    if b < a:
        c = abs(c)
        return [b+c*i for i in range(0, int((a-b)/c)+1)][::-1]
    return [a+c*i for i in range(0, int((b-a)/c)+1)]
