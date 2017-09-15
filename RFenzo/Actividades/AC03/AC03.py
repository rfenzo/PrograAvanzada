from collections import deque

class Producto:
    def __init__(self,tipo,nombre,peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso


class Centro_Distribucion:
    def __init__(self):
        self.fila = []
        self.bodega = dict()

    def recibir_camion(self, camion):
        self.fila.append(camion)
        self.fila.sort(key=lambda x: x.prioridad, reverse=True)

    def rellenar_camion(self):
        count = self.fila[0].capacidad_maxima

        for producto in self.bodega:
            if producto.peso <= count:
                self.fila[0].productos.append(producto)
                count -= producto.peso
            if count != 0:
                break

    def enviar_camion(self):
        self.fila.pop(0)

    def mostrar_productos_por(self, tipo):
        print('Tipo: Cantidad\n')
        print(tipo + len(self.bodega[tipo]))

    def recibir_donacion(self, lista_productos):
        for producto in lista_productos:
            if not producto.tipo in self.bodega.keys():
                self.bodega[producto.tipo] = [producto]
            elif producto.tipo in self.bodega.keys():
                self.bodega[producto.tipo].append(producto)


class Camion:
    def __init__(self,capacidad,prioridad):
        self.capacidad_maxima = capacidad
        self.prioridad = prioridad
        self.productos = []

    def agregar_producto(self,producto):
        self.productos.append(producto)
        pass

    def __str__(self):
        tipos_productos = []
        tipos_productos2 = set()
        for j in self.productos:
            tipos_productos.append(j.tipo)
            tipos_productos2.add(j.tipo)

        print('Tipo: Cantidad\n')
        for j in tipos_productos2:
            print(str(j)+':'+str(tipos_productos.count(j)))
        return ''

def leer_productos():
    with open('productos.txt','r') as f:
        productos =[]
        for j in f:
            a,b,c = j.split(',')
            producto = Producto(a,b,c[:-1])
            productos.append(producto)
    return productos

def leer_camiones():
    with open('camiones.txt','r') as f:
        camiones = []
        for j in f:
            if len(j.split(',')) != 2:
                continue
            a,b = j.split(',')
            camion = Camion(a,int(b[:-1]))
            camiones.append(camion)
    return camiones

productos = leer_productos()
camiones = leer_camiones()
Centro = Centro_Distribucion()

for j in camiones:
    Centro.recibir_camion(j)

Centro.recibir_donacion(productos)

Centro.enviar_camion()
Centro.enviar_camion()
Centro.enviar_camion()
Centro.enviar_camion()
Centro.enviar_camion()



