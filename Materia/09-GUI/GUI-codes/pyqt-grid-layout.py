__author__ = "Christian Pieringer"

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QGridLayout, QVBoxLayout)


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):

        # Creamos una etiqueta para status. Recordar que los os Widget simples
        # no tienen StatusBar.
        self.label1 = QLabel('', self)

        # Creamos la grilla para ubicar los Widget (botones) de manera matricial
        self.grilla = QGridLayout()

        valores = ['1', '2', '3',
                   '4', '5', '6',
                   '7', '8', '9',
                   '0', 'CE', 'C']

        # Generamos las posiciones de los botones en la grilla y le asociamos
        # el texto que debe desplegar cada boton guardados en la lista valores

        posicion = [(i, j) for i in range(4) for j in range(3)]

        for posicion, valor in zip(posicion, valores):
            if valor == '':
                continue

            boton = QPushButton(valor)

            # A todos los botones les asignamos el mismo slot o método
            boton.clicked.connect(self.boton_clickeado)

            # El * permite convertir los elementos de la tupla como argumentos
            # independientes
            self.grilla.addWidget(boton, *posicion)

        # Creamos un layout vertical
        vbox = QVBoxLayout()

        # Agregamos el label al layout con addWidget
        vbox.addWidget(self.label1)

        # Agregamos el layout de la grilla al layout vertical con addLayout
        vbox.addLayout(self.grilla)
        self.setLayout(vbox)

        self.move(300, 150)
        self.setWindowTitle('Calculator')

    def boton_clickeado(self):
        """
        Esta funcion ejecuta la inspeccion cada vez que un boton es
        presionado identificando el boton presionado y la posicion en que
        está en la grilla.
        """

        # Sender retorna el objeto que fue clickeado. En boton ahora hay una
        # instancia de QPushButton()
        boton = self.sender()

        # Obtenemos el identificador del elemento en la grilla
        idx = self.grilla.indexOf(boton)

        # Con el identificador obtenemos la posición del ítem en la grilla
        posicion = self.grilla.getItemPosition(idx)

        # Actualizamos label1
        self.label1.setText(
            'Presionado boton {}, en fila/columna: {}.'.format(idx,
                                                               posicion[:2]))


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    form.show()
    sys.exit(app.exec_())
