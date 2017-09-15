from collections import OrderedDict
from Funciones import date


def file_len(fname):
    with open("Archivos/" + fname, encoding="utf-8") as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def header_to_dict(header):
    dict = OrderedDict()
    splitted = header.split(",")
    for j in splitted:
        key, b = j.replace("\n", "").split(":")
        if b == "string":
            tipo = str
        elif b == "float":
            tipo = float
        elif b == "int":
            tipo = int
        elif b == "list":
            tipo = list
        else:
            print("agregar elif para b")
        dict[key] = tipo
    return dict


def type_input(input):

    if "." in input:
        try:
            return float
        except ValueError:
            return str
    elif input.isdigit() and input != '':
        return int
    else:
        return str


def csv_to_dict(archivo):
    data = []  # sera una lista de diccionarios
    with open("Archivos/" + archivo, encoding='utf-8') as f:
        # obtener header
        header = f.readline().replace(':', ',').split(',')
        header_nombre = []
        header_tipo = []
        i = 2
        for j in header:
            if i % 2 == 0:
                header_nombre.append(j)
            else:
                header_tipo.append(j.replace("\n", ""))
            i += 1

        # rellenar data
        for line in f:
            x = line[:-1].split(',')
            linea = OrderedDict()
            i = 0

            for j in x:
                if header_tipo[i] == "float":
                    j = float(j)
                elif header_tipo[i] == "int":
                    j = int(j)
                linea[header_nombre[i]] = j
                i += 1

            data.append(linea)

    return data


def input_to_csv(archivo):
    with open("Archivos/" + archivo, "r", encoding="utf8") as f:
        header = f.readline()
    with open("Archivos/" + archivo, "a", encoding="utf8") as f:

        reiniciar = False
        inputs = OrderedDict()
        linea = ""
        id = str(file_len(archivo) - 1)
        print("Ingrese los siguientes datos: \n")

        header_dict = header_to_dict(header)
        for j in header_dict:  # j son las keys

            if j == "id":
                linea += id + ","
                continue

            print("{}({}):".format(j, (header_dict[j])))
            input_usuario = input()
            if "fecha" in j:
                while date.revisar_fecha(input_usuario):
                    print("{}({}):".format(j, (header_dict[j])))
                    input_usuario = input()

            linea += input_usuario + ","
            if type_input(input_usuario) == header_dict[j] and j != "recurso_id":
                inputs[j] = input_usuario

            elif j == "recurso_id":
                if input_usuario != "":
                    try:
                        int(input_usuario)
                    except ValueError:
                        print(
                            "El tipo de datos ingresados no coincide con el requerido")
                        reiniciar = True
                        break
                    if int(input_usuario) > 199 or int(input_usuario) < 0:
                        print("El recurso seleccionado no existe\n")
                        reiniciar = True
                        break
                inputs[j] = input_usuario
            else:
                print("El tipo de datos ingresados no coincide con el requerido")
                reiniciar = True
                break

        if not reiniciar:
            f.write(linea[:-1] + "\n")
        else:
            input_to_csv(archivo)


def print_csv(archivo, fecha):
    dict_archivo = date.filter_by_date(csv_to_dict(archivo), fecha)

    print("//////////////////////////////      " +
          archivo + "      //////////////////////////////\n")
    x = ''

    if len(dict_archivo) == 0:
        print('Para la fecha, no existen datos en {}'.format(archivo))
        return '\n'

    for j in dict_archivo[0].keys():
        x += j + ', '
    print('[' + x[:-2] + ']')

    for j in dict_archivo:
        x = ""
        for p in j.items():
            x += str(p[1]) + ', '
        print('[' + x[:-2] + ']')
    return '\n'
