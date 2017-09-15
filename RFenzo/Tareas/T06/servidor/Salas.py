import threading
from random import choice, shuffle, sample
import os
import time


class SalasManager(threading.Thread):

    def __init__(self, server, listdir):
        super().__init__()
        self.server = server
        self.salas = {i: Sala(server, i, self) for i in listdir}
        self.act_info_salas_dict = {i: None for i in listdir}
        self.stoop = False

    @property
    def ready_to_send(self):
        for name, value in self.act_info_salas_dict.items():
            if value == None:
                return False
        return True

    def receive_req(self, sala, req):
        self.act_info_salas_dict[sala] = req

    def stop(self):
        for sala in self.salas.values():
            sala.stop()
        self.stoop = True

    def run(self):
        for sala in self.salas.values():
            sala.start()
        while not self.stoop:
            if self.ready_to_send:
                self.server.requests.append(('act_info_sala',
                                             [self.act_info_salas_dict]))

                self.act_info_salas_dict = self.act_info_salas_dict.fromkeys(
                    self.act_info_salas_dict, None)
            time.sleep(0.1)


class Sala(threading.Thread):

    def __init__(self, server, nombre_sala, pantinicio):
        super().__init__()
        self.pantinicio = pantinicio
        self.server = server
        self.nombre_sala = nombre_sala
        self.songs = [i for i in os.listdir(
            'songs/{}/'.format(self.nombre_sala))]
        self.artistas = []
        self.clientes = {}
        self.played_songs = []
        self.c_nuevos = []
        self.c_nuevos_no_jugar = []
        self.respondieron = []
        self.tabla = {}
        self.nro_c_ant = 0
        self.stoop = False

    def stop(self):
        self.stoop = True

    def new_game(self):
        self.current_song = choice(self.songs)
        self.played_songs.append(self.current_song)
        self.artistas.append(self.current_song.split('-')[0].strip())

        others = [i.split('-')[1].replace('_', ' ').replace('.wav', '')
                  for i in self.songs if i != self.current_song]

        actual = [self.current_song.split(
            '-')[1].replace('_', ' ').replace('.wav', '')]
        if others:
            options = actual + sample(others, min(3, len(others)))
        else:
            options = actual
        shuffle(options)
        self.options = options
        self.path = 'songs/{}/'.format(self.nombre_sala) +\
            self.current_song

    def run(self):
        self.i = 0
        while not self.stoop:
            x = {'n_clientes': len(self.clientes),
                 'tiempo': round(self.i, 1),
                 'artistas': self.artistas[:2]}
            self.pantinicio.receive_req(self.nombre_sala, x)

            if len(self.clientes) != 0:
                if self.nro_c_ant == 0:
                    self.new_game()

                # mandar a clientes nuevos!
                if len(self.c_nuevos) != 0:
                    x = (self.c_nuevos, self.options,
                         self.path, self.tabla)
                    self.server.requests.append(('send_act_sala', x))
                    self.c_nuevos = []

                if self.i >= 8:
                    if self.nro_c_ant != 0:
                        self.new_game()

                    for cliente in self.clientes.values():
                        self.tabla[cliente.username] = (cliente.puntaje, '',
                                                        '')

                    x = (self.clientes.values(), self.options, self.path,
                         self.tabla)
                    self.server.requests.append(('send_act_sala', x))

                    self.i = 0
                    self.c_nuevos_no_jugar = []
                    self.respondieron = []
                self.i += 1
            else:
                self.i = 0

            self.nro_c_ant = len(self.clientes)

            time.sleep(1)

    def check_correct_song(self, username, elejida):
        cliente = self.clientes[username]
        if self.nombre_sala not in cliente.aciertos_salas:
            cliente.aciertos_salas[self.nombre_sala] = 0

        if (cliente not in self.c_nuevos_no_jugar and
                cliente not in self.respondieron):
            aumento = 0
            correcto = elejida == self.current_song.split(
                '-')[1].replace('_', ' ').replace('.wav', '')
            if correcto:
                aumento = round((20-round(self.i, 1)))*100
                cliente.puntaje += aumento
                cliente.aciertos_salas[self.nombre_sala] += 1

            descalificado = 'SI' if not correcto else 'NO'
            self.tabla[username] = (cliente.puntaje,
                                    round(self.i, 1), descalificado)

            x = (self.clientes.values(), self.tabla)
            self.server.requests.append(('send_tabla', x))

            self.respondieron.append(cliente)

            return correcto, aumento, False
        else:
            return None, None, True

    def accept_client(self, cliente):
        self.tabla[cliente.username] = (cliente.puntaje, '', '')
        # mandar a clientes antiguos
        if len(self.clientes) != 0:
            x = (self.clientes.values(), self.tabla)
            self.server.requests.append(('send_tabla', x))
            self.c_nuevos_no_jugar.append(cliente)

        self.clientes[cliente.username] = cliente
        self.c_nuevos.append(cliente)

    def remove_client(self, client_username):
        quitter = self.clientes.pop(client_username)
        self.tabla.pop(client_username)
        if quitter in self.respondieron:
            self.respondieron.remove(quitter)
        # mandar a todos los clientes
        x = (self.clientes.values(), self.tabla)
        self.server.requests.append(('send_tabla', x))
