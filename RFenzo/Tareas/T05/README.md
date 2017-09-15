Resumen
-
Creo haber implementado todo lo que se pedía a nivel de juego,controles del campeón, personalidades de campeones, modificación de subditos grandes cuando el inhibidor esta muerto (linea 45 y 57 de la clase Minion), respawn de subditos, herores y inhibidor. Cheats y shortcuts. Movimientos de sprites, imagenes de ataque, la tienda con sus sistema de compra y rango de compra. Un display de los atributos del campeón y sus items comprados. Click izquierdo y derecho del campeón, y la habilidad especial usada por el campeón enemigo. 

Con respecto a la personalidad de los campeones enemigos, agregé la característica de que se aleje de una torre que lo esté dañando cuando éste no la tiene por objetivo y no hay minions cerca (para que no vaya directamente a atacar al heroe y muriese debido a la torre).

Con respecto a la compra de items, modifiqué el efecto del báculo, haciendo que reduciera el cooldown total de la habilidad especial.



Lo que no implementé:


1. Evitar superposición de unidades y estructuras no se sobrepongan.
2. Sistema de datos almacenados (partida guardada y constantes)

Observación punto 2: Deje artos parametros almacenados en el archivo **Datos.py** (tamaños de sprites, entre otras cosas) y **Campeones.py** (los parametros de cada campeon y sus habilidades, por ejemplo, se puede modificar el ataque de un campeon entre otras cosas).

Código
-
Cree dos clases dentro de **UnidadesBase.py** de las cuales heredaran las estructuras y las unidades. Estas clases **StructureTimer** y **UnitTimer** son **QTimers**.

El programa se corre desde el archivo **Frontend.py**. Lo que hice fué que el frontend, la clase InGame (QWidget del juego), tenga como atributo a una clase **MyGame** que está contenida en el archivo **Backend.py**. Al iniciar el programa y elejir un campeón, el frontend le entrega todas las señales a MyGame, por lo que el backend solo tiene acceso a las señales entregadas por el frontend, nada más.

En el frontend hay varias clases, al ejecutar el **MainWindow** se crea un objeto de la clase **Menu**, la cual luego llama a una funcion de Mainwindow para elejir el hero, creando una clase **ChooseHero**, finalmente, haciendo lo mismo, se crea una clase **InGame** la cual es la que tendrá como atributo al backend.

Todos los objetos del backend son **QTimers**, tanto la clase **MyGame** (que controlando las muertes de las unidades y el respawn de los minions) como todas las demás clases almacenadas en **Heroes.py**, **Minions.py** y **Estructuras.py**.

El archivo **Funciones.py** contiene algunas funciones útiles que son utilizas en varios archivos del programa, pero las más notables son **angle_mouse** que entrega el ángulo entre un punto y el centro de un objeto, permite que los QTimers siempre este apuntando al centro de su target, y la segunda es **get_angle** que entrega el angulo entre el el punto más cercano entre vertices de dos unidades, esto define el movimiento de las unidades a sus targets.

Finalmente tengo dos archivos de datos:

- **Campeones.py**: hay datos de los campeones, permitiendo modificar ataque, velocidad de movimiento, e incluso las habilidades especiales.
- **Datos.py**: Hay informacion del tamaño de escalamiento de las imagenes, por lo que si se modifica los numeros de **sizes**, se estaría modificando el tamaño de la imagen de un heroe o minion, pero está todo expresado en base a eso por lo que el juego y visualización del juego debería seguir siendo armónico. Adicionalmente está contenido el parametro del rango de compra de la tienda, los items de la tienda, y la vida total de las estructuras.

P.D: El frontend me quedo medio largo y desordenado, lo siento.
