PORT = 3498
HOST = '192.168.1.47'

import sys
import os
import json
import pickle
import socket
import threading

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


class Cliente:

    def __init__(self):
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket_cliente.connect((HOST, PORT))
            self.connected = True
            thread = threading.Thread(target=self.listen_server, daemon=True)
            thread.start()

        except Exception as error:
            print(error)
            self.socket_cliente.close()

    def input_username(self, username):
        salas_songs = {}
        if os.path.exists('songs'):
            for sala in os.listdir('songs/'):
                salas_songs[sala] = []
                for song in os.listdir('songs/{}/'.format(sala)):
                    salas_songs[sala].append('songs/{}/'.format(sala)+song)
        req = (username, salas_songs)
        self.send_to_server('get_user', req)

    def join_sala(self, nombre_sala):
        self.nombre_sala = nombre_sala
        self.send_to_server('enter_sala', self.nombre_sala)

    def chosen_song(self, song_name):
        self.send_to_server('check_chosen_song', song_name)

    def leave_sala(self):
        self.send_to_server('leave_sala', self.sala)

    def leave_inicio(self):
        self.send_to_server('leave_inicio', None)

    def send_msg(self, msg):
        req = (msg, self.sala)
        self.send_to_server('send_msg', req)

    def desconectar(self):
        req = (None, None)
        if hasattr(self, 'username'):
            req = (self.username, None)
        if hasattr(self, 'sala'):
            req = (self.username, self.sala)
        self.send_to_server('desconectar', req)

    def req_tabla(self):
        self.send_to_server('req_tabla', None)

    def listen_server(self):
        while self.connected:
            x = pickle.loads(self.socket_cliente.recv(2048))
            qtty, size_final, isdict, path, content = x

            if isdict:
                tipo = content['type']
                if tipo == 'account':
                    self.username = content['username']
                    self.done_downloading_signal.emit()
                    self.account_signal.emit()
                elif tipo == 'login_error':
                    self.login_error_signal.emit(content['text'])
                elif tipo == 'enter_sala':
                    self.sala = content['sala']
                    self.enter_sala_signal.emit(content['sala'])
                elif tipo == 'act_info_salas':
                    self.act_info_salas_signal.emit(content['salas'])
                elif tipo == 'act_info_mi_sala':
                    self.act_info_mi_sala_signal.emit(content)
                elif tipo == 'tabla_tiempos':
                    self.tabla_signal.emit(content['tabla'])
                elif tipo == 'evaluacion':
                    self.evaluacion_signal.emit(content)
                elif tipo == 'act_sala':
                    self.act_sala_signal.emit(content)
                elif tipo == 'leave_sala':
                    del self.sala
                    self.leave_sala_signal.emit()
                elif tipo == 'leave_inicio':
                    del self.username
                    self.leave_inicio_signal.emit()
                elif tipo == 'cerrar_programa':
                    self.connected = False
                elif tipo == 'error_jugar':
                    self.error_jugar_signal.emit(content['text'])
                elif tipo == 'recibir_msg':
                    self.recibir_msg_signal.emit(content)
                elif tipo == 'recibir_tabla':
                    self.recibir_tabla_signal.emit(content['tabla'])
            else:
                sala, cancion = path.split('/')[1:]

                self.downloading_signal.emit(cancion)

                tamano_tot = (qtty-1)*79208
                if size_final != 0:
                    tamano_tot += size_final
                else:
                    tamano_tot += 79208

                data = bytearray()
                for i in range(qtty):
                    if i+1 == qtty and size_final != 0:
                        data += self.socket_cliente.recv(size_final,
                                                         socket.MSG_WAITALL)
                    else:
                        data += self.socket_cliente.recv(79208,
                                                         socket.MSG_WAITALL)

                    self.download_porc_signal.emit(
                        cancion, len(data)/tamano_tot)

                if not os.path.exists('songs'):
                    os.makedirs('songs')

                if not os.path.exists('songs/'+sala):
                    os.makedirs('songs/'+sala)

                with open(path, 'wb') as f:
                    f.write(data)

    def send_to_server(self, req_type, req):
        dict = {'req_type': req_type, 'req': req}
        if hasattr(self, 'username'):
            dict['username'] = self.username
        if hasattr(self, 'sala'):
            dict['sala'] = self.nombre_sala
        try:
            self.socket_cliente.send(pickle.dumps(dict))
        except Exception as error:
            print(error)

    def check_username(self, username):
        self.send_to_server('req', username)

    def set_signal(self, signal, name):
        setattr(self, name, signal)

if __name__ == '__main__':
    client = Cliente()
