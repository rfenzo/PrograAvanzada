import sys
from threading import Thread
from time import sleep

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton)


class Evento:
    """
    Esta clase maneja el evento que será transmitido por la señal a su
    respectivo slot cada vez que se produzca la emisión. Por simplicidad este
    evento solo incluye un mensaje, pero en la medida que se requiera podría
    portar más información.
    """

    def __init__(self, msg=''):
        self.msg = msg


class MiThread(Thread):
    """
    Esta clase representa un thread personalizado que será utilizado durante
    la ejecución de la GUI.
    """

    def __init__(self, trigger_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger = trigger_signal

    def run(self):
        # Creamos un evento para transmitir datos desde el thread a la interfaz
        evento = Evento()

        # TO-DO
        for i in range(10):
            sleep(0.5)
            evento.msg = str(i)
            self.trigger.emit(evento)

        evento.msg = 'Status: thread terminado'
        self.trigger.emit(evento)


class MiVentana(QWidget):

    # Creamos una señal para manejar la respuesta del thread
    threads_response = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.thread = None

    def init_gui(self):
        # Configuramos los widgets de la interfaz
        self.label = QLabel('Status: esperando thread', self)
        self.boton = QPushButton('Start Thread', self)
        self.boton.clicked.connect(self.start_threads)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.boton)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # Conectamos la señal del thread al método que maneja
        self.threads_response.connect(self.update_labels)

        # Configuramos las propiedades de la ventana.
        self.setWindowTitle('Ejemplo threads')
        self.setGeometry(50, 50, 250, 200)
        self.show()

    def start_threads(self):
        """
        Este método crea un thread cada vez que se presiona el botón en la
        interfaz. El thread recibirá como argumento la señal sobre la cual
        debe operar.
        """
        if self.thread is None or not self.thread.is_alive():
            self.thread = MiThread(self.threads_response)
            self.thread.start()

    def update_labels(self, evento):
        """
        Este método actualiza el label según los datos enviados desde el
        thread através del objeto evento. Para este ejemplo, el método
        recibe el evento, pero podría
        eventualmente no recibir nada.
        """
        self.label.setText(evento.msg)


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
