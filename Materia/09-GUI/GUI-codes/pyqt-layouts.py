__author__ = 'Christian Pieringer'

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QHBoxLayout, QVBoxLayout)


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_GUI()

    def init_GUI(self):
        """
        Este método configura todos los widgets de la ventana.
        """
        self.setGeometry(100, 100, 300, 300)
        self.label1 = QLabel('Texto:', self)
        self.label1.move(10, 15)
        self.edit1 = QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)
        self.boton1 = QPushButton('&Calcular', self)
        self.boton1.resize(self.boton1.sizeHint())

        """
        Creamos el layout horizontal y agregamos los widgets mediante el
        método addWidget(). El método addStretch() nos permite incluir
        opcionalmente espaciadores.
        """
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.label1)
        hbox.addWidget(self.edit1)
        hbox.addWidget(self.boton1)
        hbox.addStretch(1)

        """
        Creamos el layout vertical y le agregamos el layout horizontal.
        Opcionalmente agregamos espaciadores para distribuir los widgets.
        Notar el juego entre el valor recibido por los espaciadores.
        """
        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    form.show()
    sys.exit(app.exec_())
