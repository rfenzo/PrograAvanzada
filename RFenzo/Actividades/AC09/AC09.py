from random import random, choice, expovariate, randint
from datetime import datetime as dt
import numpy


class Vehiculo:

    def __init__(self, person):
        self.rapidez = randint(12, 21)
        self.tipo = choice(['auto', 'camioneta'])
        person.conductor = True
        self.personas = [person]
        self.conductor = self.personas[0]
        self.posicion_inicial = person.posicion_inicial
        self.posicion = self.posicion_inicial
        self.base = None

    @property
    def capacidad(self):
        return 5 if self.tipo == 'auto' else 8

    @property
    def lleno(self):
        return True if len(self.personas) == self.capacidad else False

    def agregar_persona(self, persona):
        if not self.lleno:
            self.personas.append(persona)

    @property
    def prob_detenerse(self):
        if not self.lleno:
            return 0.6 if self.conductor.personalidad == 'generoso' else 0.3
        else:
            return 0

    def actualizar_posicion(self, tiempo):
        self.posicion = self.posicion_inicial + tiempo*self.rapidez
        if self.posicion > 100:
            self.base = (True, tiempo)


class Persona:

    def __init__(self):
        self.personalidad = choice(['egoista', 'generoso'])
        self.rapidez = randint(5, 9)
        self.posicion_inicial = randint(0, 60)
        self.posicion = self.posicion_inicial
        self.conductor = False
        self.base = None

    def actualizar_posicion(self, tiempo):
        self.posicion = self.posicion_inicial + tiempo*self.rapidez
        if self.posicion > 100:
            self.base = (True, tiempo)


class Simulacion:

    def __init__(self, tiempo_maximo, tasa_replicas):
        self.tiempo_maximo_sim = tiempo_maximo
        self.tasa_replicas = tasa_replicas
        self.tiempo_prox_temblor = 0
        self.tiempo_simulacion = 0
        self.personas = [Persona() for i in range(0, 75)]
        self.vehiculos = [Vehiculo(Persona())
                          for i in range(0, 25)]
        self.nro = 0
        self.tiempos = []
        self.p = []
        self.v = []
        self.m = []
        self.tsunamis = {'Debil': 0, 'Fuerte': 0}
        self.replicas = {'Debil': 0, 'Fuerte': 0}

    def proxima_replica(self):
        self.tiempo_prox_temblor = self.tiempo_simulacion + \
            round(expovariate(self.tasa_replicas))

    def actualizar_posiciones(self, tiempo):
        for i in self.personas:
            i.actualizar_posicion(tiempo)
        for i in self.vehiculos:
            i.actualizar_posicion(tiempo)

    def run(self):
        antes = dt.now()
        self.nro += 1
        self.proxima_replica()
        muertos = []

        while (self.tiempo_simulacion < self.tiempo_maximo_sim
               and len(muertos) < 100):
            self.tiempo_simulacion = self.tiempo_prox_temblor

            # hacer que se muevan
            self.actualizar_posiciones(self.tiempo_simulacion)

            # print('[SIMULACION] tiempo = {0} horas'.format(
            #     self.tiempo_simulacion))

            intensidad = 'Debil' if random() < 0.7 else 'Fuerte'
            # matar peatones

            for i in self.personas:
                if random() < self.prob_nosobrevivirPata(intensidad):
                    muertos.append(i)
                    # print('Muere persona por temblor')
                    self.personas.remove(i)
                    self.replicas[intensidad] += 1

            # matar autos

            for i in self.vehiculos:
                if random() < self.prob_nosobrevivirPata(intensidad):
                    [muertos.append(j) for j in i.personas]
                    self.vehiculos.remove(i)
                    self.replicas[intensidad] += len(i.personas)
                    # print('Muereb vehiculo por temblor ' +
                    #       'con {} personas'.format(len(i.personas)))

            # matar por marepoto

            if self.prob_marepoto(intensidad) < random():
                potencia = self.potencia_marepoto(intensidad)
                prob = potencia/10
                centro = randint(0, 100)
                alcance = potencia*2
                rango_valores = [i for i in range(
                    centro-alcance, centro+alcance)]
                for i in self.personas:
                    if i.posicion in rango_valores and random() < prob:
                        muertos.append(i)
                        # print('Muere persona por tsunami')
                        self.personas.remove(i)
                        self.tsunamis[intensidad] += 1

                for i in self.vehiculos:
                    if i.posicion in rango_valores and random() < prob:
                        [muertos.append(j) for j in i.personas]
                        # print('Muereb vehiculo por tsunami ' +
                        #       'con {} personas'.format(len(i.personas)))
                        self.vehiculos.remove(i)
                        self.tsunamis[intensidad] += len(i.personas)

            # recoger pasajero

            for i in self.vehiculos:
                for j in self.personas:
                    if (i.posicion == j.posicion and
                            random() < i.prob_detenerse):
                        # print('agregar pasajero')
                        i.agregar_persona(j)
                        self.personas.remove(j)

            self.proxima_replica()

        now = dt.now()-antes
        self.tiempos.append(now)
        self.p.extend(self.personas)
        self.v.extend(self.vehiculos)
        self.m.extend(muertos)

    def estadisticas(self):
        personas = self.p
        vehiculos = self.v
        tsunamis = self.tsunamis
        rep = self.replicas
        tiempos = self.tiempos

        por_auto = 0
        por_camioneta = 0
        for i in vehiculos:
            if i.tipo == 'auto':
                por_auto += len(i.personas)
            else:
                por_camioneta += len(i.personas)
        a_pie = len(personas)
        generosos = 0
        egoistas = 0
        for i in personas:
            if i.personalidad == 'egoista':
                egoistas += 1
            else:
                generosos += 1
        print('-'*10, 'RUN {}: ESTADISTICAS '.format(self.nro), '-'*10)
        print('Numero de llegados a la base en auto: ', por_auto)
        print('Numero de llegados a la base en camioneta: ', por_camioneta)
        print('Numero de llegados a la base a pie: ', a_pie)
        print('Numero de generosos llegados a la base: ', generosos)
        print('Numero de egoistas llegados a la base: ', egoistas)
        print('Numero de victimas por tsunamis debiles: ', tsunamis['Debil'])
        print('Numero de victimas por tsunamis fuertes: ', tsunamis['Fuerte'])
        print('Numero de victimas por replicas debiles: ', rep['Debil'])
        print('Numero de victimas por replicas fuertes: ', rep['Fuerte'])
        print('Tiempo de ejecucion promedio: ', numpy.mean(tiempos))

    def prob_nosobrevivirPata(self, intensidad):
        return 0.1 if intensidad == 'Debil' else 0.3

    def prob_nosobrevivirVehic(self, intensidad):
        return 0.15 if intensidad == 'Debil' else 0.6

    def prob_marepoto(self, intensidad):
        return 0 if intensidad == 'Debil' else 0.7

    def potencia_marepoto(self, intensidad):
        return 0 if intensidad == 'Debil' else randint(3, 8)

s = Simulacion(200, 1/randint(4, 10))

for _ in range(0, 10):
    s.tasa_replicas = 1/randint(4, 10)
    s.run()
    s.estadisticas()
s.estadisticas()
