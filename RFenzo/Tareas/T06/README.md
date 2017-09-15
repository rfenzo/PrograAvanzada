Lo que no hice:
- 

- Los emoticones del chat (me compliqué con el posicionamiento, pero los metodos para detectarlos y mostrarlo en pantalla están (lineas 462,470,478,y 495 a 497 del frontend.py)))
- el bonus de canción x2


Servidor
=
Server.py
-
Al momento de ejecutar el servidor, te preguntará si deseas cortar las canciones dentros de la carpeta **songs** a aproximadamente 40 seg (perderás las canciones originales), esto para que en caso de que el cliente no las tenga, sea más rápido la descarga. Finalmente te preguntará si quieres crear salas con un ecualizador predefinido en **freq=1.6** y **n=0**, estos parámetros los puedes cambiar en la **linea 57** y **linea 68** (se me olvidió reemplazar la variable), el ecualizado no debería tomar más de 1 a 2 segundos cuando n=0.

Luego de ésto el servidor comenzará a funcionar y avisará eventos importantes como coneccion, desconección y envios de canciónes a una IP.

El server crea una instancia de **SalasManager** que será detallado más adelante pero que básicamente junta la informacion que desean enviar los threads de sala y se lo pasa al servidor como un diccionario grande para luego enviarlo al cliente de una sola vez, para no saturar el server.

En general el server funciona como aquellos de los apuntes y ayudantía, con un thread por cliente que ejecuta  el método **listen client**, que recibe diccionarios serializados por **pickle** y se los pasa al metodo **handle command** el cual retorna un diccionario con la respuesta del servidor. Sin embargo, por motivos de fluidez y consistencia, decidí agregar una cola de cosas por enviar a los clientes (**self.requests** ) y un thread que las va enviando, ésto para garantizar de que el metodo encargado de enviar los datos al cliente (**send to client**) solo sea llamado una vez, generando una especie de lock.

Al ingresar un usuario nuevo, se crea un objeto de la clase **User (del archivo User.py)** que almacenará sus datos y luego se guarda serializado mediante **pickle**
en archivo dentro de la carpeta **cuentas**. En caso de ser un usuario conocido, simplemente se carga desde su archivo correspondiente. 

Al momento de **log-in** es cuando se revisan las canciones que posee el cliente, y en caso de ser diferentes, se envian las canciones faltantes (puedes borrar una cancion, y solo se descargará esa). Si el programa se cae cuanto está descargando las canciones, probablemente se deba a la conexion, para evitar que se caiga, se puede modificar el tiempo de dormido del programa al enviar las canciones, colocando **time.sleep(5)** en la **linea 125** debería funcionar si o si.

Una vez finalizada la descarga se puede jugar.

Hay cuatro metodos que se encuentran fuera de **handle commands** y que envian datos al cliente, estos son:

- **send song**: llamado desde handle command para enviar una cancion a un cliente.
- **act info sala**: llamado por el **SalasManager (del archivo Salas.py)** que una vez que contiene la información de cada una de las salas en un diccionario, ejecuta éste metodo, el cual puede actualizar tanto la informacion dentro de la sala como de la pantalla principal, ésto segun donde se encuentre el cliente.
Dentro de la sala actualiza el tiempo y puntaje, fuera de la sala actualiza tiempo, artistas reproducidos, y clientes conectados a esa sala.
- **send act sala**: llamado directamente desde las clases **salas**, se ejecuta cada 20 segundos, envía las opciones actuales, el path de la cancion actual y la tabla.

Salas.py
-
Contiene dos clases, SalasManager y Sala, ambos son threads y se comunican directamente.

-**SalasManager**: agrega a la cola de **server.requests** un diccionario con la informacion de cada una de las salas una vez que todas lo han solicitado

-**Sala**: segun su timer, envía en cada segundo informacion a SalasManager, y cada 20 segundos, informacion directamente a la cola del server. Es el encargado de revisar si la canción seleccionada por el cliente está correcta. Además tiene su propio seguimiento de clientes con el metodo **accept client** y **remove client**.

Carpeta AudioPrograms
-
Contiene dos programas:

-**AudioTools.py**: ahí se encuentra el ecualizador

-**WavHandle.py**: acá hay dos funciones, **wav_cutter** y **wav_editor**, el primero corta las canciones a 40 segundos, y el segundo es el que llama a la funcion **ecualizar** de **AudioTools** y genera las carpetas con las canciones ecualizadas y todo el manejo relacionado.

Client
=
Cliente.py
-
Decir de inmediato que es el **Frontend** el que contiene al cliente, y el cliente solo tiene señales que le permiten comunicarse con la interfaz gráfica.

El cliente posee un thread que ejecuta el metodo **listen server (linea 68)** el cual, cuando recibe un diccionario, dependiendo de la instrucción, utilizará una señal específica para comunicarse con el frontend. En caso de no ser un diccionario, se tratará de una canción, y mediante un ciclo acumulará datos hasta que la canción haya terminado de enviarse (**linea 120**).

Para enviar datos al server, posee el método **send to server** que envía siempre un diccionario serializado con **pickle** con un tipo de solicitud (Ej: 'enter_sala') y la solicitud (Ej: nombre de la sala). El cliente siempre hace envios de dato al servidor cuando es señalado por el frontend, por lo que hay varios metodos como **leave sala**, **chosen song**, etc que son llamado desde el frontend y que a su vez estos llaman al metodo **send to server**.

Finalmente, existe el metodo **set_signal** que es llamado desde el frontend cada vez que se quiere entregar al cliente una nueva señal para poder comunicarse.

Frontend.py
-
Lo más importante de éste archivo es la forma de pasar las señales al cliente, que como dije anteriormente, se realiza mediante **cliente.set_signal**. Gran parte del codigo de **MainWindow** está dedicado a crear, conectar y enviar las señales.

La **tabla de puntajes** puede ser poco intuitiva de encontrar, pero está en la pantalla de inicio en la esquina izquierda, al costado del botón salir.

Subiré ahora una screenshot de como se vé el juego en mi computador, en caso de que se vea mal en el tuyo.

