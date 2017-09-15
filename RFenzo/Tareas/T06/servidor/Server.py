PORT = 3498
HOST = '192.168.1.47'


import socket
import threading
import pickle
import json
import os
import time
import sys

from Salas import Sala, SalasManager
from User import User
from AudioPrograms import WavHandle


def get_salas_songs(salas):
    x = {}
    for sala in salas:
        x[sala] = []
        for song in os.listdir('songs/{}/'.format(sala)):
            x[sala].append('songs/{}/'.format(sala)+song)

    return x


def read_accounts():
    dict = {}
    for file in os.listdir('cuentas/'):
        with open('cuentas\{}'.format(file), 'rb') as f:
            account = pickle.load(f)
            dict[account.username] = account
    return dict

cuentas = read_accounts()

if len(cuentas) != 0:
    accounts = cuentas.values()
    last_id = max(accounts, key=lambda x: x.id).id
else:
    last_id = -1


def iden(start):
    i = int(start)+1
    while True:
        yield str(i)
        i += 1

iden = iden(last_id)


class Server:

    def __init__(self):
        # cortar canciones a 40 seg aprox
        f, n = 1.8, 0
        opciones = '[1]=SI\n[2]=NO\n'
        texto1 = 'Desea cortar a 40seg las canciones?\n'
        texto2 = 'Desea ecualizar las canciones (f{},n{})?\n'.format(f, n)

        cortar = True if input(texto1+opciones) == '1' else False
        if cortar:
            WavHandle.wav_cutter('songs/')

        ecualizar = True if input(texto2+opciones) == '1' else False
        if ecualizar:
            WavHandle.wav_editor('songs/', 1.6, 0)

        self.socket_servidor = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
        self.cuentas = cuentas
        self.activos = {}
        self.requests = []

        thread = threading.Thread(name='Read Resquest',
                                  target=self.read_requests, daemon=True)
        thread.start()

        self.salas_manager = SalasManager(self, os.listdir('songs/'))
        self.salas_manager.start()
        self.salas = self.salas_manager.salas

        self.salas_songs = get_salas_songs(self.salas.keys())
        self.c_sockets = {}
        self.stack_sending_songs = {}
        self.run_socket = {}

        self.socket_servidor.bind((HOST, PORT))
        self.socket_servidor.listen(10)
        thread = threading.Thread(name='Accept Connections',
                                  target=self.accept_connections, daemon=True)
        thread.start()

    def read_requests(self):
        while True:
            if len(self.requests) != 0:
                request, args = self.requests.pop(0)
                getattr(self, request)(*args)

    def accept_connections(self):
        while True:
            client_socket, ip = self.socket_servidor.accept()
            print('{} se ha conectado'.format(ip))
            self.run_socket[client_socket] = True

            listen_client_thread = threading.Thread(
                name='Listen Client '+str(ip[0]),
                target=self.listen_client,
                args=(client_socket, ip),
                daemon=True)

            listen_client_thread.start()

    def send_to_client(self, socket, value, qtty=1, isdict=True, path='',
                       size_final=None):
        if isdict:
            socket.sendall(pickle.dumps(
                (qtty, size_final, isdict, path, value)))
        else:  # solo para enviar las canciones
            socket.sendall(pickle.dumps(
                (qtty, size_final, isdict, path, None)))
            for i in range(qtty):
                socket.send(value[79208*i:79208*i+79208])
            time.sleep(2)

    def listen_client(self, client_socket, ip):
        while self.run_socket[client_socket]:
            try:
                dictionary = pickle.loads(client_socket.recv(79208))
                response = self.handle_command(client_socket, dictionary, ip)
                self.send_to_client(client_socket, response)
            except Exception as error:
                print('{} se ha desconectado'.format(ip))
                print(error)
                break

    def handle_command(self, client_socket, dictionary, ip):
        req_type, req = dictionary['req_type'], dictionary['req']
        if req_type == 'get_user':
            username, user_salas_songs = req

            if username in self.activos:
                text = 'Ya hay un jugador activo con ese nombre'
                return {'type': 'login_error', 'text': text}

            elif username not in self.cuentas:
                new_account = User(next(iden), username, 0)

                with open('cuentas/'+new_account.username, 'wb') as file:
                    pickle.dump(new_account, file)

                self.cuentas = read_accounts()

            self.c_sockets[self.cuentas[username].id] = client_socket

            if user_salas_songs != self.salas_songs:
                self.stack_sending_songs[username] = []

                for sala, songs in self.salas_songs.items():
                    # cuando no hay una sala (agregar todas las canciones)
                    if sala not in user_salas_songs:
                        for song_path in songs:
                            self.send_song(self.cuentas[username],
                                           song_path, ip)

                    # cuando faltan canciones en una sala
                    elif songs != user_salas_songs[sala]:
                        song_sala_user = user_salas_songs[sala]
                        diferentes = [
                            x for x in songs if x not in song_sala_user]
                        for song_path in diferentes:
                            self.send_song(
                                self.cuentas[username], song_path, ip)

            self.activos[username] = self.cuentas[username]

            return self.cuentas[username].__dict__

        elif req_type == 'check_chosen_song':
            sala = self.salas[dictionary['sala']]
            acertaste, aumento, invalido = sala.check_correct_song(
                dictionary['username'], req)
            if not invalido:
                return {'type': 'evaluacion', 'texto': acertaste, 'n': aumento}
            else:
                text = 'Debes esperar a la siguiente ronda'
                return {'type': 'error_jugar', 'text': text}

        elif req_type == 'enter_sala':
            cliente = self.activos[dictionary['username']]
            cliente.sala = req
            self.salas[req].accept_client(cliente)
            return {'type': 'enter_sala', 'sala': req}

        elif req_type == 'leave_sala':
            cliente = self.activos[dictionary['username']]
            self.salas[cliente.sala].remove_client(cliente.username)
            del cliente.sala
            return {'type': 'leave_sala'}

        elif req_type == 'leave_inicio':
            quitter = self.activos.pop(dictionary['username'])
            self.c_sockets.pop(quitter.id)
            with open('cuentas/'+dictionary['username'], 'wb') as file:
                pickle.dump(quitter, file)
            self.cuentas = read_accounts()
            return {'type': 'leave_inicio'}

        elif req_type == 'desconectar':
            self.run_socket[client_socket] = False
            client_socket = None
            username, sala = req
            if username:
                quitter = self.activos.pop(username)
                self.c_sockets.pop(quitter.id)
                if sala:
                    self.salas[sala].remove_client(username)
                    del quitter.sala

                with open('cuentas/'+dictionary['username'], 'wb') as file:
                    pickle.dump(quitter, file)
                self.cuentas = read_accounts()

            return {'type': 'cerrar_programa'}

        elif req_type == 'send_msg':
            msg, sala = req
            username = dictionary['username']
            sala = self.salas[sala]
            response = {'type': 'recibir_msg', 'text': msg, 'sender': username}
            for cliente in sala.clientes.values():
                self.send_to_client(self.c_sockets[cliente.id], response)
            return {'type': 'pass'}

        elif req_type == 'req_tabla':
            lista = [(i.username, i.puntaje, i.top_sala,
                      i.worst_sala) for i in self.activos.values()]
            return {'type': 'recibir_tabla', 'tabla': lista}

    def send_song(self, cliente, song_path, ip):
        with open(song_path, 'rb') as file:
            archivo = bytearray(file.read())
            length = len(archivo)
            qtty = length//79208
            size_final = length % 79208
            if size_final != 0:
                qtty += 1

        print('Enviando {} a {}'.format(song_path, ip))

        self.send_to_client(self.c_sockets[cliente.id], archivo, qtty,
                            False, song_path, size_final)

    def act_info_sala(self, dict_salas):
        for cliente in self.activos.values():
            if cliente.id in self.c_sockets:
                if hasattr(cliente, 'sala'):
                    if cliente.sala in dict_salas:
                        tiempo = dict_salas[cliente.sala]['tiempo']
                        response = {'type': 'act_info_mi_sala',
                                    'tiempo': tiempo,
                                    'puntaje': cliente.puntaje}

                        self.send_to_client(
                            self.c_sockets[cliente.id], response)
                else:
                    response = {'type': 'act_info_salas', 'salas': dict_salas}
                    self.send_to_client(self.c_sockets[cliente.id],
                                        response)

    def send_tabla(self, clientes, tabla):
        response = {'type': 'tabla_tiempos', 'tabla': tabla}
        for cliente in clientes:
            self.send_to_client(self.c_sockets[cliente.id], response)

    def send_act_sala(self, clientes, opciones, path, tabla):
        response = {'type': 'act_sala', 'tabla': tabla, 'opciones': opciones,
                    'path': path}
        for cliente in clientes:
            self.send_to_client(self.c_sockets[cliente.id], response)


if __name__ == "__main__":
    server = Server()
    while True:
        x = input('>   ')
        if x == 'stop':
            server.salas_manager.stop()
            sys.exit()
