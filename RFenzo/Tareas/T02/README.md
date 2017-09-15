Primero que todo, realizé los siguientes cambios en las formulas del enunciado debido a problemas de propagación de la enfermedad a otros paises, los cuales impiden el correcto funcionamiento del programa:

- prob descubrimiento de la infeccion = max(0.005,(infeccion.visibilidad * infectados *(muertos**2))/((poblacion_mundial_inicial)**3))
- prob_contagio = 0.2

A pesar de lo anterior, el modelo sigue teniendo baja probabilidad de contagiar via aerea a otros paises, pues cierra los aeropuertos antes este suceso, es por ésto que la infeccion se propaga más que nada por las fronteras, llegando acontagiar poca cantidad de personas, por lo que con la formula original de descubrimiento de la cura ésta probabilidad era infinitamente chica para la mayoria de mis pruebas. 
Por motivos de tiempo, no pude seguir probando distintas probabilidades para que el programa se desenvolviera como se deseaba.

Estructuras de datos:
 - MiLista(): **NO** es una lista ligada, va guardando los datos en atributos que tienen como nombre un numero, esto permite acceder a ellos tal como una lista mediante el __getitem__. Tambien tiene los metodos __iter__,__add__,__len__,__setitem__ y __repr__, además de algunas funciones útiles como pop,remove,sort,insert y append, que funcionan de manera parecida a las de una lista convencional. Fué utilizada en practicamente todo, tal como lo haría con una lista.
 - DiccionarioOrdenado(): Es básicamente un OrderedDict(), almacena las keys en un objeto de **MiLista** y guarda en atributos los valores, donde el nombre del atributo es una de las keys, por lo que mediante el metodo __getitem__ se puede acceder a su contenido de la siguiente forma: DiccionarioOrdenado[key]. Tambien tiene los metodos __iter__,__len__,__setitem__ y __repr__, además de alguna funciones útiles como append, pop, get_by_position,get_key,sort_values y change_dictionary. Utilizé ésta estructura para guardar todo lo que necesitara almacenar más de un dato, como los datos por día, la cola de propuestas (que debido aque es una estructura ordenada simplemente voy haciendo pop), guardar el mismísimo mundo (con las clases de Pais).

Clases:
 - Menu(): Hecho a partir de diccionarios, me permite escribir menos en el main.
 - Infeccion(): Recibe un string con el tipo de infeccion, y a partir de ésto genera sus propiedades de contagiosidad, mortalidad, etc. A cada país se le entregará como parámetro un objeto Infeccion.
 - Pais(): La clase más importante, sobre estás clases (que se almacenan en un diccionario en el main) se ejecutan todas las acciones. Tiene solo dos funciones, avanzar_dia y iniciar_infeccion que son autoexplicativas, sin embargo poseen varias **properties** que hacen que ciertos atributos como _self.estado_ y _self.prob_muerte_ se actualizen solos a medida que avanzan los días y las condiciones del pais. El país almacena sus paises fronterizos y de aeropuerto con sus nombres, no con los mismísimos objetos, por lo que desde el main se busca al objeto del pais fronterizo para modificarlos si es necesario.

Manejo de Archivos:
 - airports_to_dict(),borders_to_dict(),csv_to_dict_of_dicts(archivo): Son funciones que solo se ejecutan al iniciar una partida nueva, permite extraer losd atos de los archivos bases de la tarea y los entregan en forma de DiccionarioOrdenado().
 - mundo_to_csv(): Permite guardar partidas en un archivo "load.csv" dentro de la carpeta "Archivos", contiene toda la informacion de los paises, además de lo siguiente: dia_descubrimiento_infeccion,dia_descubrimiento_cura,progreso_al_dia,poseedores_de_cura,cola_propuestas, que son datos mundiales que se escriben en la priemra linea del .csv.
 - load_to_mundo(): Permite recuperar de "load.csv" la informacion almacenada, lo único que se pierde al volver a abrir una partida, son los datos diarios, como muertes por días, etc. Los cuales se podran volver a imprimir una vez que se avance un día desde que se cargó la partida.
 
El programa se ejecuta desde el archivo **main.py**
