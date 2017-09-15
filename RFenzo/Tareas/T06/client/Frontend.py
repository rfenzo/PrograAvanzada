import sys
import os
import re


from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QAction, QVBoxLayout, QHBoxLayout, QPushButton,
                             QDesktopWidget, QGridLayout, QLineEdit,
                             QMessageBox, QStackedWidget)
from PyQt5.QtGui import (QIcon, QPixmap, QTransform, QPainter,
                         QFont, QPalette, QBrush, QImage, QTransform)
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QCoreApplication
from PyQt5.QtMultimedia import QSound
from PyQt5.QtTest import QTest
from random import sample, shuffle
from textwrap import wrap

from Client import Cliente


class MainWindow(QMainWindow):
    # Login
    account_signal = pyqtSignal()
    login_error_signal = pyqtSignal(str)
    done_downloading_signal = pyqtSignal()
    downloading_signal = pyqtSignal(str)
    download_porc_signal = pyqtSignal(str, float)
    # Pant Inicio
    act_info_salas_signal = pyqtSignal(dict)
    enter_sala_signal = pyqtSignal(str)
    leave_inicio_signal = pyqtSignal()
    recibir_tabla_signal = pyqtSignal(list)
    # Sala Juego
    act_info_mi_sala_signal = pyqtSignal(dict)
    tabla_signal = pyqtSignal(dict)
    evaluacion_signal = pyqtSignal(dict)
    act_sala_signal = pyqtSignal(dict)
    leave_sala_signal = pyqtSignal()
    error_jugar_signal = pyqtSignal(str)
    recibir_msg_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.cliente = Cliente()
        self.iniciador()

    def iniciador(self):
        self.setWindowTitle('PrograPop')

        x = QDesktopWidget().screenGeometry()
        self.geometry = (x.width()*0.8, x.height()*0.8)
        self.setFixedSize(*self.geometry)
        fondo = QLabel('', self)
        fondo.setMinimumSize(*self.geometry)
        text = "background-image: url(IMGS/background.jpg);"
        fondo.setStyleSheet(text)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login = Login(self)

        self.pant_inicio = PantInicio(self)
        self.sala_juego = SalaJuego(self)
        self.sala_juego.boton.clicked.connect(self.cliente.leave_sala)

        self.set_login_signals()
        self.set_inicio_signals()
        self.set_sala_signals()

        self.central_widget.addWidget(self.login)
        self.central_widget.addWidget(self.pant_inicio)
        self.central_widget.addWidget(self.sala_juego)

        self.central_widget.setCurrentWidget(self.login)

    def set_login_signals(self):
        self.account_signal.connect(self.log_in)
        self.login_error_signal.connect(self.login.temp_text)
        self.done_downloading_signal.connect(self.login.done_downloading)
        self.downloading_signal.connect(self.login.downloading)
        self.download_porc_signal.connect(
            self.login.download_widget.download_porc)
        self.cliente.set_signal(self.account_signal, 'account_signal')
        self.cliente.set_signal(self.login_error_signal, 'login_error_signal')
        self.cliente.set_signal(self.done_downloading_signal,
                                'done_downloading_signal')
        self.cliente.set_signal(self.downloading_signal,
                                'downloading_signal')
        self.cliente.set_signal(self.download_porc_signal,
                                'download_porc_signal')

    def set_inicio_signals(self):
        self.enter_sala_signal.connect(self.enter_sala)
        self.act_info_salas_signal.connect(self.pant_inicio.act_info_salas)
        self.leave_inicio_signal.connect(self.salir_inicio)
        self.recibir_tabla_signal.connect(self.pant_inicio.mostrar_tabla)
        self.cliente.set_signal(self.enter_sala_signal, 'enter_sala_signal')
        self.cliente.set_signal(self.act_info_salas_signal,
                                'act_info_salas_signal')
        self.cliente.set_signal(self.leave_inicio_signal,
                                'leave_inicio_signal')
        self.cliente.set_signal(self.recibir_tabla_signal,
                                'recibir_tabla_signal')

    def set_sala_signals(self):
        self.act_info_mi_sala_signal.connect(self.sala_juego.act_info)
        self.tabla_signal.connect(self.sala_juego.act_tabla_tiempos)
        self.evaluacion_signal.connect(self.sala_juego.evaluacion)
        self.act_sala_signal.connect(self.sala_juego.act_sala)
        self.leave_sala_signal.connect(self.salir_sala)
        self.error_jugar_signal.connect(self.sala_juego.error_jugar)
        self.recibir_msg_signal.connect(self.sala_juego.show_msg)
        self.cliente.set_signal(self.act_info_mi_sala_signal,
                                'act_info_mi_sala_signal')
        self.cliente.set_signal(self.evaluacion_signal, 'evaluacion_signal')
        self.cliente.set_signal(self.tabla_signal, 'tabla_signal')
        self.cliente.set_signal(self.act_sala_signal, 'act_sala_signal')
        self.cliente.set_signal(self.leave_sala_signal, 'leave_sala_signal')
        self.cliente.set_signal(self.error_jugar_signal, 'error_jugar_signal')
        self.cliente.set_signal(self.recibir_msg_signal, 'recibir_msg_signal')

    def log_in(self):
        if not hasattr(self.pant_inicio, 'username'):
            self.pant_inicio.iniciador()
        self.pant_inicio.username.setText(self.cliente.username)
        self.central_widget.setCurrentWidget(self.pant_inicio)

    def enter_sala(self, nombre_sala):
        self.sala_juego.nombre_sala = nombre_sala
        self.central_widget.setCurrentWidget(self.sala_juego)

    def salir_sala(self):
        self.sala_juego.current_song.stop()
        self.sala_juego.chat.setText('')
        self.central_widget.setCurrentWidget(self.pant_inicio)

    def salir_inicio(self):
        self.central_widget.setCurrentWidget(self.login)

    def closeEvent(self, event):
        self.cliente.desconectar()


