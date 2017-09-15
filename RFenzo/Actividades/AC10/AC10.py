import threading
import time
import random
from random import expovariate, choice
from collections import OrderedDict


class Nodo:

    def __init__(self, value, connections):
        self.lock = threading.Lock()
        self.value = value
        self.connections = connections


class Persona(threading.Thread):

    def __init__(self, iden, hp, pieza_actual, resistance, tiempo_inicio):
        super().__init__()
        self.id = iden
        self.hp = hp
        self.pieza_actual = pieza_actual
        self.tiempo_inicio = tiempo_inicio
        self.resistance = resistance

    @property
    def vivo(self):
        return True if self.hp > 0 else False

    @property
    def meta(self):
        return False if self.pieza_actual.value != termino else True

    def run(self):
        while self.vivo and not self.meta and len(llegados) < 3:
            prox_pieza = Nodos[choice(self.pieza_actual.connections)]
            with prox_pieza.lock:
                print('Persona {} entro a la pieza {}'.format(
                    self.id, prox_pieza.value))
                self.pieza_actual = prox_pieza
                time.sleep(choice([1, 2, 3]))
                print('Persona {} sale de la pieza {}'.format(
                    self.id, prox_pieza.value))
                self.hp -= 6-self.resistance
                print('Persona {} pierde {} de vida, le queda {} de hp'.format(
                    self.id, 6-self.resistance, self.hp))

        if not self.vivo:
            print('Persona {} se murio'.format(self.id))
        elif self.meta:
            print('Persona {} llego a la meta'.format(self.id))
            llegados.append(self)


class creator(threading.Thread):

    def __init__(self, lugar_inicio):
        super().__init__()
        self.lugar_inicio = lugar_inicio

    def run(self):
        i = 0
        tiempo = 0
        while len(llegados) < 3:
            Persona(i, random.randint(80, 121), self.lugar_inicio,
                    random.randint(1, 4), tiempo).start()
            i += 1
            print('Se ha creado una persona')
            delta = expovariate(1/5)
            tiempo += delta
            time.sleep(delta)


class Simulacion:

    def __init__(self):
        pass

    def run(self):
        print("Comenzo la Simulacion!")

        creator(Nodos[inicio]).start()

with open('laberinto.txt', 'r') as f:
    inicio = f.readline().strip()
    termino = f.readline().strip()
    d = OrderedDict()
    for line in f:
        origen, destino = line.strip().split(',')
        if origen in d:
            d[origen].append(destino)
        else:
            d[origen] = [destino]

Nodos = {}
for a in d:
    Nodos[a] = Nodo(a, d[a])

Nodos['60'] = Nodo('60', [])
llegados = []
sim = Simulacion()
sim.run()
