dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def biciesto(ano):
    return (ano % 100 != 0 or ano % 400 == 0) and ano % 4 == 0


def dias_ano(ano):
    if biciesto(ano):
        return 366
    return 365


def dias_en_mes(ano, mes):
    if biciesto(ano) and mes == 2:
        return 29
    return dias_por_mes[mes - 1]


def ingresar_fecha():
    todo = input('Ingrese una fecha de la forma AAAA-MM-DD HH:MM:SS\n')

    if revisar_fecha(todo):
        x = ingresar_fecha()
        return x
    else:
        return todo


def revisar_fecha(todo):
    invalido = False
    inputs = todo.split(' ')

    if len(inputs) == 1:
        print("Formato invalido")
        invalido = True
    else:
        lista_fecha = inputs[0].split("-")
        if len(lista_fecha) == 1:
            print("Formato invalido")
            invalido = True
        else:
            lista_hora = inputs[1].split(":")
            if len(lista_hora) == 1:
                print("Formato invalido")
                invalido = True
            else:
                fecha_lista = lista_fecha + lista_hora
                for j in fecha_lista:
                    if not j.isdigit():
                        print('Fecha invalida, solo se aceptan numeros')
                        invalido = True

                for j in fecha_lista[1:]:
                    if len(j) != 2:
                        print(
                            'Fecha invalida, MM,DD,HH,MM,SS son numeros de dos digitos')
                        invalido = True

                if len(fecha_lista) != 6:
                    print('Formato invalido')
                    invalido = True

                elif len(fecha_lista[0]) != 4:
                    print('Fecha invalida, AAAA es un numeros de 4 digitos')
                    invalido = True

                elif int(fecha_lista[0]) < 2000:
                    print('Fecha invalida, AAAA debe ser mayor o igual a 2000')
                    invalido = True

                elif int(fecha_lista[1]) > 12 or int(fecha_lista[1]) < 1:
                    print('Fecha invalida, MM (mes) es un numero entre 01 y 12')
                    invalido = True

                elif int(fecha_lista[2]) > dias_en_mes(int(fecha_lista[0]), int(fecha_lista[1])) or int(
                        fecha_lista[2]) < 1:
                    print('Fecha invalida, DD es un numero entre 01 y {}, para el mes {}'.format(
                        dias_en_mes(int(fecha_lista[0]), int(fecha_lista[1])), fecha_lista[1]))
                    invalido = True

                elif int(fecha_lista[3]) > 24 or int(fecha_lista[3]) < 0:
                    print('Fecha invalida, HH es un numero entre 00 y 24')
                    invalido = True

                elif int(fecha_lista[4]) > 60 or int(fecha_lista[4]) < 0:
                    print('Fecha invalida, MM (minutos) es un numero entre 00 y 60')
                    invalido = True

                elif int(fecha_lista[5]) > 60 or int(fecha_lista[5]) < 0:
                    print('Fecha invalida, SS es un numero entre 00 y 60')
                    invalido = True

    return invalido


def convertir_a_horas(fecha):  # se considera tiempo 0 el 2000-01-01
    total = 0
    if len(fecha) != len("2017-03-15 16:10:00"):
        ano, b, h = fecha.split(" ")
    else:
        ano, h = fecha.split(" ")

    f = ano.split("-") + h.split(":")

    f = [int(j) for j in f]
    anos = [j for j in range(2000, f[0])]
    meses = [j for j in range(1, f[1])]
    dias = [j for j in range(1, f[2])]
    for j in anos:
        total += dias_ano(j) * 24
    for j in meses:
        total += dias_en_mes(f[0], j) * 24
    for j in dias:
        total += 24

    return total + f[3] + f[4] / 60 + f[5] / 3600


def convertir_a_fecha(horas):
    segundos = int(horas * 3600)
    conteo = 0
    ano = 2000
    while conteo + dias_ano(ano) * 86400 < segundos:
        conteo += dias_ano(ano) * 86400
        ano += 1
    mes = 1
    while conteo + dias_en_mes(ano, mes) * 86400 < segundos:
        conteo += dias_en_mes(ano, mes) * 86400
        mes += 1

    dias = (segundos - conteo) // 86400
    conteo += dias * 86400
    horas = ((segundos - conteo) // 3600)
    conteo += horas * 3600
    minutos = ((segundos - conteo) // 60)
    conteo += minutos * 60
    segundos = (segundos - conteo)
    return "{}-{}-{} {}:{}:{}".format(str(ano).zfill(4), str(mes).zfill(2), str(dias + 1).zfill(2), str(horas).zfill(2), str(minutos).zfill(2), str(segundos).zfill(2))


# cual sera la fecha luego de "horas" desde "fecha_actual".
def calcular_prox_fecha(fecha_actual, horas):
    if not fecha_actual:
        return None
    return convertir_a_fecha(convertir_a_horas(fecha_actual) + horas)


def geq(fecha1, fecha2):  # True si fecha1 > fecha2
    return convertir_a_horas(fecha1) > convertir_a_horas(fecha2)


def between(x, fecha1, fecha2):
    return geq(x, fecha1) and geq(fecha2, x)


def diferencia_en_horas(fecha_inicio, fecha_final):
    return convertir_a_horas(fecha_final) - convertir_a_horas(fecha_inicio)


def filter_by_date(lista, fecha, reverse=False):

    return [x for x in lista if cronologico(x, fecha, reverse)]


def cronologico(diccionario, fecha_actual, reverse):
    if not reverse:
        if "fecha_inicio" in diccionario:
            if geq(diccionario["fecha_inicio"], fecha_actual):
                return False
    else:
        if "fecha_termino" in diccionario:
            # en este caso, fecha_Actual, sera la fecha de inicio del incendio
            if geq(fecha_actual, diccionario["fecha_termino"]):
                return False
    return True
