+ Log-in: sensible a contraseñas y nombres de usuario mal ingresadas, genera un objeto persona con el recurso y tipo (anaf,piloto,jefe).

+ Ingresar fecha: Sensible a años bisiesto superiores al 2000. Robusto contra malos inputs, tanto al momento de ingresar como al modificar archivos.

+ Es posible ver todos los archivos desde un usuario anaf, "incendios.csv" solo se muestran los incendios que partieron antes de la fecha.

+ Es posible modificar archivos desde usuario anaf

+ Es posible, crear usuarios nuevos, cerrar sesion y acceder a ellos sin necesidad de cerrar el programa.

+ Es posible modificar la fecha sin necesidad de salir del programa, recargando todos los datos segun la nueva fecha.

+ El programa restringe el menu para los usuarios NO anaf

+ En caso de que no se encuentre creada la carpeta para almacenar los reportes, la creará automáticamente

+ El efecto de las meteorologia sobre el incendio es calculado con la funcion update() de Incedio, realiza una simulacion hora a hora, pero esta hecho para que no tenga que calcular todo de nuevo si ya fue calculado para t>t_0, si no que verificar desde la vez anterior que se verificó.

+ No logré implementar las simulaciones, hice algunos intentos que se pueden ver comentados tanto en el main (linea 127), como en el update de Incendios, pero creo que la estructura usada, con las funciones ya implementadas podrian permitirlo. Por ejemplo, el porcentaje de extincion, puntos de poder, fecha_retirada, fecha_llegada al incendio, entre otras, está inplementadas, pero al no poder realizar la simulacion, nunca se ocupan.

+ No me pareció necesario realizar una herencia de la clase persona para crear usuarios ANAF,PILOTO o JEFE, pues no poseín grandes diferencias.

+ Los usuarios PILOTO o JEFE deberian poder ver el incendio al cual estan asignados por el codigo que tengo hecho, pero no lo puedo probar porque no puedo simular.

+ Para manejar el tiempo, cree el archivo date.py que contiene varias funciones que permiten pasar de fecha a horas, de horas a fecha, calcular diferencias de horas, etc. Verifiqué que funcionara todo comparandolo con datetime.

+ Para leer los archivos, cree el archivo custm_csv que contienen varias funciones, entre las cuales está:

   + input_to_csv: que es utilizado para pedir al usuario datos y luego escribirlos en el archivo en formato csv

   + csv_to_dict: que lee el archivo y por cada linea crea un diccionario ordenado (OrderedDict)

   + print_csv: que permite imprimir un archivo en formato csv.
