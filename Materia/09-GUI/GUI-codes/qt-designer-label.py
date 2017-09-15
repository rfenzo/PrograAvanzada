__author__ = 'Christian Pieringer'

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

"""
Creamos nuestra ventana principal heredando desde la GUI creada con Designer.
La función loadUiType retorna una tupla en donde  el primer elemento
corresponde al nombre de la ventana definido en QtDesigner, y el segundo
elemento a la clase base de la GUI.
"""

formulario = uic.loadUiType("qt-designer-label.ui")


class MainWindow(formulario[0], formulario[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
