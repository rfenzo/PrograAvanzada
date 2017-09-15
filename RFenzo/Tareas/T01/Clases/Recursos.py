import math
from Funciones.date import calcular_prox_fecha, geq, convertir_a_horas, convertir_a_fecha, diferencia_en_horas


class Recurso:

    def __init__(self, recurso):

        self.recurso = recurso
        self.id = recurso['id']
        self.tipo = recurso['tipo']

        self.lat = recurso['lat']
        self.lat_actual = recurso['lat']
        self.lon = recurso['lon']
        self.lon_actual = recurso["lon"]

        self.velocidad = recurso['velocidad']
        self.autonomia = recurso['autonomia']
        self.delay = recurso['delay']
        self.tasa_extincion = recurso['tasa_extincion']
        self.costo = recurso['costo']
        self._incendio = None
        self.fecha_retiro = None
        self._fecha_actual = None
        self.fecha_llegada_base = None
        self.estado = "standby"

    @property
    def incendio(self):
        return self._incendio

    @incendio.setter
    def incendio(self, incendio):
        self._incendio = incendio
        self.estado = "ruta a incendio"
        self.fecha_salida = incendio._fecha_actual
        distancia = math.sqrt((self.incendio.lat * 110 - self.lat * 110)
                              ** 2 + (self.incendio.lon * 110 - self.lon * 110) ** 2)
        self.fecha_llegada_incendio = calcular_prox_fecha(
            self.fecha_salida, distancia / (self.velocidad * 3.6))

    @property
    def fecha_actual(self):
        return self._fecha_actual

    @fecha_actual.setter
    def fecha_actual(self, fecha):
        self.update(fecha)
        self._fecha_actual = fecha

    def direccion_avance(self):
        norma = (((self.incendio.lat - self.lat_actual))**2 +
                 ((self.incendio.lon - self.lon_actual))**2)**0.5
        if self.estado == "ruta a incendio":
            return [(self.incendio.lat - self.lat_actual) / norma, (self.incendio.lon - self.lon_actual) / norma]
        elif self.estado == "trabajando en incendio" or self.estado == "standby":
            return [0, 0]
        else:
            return [(-self.incendio.lat + self.lat_actual) / norma, (-self.incendio.lon + self.lon_actual) / norma]

    def update(self, fecha):
        # [x,y], es [0,0] si esta standby o trabajando en incendio
        direccion_avance = self.direccion_avance()
        self._fecha_actual = fecha

        self.lat_actual += direccion_avance[0] * self.velocidad * 3.6 / \
            100 * diferencia_en_horas(self.fecha_salida, self._fecha_actual)
        self.lon_actual += direccion_avance[1] * self.velocidad * 3.6 / \
            100 * diferencia_en_horas(self.fecha_salida, self._fecha_actual)

        if geq(fecha, self.fecha_llegada_incendio):  # fecha_retiro es agregada desde incendios
            if not self.fecha_retiro:
                self.estado = "trabajando en incendio"
            elif geq(self.fecha_retiro, fecha):
                self.estado = "trabajando en incendio"
            elif not geq(self.fecha_retiro, fecha) and self.estado != "standby":
                self.estado = "ruta a base"

        if self.lat_actual == self.lat and self.lon_actual == self.lon:
            if not self.fecha_llegada_base:
                self.fecha_llegada_base = fecha
            self.estado = "standby"

        return self.estado

    @property
    def check_puntos_extincion_por_salida(self):
        return float(self.autonomia - 2 * self.check_distancia / self.velocidad) * self.tasa_extincion

    @property
    def check_distancia(self):
        if not self.incendio:
            return 0
        return math.sqrt((self.incendio.lat * 110 - self.lat * 110)**2 + (self.incendio.lon * 110 - self.lon * 110)**2)

    @property
    def tiempo_trabajado(self):
        return int(diferencia_en_horas(self.fecha_salida, self.incendio.fecha_actual))

    @property
    def tiempo_trabajo_restante(self):
        return int(self.autonomia - self.tiempo_trabajado)
    """
    ##############################################################################################################
    """

    def __str__(self):
        print('id:{},tipo:{},lat_base:{},lon_base:{},velocidad:{},autonomia:{}, delay:{}, tasa_extincion:{}, costo:{} \n'.format(self.id, self.tipo, self.lat_actual,
                                                                                                                                 self.lon_actual,
                                                                                                                                 self.velocidad,
                                                                                                                                 self.autonomia,
                                                                                                                                 self.delay, self.tasa_extincion, self.costo))
        print("lat_actual:{}, lon_actual:{}, estado:{} \n".format(
            self.lat_actual, self.lon_actual, self.estado))
        if self.estado != "standby":
            print('tiempo_trabajado:{}, tiempo_trabajo_restante:{}\n'.format(
                self.tiempo_trabajado, self.tiempo_trabajo_restante))
        return ''
