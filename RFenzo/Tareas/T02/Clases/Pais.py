from Clases.Infeccion import Infeccion
from EstructurasDeDatos.MiLista import MiLista


class Pais:
    def __init__(self,nombre,habitantes, frontera, aeropuerto,infectados = 0,infeccion = None, muertos = 0
                 ,estado_aeropuerto = True,estado_frontera = True, mascarilla = False,dia_actual = 0,cura = False,
                 dia_extincion = None,dia_inicio_infeccion = None):
        self.nombre = nombre

        self.habitantes = habitantes
        self.muertos = muertos

        self.infectados = infectados
        self.infeccion = infeccion

        self.dia_extincion = dia_extincion
        self.dia_actual = dia_actual
        self.dia_inicio_infeccion = dia_inicio_infeccion

        if aeropuerto:
            self.aeropuerto = aeropuerto
        else:
            self.aeropuerto = MiLista()

        if frontera:
            self.frontera = frontera
        else:
            self.frontera = MiLista()

        #booleans:
        self.mascarilla = mascarilla
        self.estado_frontera = estado_frontera
        self.estado_aeropuerto = estado_aeropuerto
        self.cura = cura

    def inicio_infeccion(self,infeccion,dia):
        self.infeccion = Infeccion(infeccion)
        self.infectados = 1
        self.dia_inicio_infeccion = dia

    def avanzar_dia(self):
        self.dia_actual += 1

    @property
    def estado(self):
        if self.muertos == self.habitantes:
            if not self.dia_extincion:
                self.dia_extincion = self.dia_actual
            return "muerto"
        elif self.infectados == 0:
            if self.dia_inicio_infeccion:
                self.dia_termino_infeccion = self.dia_actual
            return "limpio"
        else:
            return "infectado"

    @property
    def sanos(self):
        return self.habitantes - self.muertos - self.infectados

    @property
    def efecto_mascarilla(self):
        if self.mascarilla:
            return 0.3
        return 1

    @property
    def prob_muerte(self):
        return min(min(0.2,((self.dia_actual-self.dia_inicio_infeccion)**2)/100000)*self.infeccion.mortalidad,1)