class Login(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.iniciador()

    def iniciador(self):
        logo = QLabel('', self)
        img = QPixmap('IMGS/logo.png')
        logo.setAlignment(Qt.AlignCenter)
        logo.setPixmap(img)

        texto = QLabel('Nombre de usuario: ', self)
        texto.setFont(QFont("Rockwell", 13))
        texto.setStyleSheet('color: white')
        self.username_input = QLineEdit('', self)
        self.username_input.setFont(QFont("Rockwell", 13))
        self.boton = QPushButton('Ingresar', self)
        self.boton.setFont(QFont("Rockwell", 13))
        self.boton.clicked.connect(self.send_username)
        self.temp_text_label = QLabel('', self)
        self.temp_text_label.setAlignment(Qt.AlignCenter)

        self.download_widget = DownloadWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(logo)
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(texto)
        hbox1.addWidget(self.username_input)
        hbox1.addStretch()
        hbox2.addStretch()
        hbox2.addWidget(self.boton)
        hbox2.addStretch()

        vbox.addWidget(self.temp_text_label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)

    def send_username(self):
        username = self.username_input.text()
        if username != '':
            self.parent.cliente.input_username(username)

    def temp_text(self, text):
        self.temp_text_label.setText(text)
        QTest.qWait(1500)
        self.temp_text_label.setText('')

    def downloading(self, text):
        self.download_widget.append(text)

    def done_downloading(self):
        if not self.download_widget.isHidden():
            self.download_widget.terminado()

    def closeEvent(self, event):
        self.parent.cliente.desconectar()


class DownloadWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.iniciador()

    def iniciador(self):
        self.vbox = QVBoxLayout()
        self.vboxizq = QVBoxLayout()
        self.vboxder = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addLayout(self.vboxizq)
        hbox.addLayout(self.vboxder)
        self.vbox.addLayout(hbox)
        self.setWindowTitle('Downloading Songs')
        self.setLayout(self.vbox)

    def append(self, song):
        setattr(self, song+'porcent', QLabel('0 %', self))
        qlabel = QLabel('Downloading: '+song, self)
        qlabelporcent = getattr(self, song+'porcent')
        self.vboxizq.addWidget(qlabel)
        self.vboxder.addWidget(qlabelporcent)
        self.show()

    def download_porc(self, song, n):
        qlabelporcent = getattr(self, song+'porcent')
        qlabelporcent.setText('{} %'.format(round(100*n)))

    def terminado(self):
        exit = QPushButton('OK, a jugar!', self)
        exit.clicked.connect(self.hide)
        self.vbox.addWidget(exit)
        self.show()


class PantInicio(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def iniciador(self):
        self.tabla = TablaPuntajes()

        vbox = QVBoxLayout()
        self.username = QLabel('', self)
        self.username.setFont(QFont("Rockwell", 30))
        self.username.setMinimumHeight(100)
        self.username.setStyleSheet('color: white')
        self.username.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.username)

        name_salas = os.listdir('../client/songs')
        nro_estilos = len([None])
        nro_salas = len(name_salas)
        posiciones = [(i, j) for i in range(0, int(nro_salas/2))
                      for j in range(0, 2)]
        self.grid = QGridLayout()
        self.salas = {}

        i = 0
        for posicion in posiciones:
            new_sala = QPushButton('', self)
            new_sala.setFont(QFont("Rockwell", 13))
            self.salas[name_salas[i]] = new_sala
            new_sala.clicked.connect(self.enter_sala)
            self.grid.addWidget(new_sala, *posicion)
            i += 1

        vbox.addLayout(self.grid)

        cerrar_sesion = QPushButton('Cerrar sesión', self)
        cerrar_sesion.setFont(QFont("Rockwell", 13))
        cerrar_sesion.clicked.connect(self.parent.cliente.leave_inicio)
        tabla = QPushButton('Tabla de puntajes', self)
        tabla.setFont(QFont("Rockwell", 13))
        tabla.clicked.connect(self.req_tabla)
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(tabla)
        hbox.addStretch()
        hbox.addStretch()
        hbox.addWidget(cerrar_sesion)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def enter_sala(self):
        text = self.sender().text()
        sala = text.split('\n')[1].strip()
        self.parent.cliente.join_sala(sala)

    def act_info_salas(self, dict):
        for nombre_sala, content in dict.items():
            t = content['tiempo']
            n_clientes = content['n_clientes']
            artistas = ', '.join(content['artistas'])

            info = """
            {}
            Tiempo canción actual: {}
            Numero de usuarios: {}
            Algunos artistas :{}
            """.format(nombre_sala, t, n_clientes, artistas)
            self.salas[nombre_sala].setText(info)

    def req_tabla(self):
        self.parent.cliente.req_tabla()

    def mostrar_tabla(self, list):
        self.tabla.set_info(list)
        self.tabla.show()


class TablaPuntajes(QWidget):

    def __init__(self):
        super().__init__()
        self.iniciador()

    def iniciador(self):
        self.setWindowTitle('Tabla de puntajes')
        self.setFixedWidth(500)
        vbox = QVBoxLayout()
        self.posiciones = [(i, j) for i in range(1, 11)
                           for j in range(0, 4)]
        self.grid = QGridLayout()
        self.places = {}

        header = ['Nombre', 'Puntaje', 'Mejor sala', 'Peor sala']
        header_pos = [(0, i) for i in range(0, 4)]
        for posicion in header_pos:
            head = QLabel(header[posicion[1]], self)
            self.grid.addWidget(head, *posicion)

        for posicion in self.posiciones:
            new_player = QLabel('', self)
            self.places[posicion] = new_player
            self.grid.addWidget(new_player, *posicion)

        boton_salir = QPushButton('Salir', self)
        boton_salir.clicked.connect(self.hide)
        vbox.addLayout(self.grid)
        vbox.addWidget(boton_salir)
        self.setLayout(vbox)

    def set_info(self, sorted_players):
        # es una lista de tuplas
        i = 0
        for posicion in self.posiciones:
            if i//4 < len(sorted_players):
                self.places[posicion].setText(str(sorted_players[i//4][i % 4]))
            else:
                self.places[posicion].setText('')
            i += 1


class SalaJuego(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.iniciador()

    def iniciador(self):
        xsize, ysize = self.parent.geometry

        self.emojis = [':poop:', 'O:)', ':D', ';)',
                       '8)', 'U.U', ':(', '3:)', 'o.o', ':v']

        # vbox izq
        vbox_izq = QVBoxLayout()
        self.puntaje = QLabel('', self)
        self.puntaje.setFont(QFont("Rockwell", 15))
        self.puntaje.setStyleSheet('color: white')
        self.puntaje.setAlignment(Qt.AlignCenter)
        self.tiempo = QLabel('', self)
        self.tiempo.setStyleSheet('color: white')
        self.tiempo.setFont(QFont("Rockwell", 80))
        self.tiempo.setAlignment(Qt.AlignCenter)
        vbox_izq.addWidget(self.tiempo)
        vbox_izq.addWidget(self.puntaje)

        for i in range(4):
            x = QPushButton('', self)
            x.setFont(QFont("Rockwell", 15))
            x.setStyleSheet('color: white')
            x.setFixedSize(xsize/3-20, ysize/7-10)
            x.id = i
            x.clicked.connect(self.elejido)
            vbox_izq.addWidget(x)
            setattr(self, 'opcion'+str(i), x)

        # vbox der
        vbox_der = QVBoxLayout()
        self.tabla = QLabel('', self)
        self.tabla.setFont(QFont("Rockwell", 11))
        self.tabla.setStyleSheet('color: white')
        self.tabla.setFixedWidth(xsize/3-10)
        vbox_der.addWidget(self.tabla)
        vbox_der.addStretch()

        # vbox chat
        self.emojis_display = []
        vbox_chat = QVBoxLayout()
        self.chat = QLabel('', self)
        self.chat.setFont(QFont("Rockwell", 13))
        self.chat.setStyleSheet('color: white')
        self.chat_input = QLineEdit('', self)
        self.chat_input.setFont(QFont("times", 13))
        self.boton_chat = QPushButton('Send', self)
        self.boton_chat.setFont(QFont("times", 13))
        # self.boton_chat.setFixedWidth(50)
        self.boton_chat.clicked.connect(self.send_msg)
        hbox_chat = QHBoxLayout()
        hbox_chat.addWidget(self.chat_input)
        hbox_chat.addWidget(self.boton_chat)
        self.chat.setFixedWidth(xsize/3-10)
        vbox_chat.addWidget(self.chat)
        vbox_chat.addStretch()
        vbox_chat.addLayout(hbox_chat)

        # hbox
        hbox = QHBoxLayout()
        hbox.addLayout(vbox_chat)
        hbox.addLayout(vbox_izq)
        hbox.addLayout(vbox_der)

        # acertaste
        self.mensaje = QLabel('', self)
        self.mensaje.setFont(QFont("times", 26))
        self.mensaje.setStyleSheet('color: white')
        self.mensaje.setFixedHeight(ysize/6-10)
        self.mensaje.setAlignment(Qt.AlignCenter)

        # layout final
        vboxgrande = QVBoxLayout()
        vboxgrande.addWidget(self.mensaje)
        vboxgrande.addLayout(hbox)
        hbox_boton = QHBoxLayout()
        hbox_boton.addStretch()
        self.boton = QPushButton('Salir de la sala')
        self.boton.setFont(QFont("times", 13))
        hbox_boton.addWidget(self.boton)
        hbox_boton.addStretch()

        vboxgrande.addLayout(hbox_boton)
        self.setLayout(vboxgrande)

    def find_emojis(self, msg, posx, posy):
        for palabra in msg.split(' '):
            bool, emoji = self.is_emoji(palabra)
            if bool:
                posx = (msg.find(palabra)+posx)*10
                posy = posy*30
                self.create_emoji(emoji, (posx, posy))

    def create_emoji(self, txt, pos):
        label = QLabel('', self)
        img = QPixmap('emojis/'+txt.replace(':', 'h')+'.png')
        label.setPixmap(img)
        label.move(*pos)
        label.show()
        self.emojis_display.append(label)

    def is_emoji(self, s):
        for emoji in self.emojis:
            if emoji == s:
                return True, emoji
        return False, None

    def send_msg(self):
        msg = self.chat_input.text()
        if msg != '':
            self.chat_input.setText('')
            self.parent.cliente.send_msg(msg)

    def show_msg(self, dict):
        msg = dict['text']
        sender = dict['sender']
        text = self.chat.text()
        text += sender + ': '+'\n'.join(wrap(msg, 30))+'\n'
        #posx = len(self.parent.cliente.username)
        #posy = len(text.split('\n'))
        #self.find_emojis(msg, posx, posy)
        self.chat.setText(text)

    def play_song(self, path):
        if hasattr(self, 'current_song'):
            self.current_song.stop()
        self.current_song = QSound(path)
        self.current_song.play()

    def act_opciones_sala(self, options):
        self.marcado = False
        i = 0
        for song_name in options:
            boton = getattr(self, 'opcion'+str(i))
            boton.setStyleSheet('background-color: None')
            boton.setText(song_name)
            boton.show()
            i += 1

    def elejido(self):
        sender = self.sender()
        self.chosen = 'opcion'+str(sender.id)
        self.parent.cliente.chosen_song(sender.text())

    def act_info(self, dict):
        tiempo = dict['tiempo']
        puntaje = dict['puntaje']
        self.tiempo.setText(str(tiempo))
        self.puntaje.setText('Puntaje actual: {}'.format(puntaje))

    def act_tabla_tiempos(self, tabla):
        text = '{}|{}|{}|{}\n'.format('User', 'Puntaje',
                                      'Tiempo',
                                      'Descalificado?')
        for username, x in tabla.items():
            puntaje, t, desc = x
            text += '{}|{}|{}|{}\n'.format(username, puntaje,
                                           t, desc)

        self.tabla.setText(text)

    def act_sala(self, dict):
        self.play_song(dict['path'])
        self.act_tabla_tiempos(dict['tabla'])
        self.act_opciones_sala(dict['opciones'])

    def evaluacion(self, dict):
        acertaste = dict['texto']
        boton = getattr(self, self.chosen)
        color = '(0,255,0)' if acertaste else '(255,0,0)'
        boton.setStyleSheet('background-color: rgb'+color)
        aumento = dict['n']
        if acertaste:
            text = "Acertaste!\nSumaste {} puntos".format(aumento)
        else:
            text = "Fallaste"
        self.mensaje.setText(text)
        QTest.qWait(3000)
        self.mensaje.setText('')

    def error_jugar(self, text):
        self.mensaje.setText(text)
        QTest.qWait(3000)
        self.mensaje.setText('')

if __name__ == '__main__':
    app = QApplication([])
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
