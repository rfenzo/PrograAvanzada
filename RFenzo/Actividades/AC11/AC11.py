import sys
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication, QLabel,
                             QGridLayout, QWidget, QVBoxLayout,  QHBoxLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtTest import QTest
from random import shuffle


class Memorize(QWidget):

    def __init__(self):
        super().__init__()
        self.init_Memorize()

    def init_Memorize(self):
        self.grid = QGridLayout()
        self.botones = []

        posiciones = [(i, j) for i in range(0, 5) for j in range(0, 5)]
        numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]*2
        numeros.append('b')
        shuffle(numeros)
        self.pos = {}

        i = 0
        for posicion in posiciones:
            self.pos[posicion] = numeros[i]
            boton = QPushButton('')
            boton.setIcon(QIcon("Imgs/back.png"))
            boton.setIconSize(QSize(120, 120))
            boton.foto = numeros[i]
            #boton.setIconSize(QSize(12, 12))
            boton.clicked.connect(self.boton_clickeado)
            self.botones.append(boton)
            self.grid.addWidget(boton, *posicion)
            i += 1

        self.contador = 0
        vert = QVBoxLayout()

        self.intentos = QLabel('')
        self.ganaste = QLabel('')
        self.hor = QHBoxLayout()
        self.hor.addWidget(self.intentos)
        self.hor.addWidget(self.ganaste)

        self.label = QLabel('')
        self.ocultar = QPushButton('Ocultar')
        self.ocultar.clicked.connect(self.boton_ocultar)

        vert.addLayout(self.hor)
        vert.addLayout(self.grid)
        vert.addWidget(self.ocultar)

        self.setLayout(vert)

        self.setGeometry(100, 100, 800, 800)
        self.show()
        self.match = []
        self.anterior = None
        self.procesando = False

    def boton_clickeado(self):
        if not self.procesando:

            boton = self.sender()
            foto = boton.foto

            if boton.foto == 'b':
                self.contador += 9

            boton.setIcon(QIcon("Imgs/{}.png".format(foto)))

            if self.anterior != None:
                self.procesando = True
                self.contador += 1
                self.intentos.setText('Nro Intentos {}'.format(self.contador))
                QTest.qWait(3000)
                if not self.is_match(boton, self.anterior):
                    boton.setIcon(QIcon("Imgs/back.png"))
                    self.anterior.setIcon(QIcon("Imgs/back.png"))
                else:
                    self.match.append((boton, self.anterior))

                self.anterior = None
                self.procesando = False
                self.intentos.setText('')

                if len(self.match) == 12:
                    self.ganaste.setText('GANASTE!')

            else:
                self.anterior = boton

    def boton_ocultar(self):
        for boton in self.botones:
            boton.setIcon(QIcon("Imgs/back.png"))

    def is_match(self, boton1, boton2):
        if boton1.foto == boton2.foto:
            return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Memorize()
    sys.exit(app.exec_())
