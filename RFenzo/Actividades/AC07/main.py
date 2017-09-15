__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime


"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""


def verificar_transferencia(funcion):
    def _verificar_transferencia(self, origen, destino, monto, clave):
        if origen not in self.cuentas or destino not in self.cuentas:
            raise AssertionError('Alguna de las cuentas no existe')
        elif self.cuentas[origen].saldo < monto:
            raise AssertionError(
                'La cuenta de origen no tiene saldo suficiente')
        elif self.cuentas[origen].clave != clave:
            raise AssertionError(
                'La clave no coincide con la cuenta de origen')
        return funcion(self, origen, destino, monto, clave)
    return _verificar_transferencia


def verificar_inversion(funcion):
    def _verificar_inversion(self, cuenta, monto, clave):
        if cuenta not in self.cuentas:
            raise AssertionError('La cuenta no existe')
        elif self.cuentas[cuenta].clave != clave:
            raise AssertionError(
                'La clave no coincide con la cuenta de origen')
        elif self.cuentas[cuenta].saldo < monto:
            raise AssertionError(
                'La cuenta no tiene saldo suficiente')
        elif self.cuentas[cuenta].inversiones + monto > 10000000:
            raise AssertionError(
                'No puedes tener mas de 10.000.000 en inversiones')
        return funcion(self, cuenta, monto, clave)
    return _verificar_inversion


def verificar_cuenta(funcion):
    def _verificar_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        while numero in self.cuentas:
            numero = self.crear_numero()
        if len(clave) != 4 or not clave.isdigit():
            raise AssertionError('La clave debe tener 4 numeros')
        elif rut.count('-') != 1 or not rut.replace('-', '').isdigit():
            raise AssertionError(
                "Rut invalido, tiene mas de un guion")
        else:
            print('Cuenta creada correctamente')
            return funcion(self, nombre, rut, clave, numero, saldo_inicial)
    return _verificar_cuenta


def verificar_saldo(funcion):
    def _verificar_saldo(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            raise AssertionError('La cuenta no existe')
        return self.cuentas[numero_cuenta].saldo
    return _verificar_saldo


def log(path):
    def _log(funcion):
        def __log(*args, **kwargs):
            with open(path, 'a') as f:
                x = funcion(*args, **kwargs)
                # si se desea imprimir la instancia de banco, comentar la linea
                # 72
                args = [z for z in args if not isinstance(z, Banco)]
                lista = ['-'.join(key, value) for key, value in kwargs]
                f.write('{} - {} : {}, {} | {} \n'.format(
                    datetime.now(), funcion.__name__, args, lista, x))
        return __log
    return _log


"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""


class Banco:

    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @log("C:/Users/roman/desktop/output.txt")
    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @log("C:/Users/roman/desktop/output.txt")
    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @log("C:/Users/roman/desktop/output.txt")
    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @log("C:/Users/roman/desktop/output.txt")
    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:

    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    try:
        bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())
    except AssertionError as Error:
        print('Error: ', Error)

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """

    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
