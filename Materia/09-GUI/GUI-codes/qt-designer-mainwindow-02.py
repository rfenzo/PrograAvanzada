__author__ = 'Christian Pieringer'

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)

from backend import cuociente  # Importamos el back-end

formulario = uic.loadUiType("qt-designer-mainwindow.ui")


class MainWindow(formulario[0], formulario[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Creamos las conexiones con los puertos."""
        self.pushButton1.clicked.connect(self.click_button)

    def click_button(self):
        """
        Este método controla la acción ejecuta cada vez que presionamos el
        botón1.
        """

        try:
            """
            Cuociente pertenece al backend. En este caso, cualquier cambio en
            el cómo calcular cuociente no significará un cambio en el
            front-end.
            """
            resultado = cuociente(self.lineEdit1.text(), self.lineEdit2.text())
            self.label_3.setText('= {}'.format(resultado))
        except ValueError as err:
            QMessageBox.warning(self, '', str(err))


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
