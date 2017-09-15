import unittest
from main import Descifrador

class TestearFormato(unittest.TestCase):

    def setUp(self):
        self.archivo = open('mensaje_marciano.txt','r')

    def test_archivo(self):
        total_suma = 0
        total_chars = 0

        for line in self.archivo:
            bytes = line.split(' ')
            for j in bytes:
                self.assertIsInstance(j,str)
                total_chars += len(j)
                for bin in j:
                    x = bin.replace('/n','')
                    try:
                        total_suma += int(x)
                    except Exception:
                        pass

        self.assertEqual(total_suma, 253)
        self.assertEqual(total_chars, 408)

    def tearDown(self):
        self.archivo.close()


class TestearMensaje(unittest.TestCase):
    def setUp(self):
        self.d= Descifrador('mensaje_marciano.txt')

    def test_incorrectos(self):
        self.d.lectura_archivo()
        self.assertTrue(self.d.elimina_incorrectos().replace(' ','').isdigit()) #verifica que sean solo binarios
        x = self.d.elimina_incorrectos()[1:]
        for j in x.split(' '): #verificar que tenga len mayor a 6 y menor a 8
            self.assertTrue(len(j) > 5 and len(j) < 8)

    def test_caracteres(self):
        codigo = self.d.lectura_archivo()
        codigo = self.d.elimina_incorrectos()
        self.assertTrue('$' not in self.d.limpiador(self.d.codigo))

    def test_codificacion(self):
        codigo = self.d.lectura_archivo()
        codigo = self.d.elimina_incorrectos()
        self.assertTrue(codigo.replace(' ','').isdigit())

suite = unittest.TestLoader().loadTestsFromTestCase(TestearFormato)
suite = unittest.TestLoader().loadTestsFromTestCase(TestearMensaje)
unittest.TextTestRunner().run(suite)