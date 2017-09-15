from PyQt4 import QtGui
from PyQt4 import QtCore


class Ventana(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.__setUp()

    def __setUp(self):
        self.boton1 = QtGui.QPushButton('&Procesar', self)
        #self.boton1.resize(self.boton1.sizeHint())

    def keyPressEvent(self, KeyEvent):
        
        if KeyEvent.key() == QtCore.Qt.Key_S:
            print('Una tecla')
        elif KeyEvent.text().lower() ==  'a':
            print('otra tecla')

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ventana = Ventana()
    ventana.show()    
    app.exec_()