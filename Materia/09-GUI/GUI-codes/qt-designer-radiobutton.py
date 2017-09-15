__author__ = 'Christian Pieringer'

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

formulario = uic.loadUiType("qt-designer-radiobutton.ui")
print(formulario[0], formulario[1])


class MainWindow(formulario[0], formulario[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.mostrar_gustos)

    def mostrar_gustos(self):
        for rb_id in range(1, 3):
            if getattr(self, 'radioButton' + str(rb_id)).isChecked():
                opcion = getattr(self, 'radioButton' + str(rb_id)).text()
                self.label2.setText('prefiere: {0}'.format(opcion))


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
