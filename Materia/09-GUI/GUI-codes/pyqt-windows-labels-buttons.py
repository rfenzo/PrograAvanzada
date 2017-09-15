__author__ = 'Christian Pieringer'

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton)


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):
        """
        Este método inicializa la interfaz y todos sus elementos o Widgets
        una vez que es llamado el formulario.
        """

        self.labels = {}
        self.labels['label1'] = QLabel('Texto:', self)
        self.labels['label1'].move(10, 15)
        self.labels['label2'] = QLabel('Aqui se escribe la respuesta', self)
        self.labels['label2'].move(10, 50)

        self.edit1 = QLineEdit('')
        self.edit1.setGeometry(45, 15, 100, 20)

        """
        El uso del caracter & al inicio del texto de algún botón o menú permite
        que la primera letra del mensaje mostrado esté destacada. La
        visualización depende de la plataforma utilizada.
        """
        self.boton1 = QPushButton('&Procesar', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.move(5, 70)

        """Agrega todos los elementos al formulario."""
        self.setGeometry(200, 100, 300, 300)
        self.setWindowTitle('Ventana con Boton')
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
