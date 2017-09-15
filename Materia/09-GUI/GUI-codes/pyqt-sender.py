__author__ = "Christian Pieringer"

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QCoreApplication


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):
        self.label1 = QLabel('Status:', self)

        self.boton1 = QPushButton('&Boton 1', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.boton_callback)

        self.boton2 = QPushButton('&Boton 2', self)
        self.boton2.clicked.connect(self.boton_callback)
        self.boton2.resize(self.boton2.sizeHint())

        self.boton3 = QPushButton('&Salir', self)
        self.boton3.clicked.connect(QCoreApplication.instance().quit)
        self.boton3.resize(self.boton3.sizeHint())

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton1)
        hbox.addWidget(self.boton2)
        hbox.addWidget(self.boton3)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # Agregamos todos los elementos al formulario
        self.setGeometry(200, 100, 300, 200)
        self.setWindowTitle('Sender')

    def boton_callback(self):
        # Esta función registra el objeto que envía la señal del evento
        # y lo refleja mediante el método sender() en label3.
        sender = self.sender()
        self.label1.setText('Status: presionado boton {0}'.format(
            sender.text()))
        self.label1.resize(self.label1.sizeHint())


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    form.show()
    sys.exit(app.exec_())
