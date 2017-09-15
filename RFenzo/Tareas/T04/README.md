Primero que todo, en cada archivo entregado se encuentra documentada cada funcion y atributo utilizado, por lo que si no queda claro algo en este README, por favor ir directamente al archivo.

Resumen:
=
Traté de que mi código reflejara de mejor manera la realidad, generando por ejemplo clases separadas para cada tipo de ayudante, objetos independientes para cada ayudante, y que pudieran ser independientes (por ejemplo para que cada ayudante pueda ayudar a los alumnos durante una actividad).

Se implementaron casi todas las exigencias descritas por enunciado, generando graficos, estadisticas, etc.

Especificaciones del enunciado no se implementaron:
-
- Capacidad de los alumnos de mandar mails al profesor para retrasar la entrega de la tarea
- Capacidad del coordinador de realizar un descuento temporar en las notas
- Estadistica: Porcentaje de alumnos que aumentaron su confianza y cuantos la disminuyeron

Problema de simulacion:
-
No logré detectar el motivo de porqué los alumnos que no botan el ramo obtienen notas tan altas en tiempos avanzados del curso, me da la impresión de que la confianza se retroalimenta y por lo tanto, por ejemplo, el area de pep8 de tareas se dispara y no hay forma de que puedan sacarse malas notas.



Simulacion.py
=
Dentro de este archivo se realiza toda la simulacion.

Clase Simulacion
-
La clase Simulacion recibe como parametros, aquellos datos que se detallan en escenarios.csv.

En el init se llama a la funcion **person_gen() [linea 83]** que retorna, segun lo almacenado en **integrantes.csv**, una lista de alumnos, profesores, ayudantes de docencia, ayudantes de tareas y el coordinador del curso.

La generacion de eventos es regulada por el metodo **gen_eventos() [linea 145]**, metodo que revisa en el atributo *eventos* si un evento del mismo tipo ya se encuentra a la espera de ser ejecutado, si ya hay uno, entonces no agrega el siguiente evento. Esto conlleva a que en el atributo *eventos* siempre haya un, y solo un evento programado para cada tipo de evento (una ayudantia, una catedra, un control, etc...)

Para ejecutar los eventos se utiliza el metodo **ejecutar_evento [linea 219]**.

Finalmente, se usa el metodo **run() [linea 395]** para iterar hasta el fin de la simulacion (evento de entrega de notas del examen, semana 15)

Menu
=
A partir de la **linea 528** comienza el codigo para el menu (utiliza la **clase Menu**, que está ubicada en la carpeta Clases), el cual permite realizar una simulacion (y ver sus estadisticas) o multiples simulaciones a partir de los parametros en *escenarios.csv* (y ver cual es el escenario que tiene más aprobacion), para éste último puede que tome un tiempo realizar todas las simulaciones, por lo que coloqué unos *prints* para ir viendo su progreso.

Personas.py
=
Dentro de este archivo se encuentras las clases de todos los que participan en el curso y son detallados a continuacion

Clase Alumno
-
Todos los atributos de los alumnos son actualizados mediante el uso de **properties**.

Una de los metodos importantes de esta clase es el metodo **refresh() [linea 123]** la cual es llamada desde el metod **run()** de la clase **Simulacion**. Este metodo va actualizando el tiempo del alumno y guarda en diccionarios los valores anteriores de todos sus atributos semanales.

Otro metodo importante es el de **recibir_nota() [linea 352]** y **rendir_evaluacion [linea 415]**, el primero es utilizado para interactuar con el **coordinador** y la segunda para interactuar con una evaluacion (actividad,control o EntregaTarea).

Clase Ayu_Tareas
-
Posee el metodo **corregir() [linea 491]** el cual genera las notas para cada alumno segun una Tarea y se las entrega al coordinador.

Clase Ayu_Docencia
-
Posee el metodo **corregir() [linea 491]** el cual genera las notas para cada alumno segun una evaluacion y se las entrega al coordinador.

Además posee el metodo **ayudar() [linea 572]** el cual modifica el nivel de **S** del alumno, este metodo es llamado desde **Simulacion.py** en el metodo **ejecutar_evento**.

Clase Profesor
-
Posee el metodo **atender() [linea 638]** el cual es el encargado de atender (mediante el metodo **reunion() [linea 243]** de la clase **Alumno**) a los alumnos que solicitan una reunion con el profesor.

Clase Coordinador
-
Posee el metodo **publicar_notas() [linea 720]** el cual entrega a los alumnos las notas de una evaluacion, ademas calcula el promedio del curso,los reprobados y reprobados de la actividad y los guarda los atributos del coordinador.

Funciones.py
=
Dentro de este archivo se encuentran funciones útiles y que permiten manejar datos como las personalidades de los alumnos o la dinámica de los ayudantes de docencia en una actividad de clases (responder dudas).

Generadores.py
=
Dentro de este archivo se encuentran funciones dedicadas esclusivamente a generar datos, como el numero de creditos, numero de horas disponibles, fecha de los controles, el generador de personas, el lector de **escenarios.csv** y el generador de nota esperada.

parametros.csv
=
Permite modificar los valores de los parametros por defecto del enunciado, en total son 38, 11 de los cuales son los mismos de **escenarios.csv**. 

Los 27 restantes son detallados a continuacion:

- lim sup random exigencia y lim inf random exigencia: permiten modificar la formula de exigencia.
- lim sup random p inicial y lim inf random p inicial: permiten modificar el nivel de programacion inicial.
- cte conf notas act, cte conf notas tarea y cte conf notas ctrl: permiten modificar la ponderacion de cada tipo de evaluacion en la confianza relacionada a una nota.
- dif_(materia): permite modificar la dificultad de cada una de las materias.
- lim (sup o inf) random hour (creditos): permite modificar los rango de horas disponibles para cada cantidad de creditos.

datos.py
=
Se encuentran parametros de enunciado que son utilizados constantementes, inclusive los parametros leidos desde **parametros.csv** que se pedia por enunciado.

defaults.csv
=
Simplemente contiene los parametros por defecto del enunciado, al colocar un **-** en una linea de **parametros.csv** se reemplazara su valor por el correspondiente en **defaults.csv**.









