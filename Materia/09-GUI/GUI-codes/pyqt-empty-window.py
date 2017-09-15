__author__ = 'christian pieringer'

import sys

from PyQt5.QtWidgets import (QWidget, QApplication)


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Definimos la geometría de la ventana.
        # Parámetros: (x_top_left, y_top_left, width, height)
        self.setGeometry(200, 100, 300, 300)

        # Podemos dar nombre a la ventana (Opcional)
        self.setWindowTitle('Mi Primera Ventana')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec_())
