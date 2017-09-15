import csv

from Clases.Pais import Pais

from Clases.Infeccion import Infeccion
from EstructurasDeDatos.DiccionarioOrdenado import DiccionarioOrdenado
from EstructurasDeDatos.MiLista import MiLista


def airports_to_dict():
    with open("Archivos/random_airports.csv") as f:
        x = csv.reader(f,delimiter = ",")
        total = DiccionarioOrdenado()
        for line in x:
            linea = MiLista(*line)
            total.append(linea[0],linea[1])
        total.pop()

        f.close()
    return total


def borders_to_dict():
    with open("Archivos/borders.csv") as f:
        x = csv.reader(f,delimiter = ";")
        total = DiccionarioOrdenado()
        for line in x:
            linea = MiLista(*line)
            total.append(linea[0],linea[1])
        total.pop()
        for key,pais2 in total:
            if type(pais2) != MiLista:
                total[key] = MiLista(pais2)
    return total

def csv_to_dict_of_dicts(archivo):
    with open("Archivos/"+ archivo) as f:
        x = csv.reader(f,delimiter = ",")
        total = DiccionarioOrdenado()
        header= None
        for line in x:
            if not header:
                header = MiLista(*line)
                header.pop()
            else:
                linea = MiLista(*line)
                pais = linea.pop()
                info = DiccionarioOrdenado()
                i=0
                for j in header:
                    info.append(j,linea[i])
                    i+=1
                total.append(pais,info)
        return total

def mundo_to_csv(diccionario_mundo,dia_descubrimiento_infeccion,dia_descubrimiento_cura,progreso_al_dia,poseedores_de_cura,cola_propuestas):
    f = open("Archivos/" + "load.csv","w")
    f.write("{};{};{};{};{}\n".format(dia_descubrimiento_infeccion,dia_descubrimiento_cura,progreso_al_dia,poseedores_de_cura,cola_propuestas))
    for _,cp in diccionario_mundo:
        if cp.infeccion:
            x= cp.infeccion.tipo
        else:
            x=None
        f.write("{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13}\n".format(
            cp.nombre,cp.habitantes,cp.frontera,cp.aeropuerto,cp.infectados,x,cp.muertos,cp.estado_aeropuerto,
            cp.estado_frontera,cp.mascarilla,cp.dia_actual,cp.cura,cp.dia_extincion,cp.dia_inicio_infeccion,
            ))
    f.close()

def load_to_mundo():
    with open("Archivos/load.csv","r") as f:
        x = csv.reader(f, delimiter=";")
        mundo = DiccionarioOrdenado()
        firstline = False
        for line in x:
            linea = MiLista(*line)
            if not firstline:
                firstline= True
                if linea[0] == "None":
                    dia_descubrimiento_infeccion = None
                else:
                    dia_descubrimiento_infeccion = int(linea[0])
                if linea[1] == "None":
                    dia_descubrimiento_cura = None
                else:
                    dia_descubrimiento_cura = int(linea[1])
                progreso_al_dia = int(linea[2])
                poseedores_de_cura = MiLista()
                if len(linea[3]) != 2:
                    x = linea[3][1:-1].replace(" ", "").split(",")
                    poseedores_de_cura = MiLista(*x)
                cola_propuestas = DiccionarioOrdenado()
                if len(linea[4]) != 2:
                    x = linea[4][1:-1].replace(" ", "").split(",")
                    for key,valor in x.split(":"):
                        cola_propuestas[key] = valor
                continue
            nombre, habitantes, infectados, infeccion, muertos, estado_aeropuerto,estado_frontera, mascarilla, dia_actual, cura= linea[0],int(linea[1]),int(linea[4]),(linea[5]),int(linea[6]),bool(linea[7]),bool(linea[8]),bool(linea[9]),int(linea[10]),bool(linea[11])
            frontera = MiLista()
            if len(linea[2]) != 2:
                x = linea[2][1:-1].replace(" ","").split(",")
                frontera = MiLista(*x)
            aeropuerto = MiLista()
            if len(linea[3]) != 2:
                x = linea[3][1:-1].replace(" ","").split(",")
                aeropuerto = MiLista(*x)
            if linea[12] == "None":
                dia_extincion = None
            else:
                dia_extincion = int(linea[12])
            if linea[13] == "None":
                dia_inicio_infeccion = None
            else:
                dia_inicio_infeccion = int(linea[13])

            if infeccion != "None" or infeccion:
                infeccion = Infeccion(infeccion)
            else:
                infeccion = None

            pais = Pais(nombre,habitantes,frontera,aeropuerto,infectados,infeccion,muertos,estado_aeropuerto,estado_frontera,mascarilla,dia_actual,cura,dia_extincion,dia_inicio_infeccion)


            mundo.append(nombre, pais)

        return mundo,dia_descubrimiento_infeccion,dia_descubrimiento_cura,progreso_al_dia,poseedores_de_cura,cola_propuestas

