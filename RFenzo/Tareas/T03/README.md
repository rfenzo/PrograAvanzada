Metodo de ejecución
=

Para ejecutar una lista de comandos, primero se obtiene, de manera recursiva todos los comandos anidados (funcion *get_anidados*), para luego ejecutarlos por separado.

Entonces, para ejecutar una lista de comandos, se utilizan tres ejecutadores:

* *ej_no_anidado(sub_comando)*: el cual llama a la funcion requerida (LEN, asignar, etc) y la opera con el resto de los argumentos. Finalmente guarda en *stack_anidados* el resultado de aquella operacion bajo una key. Si la funcion es *asignar*, guarda el valor en 'variables' bajo una key. 
Esta es la funcion que atrapa las excepciones y permite la ejecución fluida del programa.

* *ej_anidado(comando)*: ejecuta *ej_no_anidado* sobre la lista de comandos anidados generados al comienzo, esto funciona porque al ejecutar una funcion, todas estas reemplazan sus parametros por los valores en *stack_anidados* y *variables*, resultando en un comando no anidado.

* *ejecutar(graficar, comandos)*: ejecuta *ej_anidado* sobre la lista de comandos. Esta es la funcion que recibe como argumento el 'querry_array' de main.py y un booleano para evitar que se restringir la funcion *graficar* en caso de que se seleccione el boton *generar archivo*.

Por otro lado, todas las funciones ejecutan tres metodos antes de hacer cualquier cosa, estos son:

* *replace_stack(args)*: recibe los argumentos de la funcion y en caso de estar guardados en el stack, los reemplaza y retorna un nuevo args

* *replace_variables(args)*: analogo al anterior pero con variables

* *handle_error(args,parametros)*: esta es la funcion que levanta errores en caso de que haya mal formato de parametros.

**Las funciones que reciben un gran numero datos utilizan generadores.**

Archivos
=
Consultas.py
-
Contiene todas las funciones correspondientes a las consultas, como *asignar*, *LEN*, *comparar*, etc.
Adicionalmente, contiene los metodos para obtener los comandos anidados y los tres ejecutadores.

Funciones.py
-
Contiene funciones que luego son usadas en **Consultas.py** como las anteriormente mencionadas:  *replace_stack*, *replace_variables*, *handle_error*.

Adicionalmente, contiene algunas otras funciones útiles detalladas a continuación:

* *csv_reader(archivo)*: retorna el el *header* como diccionario, y un generador de diccionarios por cada fila del archivo.

* *factorial(x)* : calcula el factorial de x

* *gen_tee(x,varstack)* : se ejecuta dentro de *replace_stack* y *replace_variables*. Revisa si x está dentro de varstack, si lo está y es un generador, retorna una nuevo generador mediante itertools.tee (ésto permite ocupar una variable más de una vez, de otro modo, como es un generador, solo se podría llamar una vez). Si lo está y no es un generador, simplemente retorna lo almacenado en varstack[x]. Finalmente, si no está en varstack, simplemente retorna x. 

* *check_range(string)* : se utiliza para la función *graficar* cuando se le ingresa un *rango*, permite revisar que tenga un buen formato

* *rango_intervalo(a,b,c)* : similar a la funcion *range* usual, pero permite ocupar saltos decimales y negativos (cuando b<a).

Operadores.py
-
Contiene una funcion por cada operador posible (+ , -, * , / , > , < , <= , >= , != ,==, >=<), las cuales son llamadas mediante las funciones *operacion* y *comparacion* de **Funciones.py** que simplemente operan dos numeros, retornado un booleano o un numero.

my_tests.py
-
Es donde se realiza el testing, adicionalmente a lo solicitado en el enunciado, también se probó la función *operar* para testear un **Error matemático** pues con los test mínimos no era posible probar.