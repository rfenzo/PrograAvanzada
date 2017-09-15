from gui.Gui import MyWindow
from PyQt5 import QtWidgets
from consultas import ejecutar
import sys


class T03Window(MyWindow):

    def __init__(self):
        super().__init__()
        self.contar = self.contador()

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!
        l_s_t = ejecutar(True, querry_array)

        [self.add_answer(self.escribir(i)) for i in l_s_t]

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        l_s_t = ejecutar(False, querry_array)
        with open('resultados.txt', 'w') as f:
            [f.write(self.escribir(i)) for i in l_s_t]
        self.add_answer('Archivo generado correctamente\n')

    def contador(self):
        i = 0
        while True:
            yield i
            i += 1

    def escribir(self, i):
        nconsulta = '---------- Consulta {} ----------'.format(
            str(next(self.contar)).zfill(2))+'\n'
        consulta = str(i[0])+'\n'
        resultado = 'Resultado:' + str(i[1])+'\n'
        tiempo = 'Tiempo: ' + str(i[2]) + '\n'
        return nconsulta+consulta+resultado+tiempo


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
