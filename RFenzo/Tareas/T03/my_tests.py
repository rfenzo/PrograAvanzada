import consultas
import random
import numpy
import unittest
import itertools
from funciones import rango_intervalo
from types import GeneratorType as generador


class Testeo(unittest.TestCase):

    def test_asignar(self):
        funcion = consultas.asignar
        # para todo tipo de datos:
        # retorna none
        self.assertIsNone(funcion("x0", "a"))
        self.assertIsNone(funcion("x1", 1))
        self.assertIsNone(funcion("x2", False))
        self.assertIsNone(funcion("x3", ["asignar", "a", 1]))
        self.assertIsNone(funcion("x4", [1, 2, 3, 4]))
        self.assertIsNone(funcion("x5", 1.))
        # las guarda en memoria
        self.assertIn("x0", consultas.variables)
        self.assertIn("x1", consultas.variables)
        self.assertIn("x2", consultas.variables)
        self.assertIn("x3", consultas.variables)
        self.assertIn("x4", consultas.variables)
        self.assertIn("x5", consultas.variables)
        # las guarda bien..
        self.assertEquals(consultas.variables["x0"], "a")
        self.assertEquals(consultas.variables["x1"], 1)
        self.assertEquals(consultas.variables["x2"], False)
        self.assertEquals(consultas.variables["x3"], ["asignar", "a", 1])
        self.assertEquals(consultas.variables["x4"], [1, 2, 3, 4])
        self.assertEquals(consultas.variables["x5"], 1.)
        # error de tipo:
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1, 2)
        # argumento invalido:
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion("x", 2, 3)
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()

    def test_filtrar(self):
        funcion = consultas.filtrar
        # retorna columna (generador)
        gen = (i for i in range(0, 100))
        filtrado = funcion(gen, ">", 22)
        self.assertIsInstance(filtrado, generador)
        # realmente los filtra
        [self.assertGreaterEqual(x, 22) for x in filtrado]
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1, ">", 1)
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion([1], ">")
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x", ">", 2)
        # imposible procesar
        with self.assertRaisesRegexp(Exception, "Imposible procesar"):
            funcion((i for i in range(0, 100)), ">%", 1)

    def test_evaluar(self):
        funcion = consultas.evaluar
        # retorna columna (generador)
        func = lambda x: x**2
        evaluado = funcion(func, -1, 1, 0.1)
        self.assertIsInstance(evaluado, generador)
        # realmente los evalua
        cuadrados = [i for i in evaluado]
        normales = [i for i in rango_intervalo(-1, 1, 0.1)]
        [self.assertAlmostEqual(x[0]**2, x[1])
         for x in zip(normales, cuadrados)]
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1, 1, 1, 1)
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion(1, 2)
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x", 1, 2, 3)

    def test_PROM(self):
        funcion = consultas.PROM
        # retorna numero
        gen = (i for i in range(0, 101))
        promedio = funcion(gen)
        self.assertIsInstance(promedio, (int, float))
        # calculado correctamente
        self.assertEquals(promedio, numpy.mean([i for i in range(0, 101)]))
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1)
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion([])
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion([], [])
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x")

    def test_MEDIAN(self):
        funcion = consultas.MEDIAN
        # retorna numero
        gen = (i**2 for i in range(0, 101))
        mediana = funcion(gen)
        self.assertIsInstance(mediana, (int, float))
        # calculado correctamente
        self.assertEquals(mediana, numpy.median([i**2 for i in range(0, 101)]))
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1)
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion([])
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion([1], [1])
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x")

    def test_VAR(self):
        funcion = consultas.VAR
        # retorna numero
        gen = (i**2 for i in range(0, 101))
        varianza = funcion(gen)
        self.assertIsInstance(varianza, (int, float))
        # calculado correctamente
        self.assertEquals(varianza, numpy.var(
            [i**2 for i in range(0, 101)], ddof=1))
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1)
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion([])
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion([1], [1])
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x")

    def test_DESV(self):
        funcion = consultas.DESV
        # retorna numero
        gen = (i**2 for i in range(0, 101))
        desv = funcion(gen)
        self.assertIsInstance(desv, (int, float))
        # calculado correctamente
        self.assertEquals(desv, numpy.var(
            [i**2 for i in range(0, 101)], ddof=1)**0.5)
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1)
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion([])
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion()
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion({}, {})
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x")

    def test_comparar_columna(self):
        funcion = consultas.comparar_columna
        # retorna boolean
        gen11 = (i**2 for i in range(0, 102))
        gen11, gen21, = itertools.tee(gen11)
        gen12 = (i**2 for i in range(0, 101))
        gen12, gen22 = itertools.tee(gen12)

        boolean = funcion(gen11, ">", "LEN", gen12)
        self.assertIsInstance(boolean, bool)
        # calculado correctamente
        self.assertEquals(consultas.LEN(gen21) > consultas.LEN(gen22), boolean)
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1, 1, 1, 1)
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion([], "a", "b", [])
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion([], [])
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x", "a", "b", "y")

    def test_do_if(self):
        funcion = consultas.do_if
        # retorna el correcto
        gen1 = (i**2 for i in range(0, 101))
        gen1, gen2, gen3, gen4, gen5, gen6 = itertools.tee(gen1, 6)
        doif1 = funcion(['PROM', gen1], True, ['DESV', (gen2)])
        doif2 = funcion(['PROM', gen4], False, ['DESV', (gen5)])
        self.assertEquals(doif1, consultas.PROM(gen3))
        self.assertEquals(doif2, consultas.DESV(gen6))
        # error de tipo
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion(1, 1, 1)
        with self.assertRaisesRegexp(Exception, "Error de tipo"):
            funcion([], 1, [])
        # argumento invalido
        with self.assertRaisesRegexp(Exception, "Argumento invalido"):
            funcion([], [])
        # referencia invalida
        with self.assertRaisesRegexp(Exception, "Referencia invalida"):
            funcion("x", "a", "y")

    def test_operar(self):
        funcion = consultas.operar
        with self.assertRaisesRegexp(Exception, "Error matematico"):
            funcion((i for i in range(0, 10)), "/", 0)


suite = unittest.TestLoader().loadTestsFromTestCase(Testeo)
unittest.TextTestRunner().run(suite)
