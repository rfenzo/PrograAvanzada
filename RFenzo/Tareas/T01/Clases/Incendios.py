import math
from Funciones import date

from Funciones.custom_csv import csv_to_dict


class Incendio:

    def __init__(self, incendio, fecha_actual):
        self.id = incendio["id"]
        self.lat = incendio["lat"]
        self.lon = incendio["lon"]
        self.potencia = incendio["potencia"]
        self.fecha_inicio = incendio["fecha_inicio"]
        self._fecha_actual = fecha_actual
        self.radio = 1
        self.recursos_utilizados = []
        self.recursos_activos = []
        self.puntos_extincion_recursos = 0
        self.now = 0

    @property
    def fecha_actual(self):
        return self._fecha_actual

    @fecha_actual.setter
    def fecha_actual(self, fecha):
        self.update(fecha)
        self._fecha_actual = fecha

    @property
    def diferencia_en_horas(self):
        if self.radio == 1:
            return date.diferencia_en_horas(self.fecha_inicio, self.fecha_actual)
        else:
            return date.diferencia_en_horas(date.convertir_a_fecha(self.now), self.fecha_actual)

    @property
    def activo(self):
        if self.puntos_poder - self.puntos_extincion_recursos > 0:
            return True
        return False

    @property
    def superficie_afectada(self):
        return int(math.pi * self.radio ** 2)

    @property
    def puntos_poder(self):
        return self.superficie_afectada * self.potencia

    def update(self, fecha):
        self._fecha_actual = fecha
        """                                ESTO SE PONDRIA SI FUNCIONARA LA SIMULACION
        if self.activo:
            for j in self.recursos_activos:
                estado_recurso = j.update(fecha)
                if estado_recurso == "trabajando en incendio":
                    self.puntos_extincion_recursos += j.tasa_extincion #no se multiplica por nada porque iremos revisando hora a hora.
                if (self.puntos_poder -self.puntos_extincion_recursos )<= 0  or j.tiempo_trabajo_restante <  0:
                    j.fecha_retiro = fecha
        else:
            return self.activo
        """

        meteorologias = date.filter_by_date(date.filter_by_date(
            csv_to_dict("meteorologia.csv"), fecha), self.fecha_inicio, reverse=True)
        meteorologias.sort(
            key=lambda x: date.convertir_a_horas(x["fecha_inicio"]))

        if self.now == 0:
            self.now = date.convertir_a_horas(self.fecha_inicio)

        climas_activos = {'VIENTO': 0,
                          'TEMPERATURA': 0, 'LLUVIA': 0, 'NUBES': 0}

        for _ in range(1, int(self.diferencia_en_horas) + 1):
            contador = 0
            for j in climas_activos:
                if climas_activos == 0:
                    contador += climas_activos[j]
            # ningún clima activo, entonces saltamos al siguiente clima, para
            # no pasar de a una hora.
            if contador == 0:
                pass

            self.radio += 500 / 1000

            for j in meteorologias:  # agregar climas
                if Incendio.intersecta(self, j):
                    climas_activos[j["tipo"]] = j

            for j in climas_activos:  # eliminar climas ya pasados
                if climas_activos[j] != 0:
                    if not date.geq(climas_activos[j]["fecha_termino"], date.convertir_a_fecha(self.now)):
                        meteorologias.pop(
                            meteorologias.index(climas_activos[j]))
                        climas_activos[j] = 0

            if climas_activos["VIENTO"] != 0:
                self.radio += ((climas_activos["VIENTO"]
                                ["valor"] * 3600 / 1000) / 100)

            if climas_activos["TEMPERATURA"] != 0:
                if climas_activos["TEMPERATURA"]["valor"] > 30:
                    self.radio += (climas_activos["TEMPERATURA"]
                                   ["valor"] - 30) * ((25 / 1000))

            if climas_activos["LLUVIA"] != 0:
                self.radio -= climas_activos["LLUVIA"]["valor"] * ((50 / 1000))

            self.now += 1

        self.now = date.convertir_a_horas(self._fecha_actual)

        return self.activo

    def agregar_recurso(self, recurso):
        if recurso in self.recursos_activos:
            if recurso.estado == "standby":
                self.recursos_utilizados.append(
                    self.recursos_activos.pop(self.recursos_activos.index(recurso)))
                self.recursos_activos.append(recurso)
        else:
            self.recursos_activos.append(recurso)

    @property
    def porcentaje_extincion(self):
        porcentaje = (self.puntos_extincion_recursos / self.puntos_poder) * 100
        return porcentaje

    def intersecta(self, clima):
        fisicamente = False
        x = clima["lat"] * 110  # x e y estan en km
        y = clima["lon"] * 110
        radio = clima["radio"] / 1000  # radio esta en km
        if math.sqrt((self.lat * 110 - x) ** 2 + (
                self.lon * 110 - y) ** 2) < self.radio + radio:  # si cumple entonces se intersectan fisicamente
            fisicamente = True

        temporalmente = date.between(convertir_a_fecha(self.now), clima[
                                     "fecha_inicio"], clima["fecha_termino"])

        return fisicamente and temporalmente

    def __str__(self):
        print("------------------------------------------------Incendio id: {}-------------------------------------------------------------------".format(self.id))
        print('lat:{},lon:{},potencia:{},fecha_inicio:{}, porcentaje_extincion: {}\n'.format(
            self.lat, self.lon, self.potencia, self.fecha_inicio, self.porcentaje_extincion))
print('Recursos activos:\n')
    if len(self.recursos_activos) != 0:
        for j in self.recursos_activos:
            print('id:{},tipo:{}'.format(j.id, j.tipo))
    else:
        print("No se encuentran recursos activos en este incendio.")
    print(
        "----------------------------------------------------------------------------------------------------------------------------------\n")
    return""
