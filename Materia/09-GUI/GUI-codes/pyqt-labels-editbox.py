__author__ = 'cpieringer'

import sys

from PyQt5 import QtWidgets


class MiVentana(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        """
        Este método realiza la inicialización de la ventana.
        """
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):
        """
        Este método configura la interfaz y todos sus widgets una vez que se
        llama __init__().
        """

        # Agregamos etiquetas usando el widget QLabel
        self.label1 = QtWidgets.QLabel('Texto:', self)
        self.label1.move(10, 15)

        self.label2 = QtWidgets.QLabel('Esta etiqueta es variable', self)
        self.label2.move(10, 50)

        # Agregamos cuadros de texto mediante QLineEdit
        self.edit1 = QtWidgets.QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)

        # Ajustamos la geometria de la ventana
        self.setGeometry(200, 100, 300, 300)
        self.setWindowTitle('Ventana con Boton')

        # Una vez que fueron agregados todos los elementos a la ventana la
        # desplegamos en pantalla
        self.show()


if __name__ == '__main__':
    """
    Recordar que en el programa principal debe existir una instancia de
    QApplication antes de crear los demas widgets, incluidas la ventana
    principal.

    Si la aplicacion no recibe parametros desde la line de comandos
    QApplication recibe una lista vacia como QApplication([]).
    """

    app = QtWidgets.QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
