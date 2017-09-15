from PyQt5.QtCore import QTimer
from Datos import (area_real, sizes, tot_life, real_size,
                   vertices)
from Funciones import move_vertices


def iden():
    i = 0
    while True:
        yield str(i)
        i += 1
iden = iden()


class StructureTimer(QTimer):

    def __init__(self, mygame, pos, tipo, team):
        super().__init__()
        self.timeout.connect(self.ciclo)
        self.start(mygame.refresh_rate*1000)
        self.id = next(iden)
        self.tamano = area_real[tipo]
        self.center = (pos[0]+real_size[tipo]/2, pos[1]+real_size[tipo]/2)
        self.tot_life = tot_life[tipo]
        self.pos = pos
        # mygame.areas_ocupadas[self.id] = Area(self.pos, self.tamano)
        self.refresh_rate = mygame.refresh_rate
        self.nro_ciclos = int(1/self.refresh_rate)
        self.vertices = move_vertices(vertices[tipo], pos)
        self.dano_recibido = 0
        self.tipo = tipo
        self.team = team
        self.mygame = mygame
        self.__freeze = 0
        self.__downlife = 0
        self.i = 0

        self.pos_signal = mygame.pos_signal_struct
        self.pos_signal.emit(pos, self.tipo, sizes[self.tipo], self.id)
        self.mod_life_signal = mygame.mod_life_signal

    @property
    def alive(self):
        return self.life > 0

    @property
    def life(self):
        return self.tot_life - self.dano_recibido

    @property
    def freeze(self):
        return self.__freeze

    @freeze.setter
    def freeze(self, value):
        self.__freeze = value

    def receive_dmg(self, agresor):
        if hasattr(agresor, 'damage'):
            self.dano_recibido += agresor.damage
            self.mod_life_signal.emit(self.id, self.life, self.tot_life)

    @property
    def downlife(self):
        return self.__downlife

    @downlife.setter
    def downlife(self, value):
        self.__downlife = value

    def end_game(self):
        self.stop()


class UnitTimer(QTimer):

    def __init__(self, mygame, pos, tipo, team):
        super().__init__()
        self.timeout.connect(self.ciclo)
        self.start(mygame.refresh_rate*1000)
        self.id = next(iden)
        self.refresh_rate = mygame.refresh_rate
        self.tipo = tipo
        self.team = team
        self.isHero = tipo in ['Chau', 'Franky', 'Hernan']
        self.__pos = pos
        self.pos_inicial = pos
        self.refresh_rate = mygame.refresh_rate
        self.nro_ciclos = int(1/self.refresh_rate)
        self.tamano = area_real[self.tipo]
        self.dano_recibido = 0
        self.dx, self.dy = 0, 0
        self.team = team
        self.mygame = mygame
        self.target = None
        self.__freeze = 0
        self.__downlife = 0
        self.i = 0
        self.nro_img = 0
        self.img_attack = 0
        self.atacando = False

        if tipo in ['MinionG', 'MinionN']:
            self.pos_signal = mygame.pos_signal_minion
        else:
            self.pos_signal = mygame.pos_signal_hero

        self.pos_signal.emit(self.pos, self.tipo, sizes[self.tipo], self.id,
                             self.team)
        self.mod_life_signal = mygame.mod_life_signal
        self.mod_cool_signal = mygame.mod_cool_signal
        self.attack_graphic = mygame.attack_graphic
        self.r_attack_graphic = mygame.r_attack_graphic
        self.new_pos_signal = mygame.new_pos_signal
        self.change_img_signal = mygame.change_img_signal
        self.attack_graphic = mygame.attack_graphic
        self.r_attack_graphic = mygame.r_attack_graphic

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value
        # self.mygame.areas_ocupadas[self.id] = Area(self.pos, self.tamano)
        self.new_pos_signal.emit(
            self.id, (self.pos[0], self.pos[1]), self.isHero)

    @property
    def freeze(self):
        return self.__freeze

    @freeze.setter
    def freeze(self, value):
        self.__freeze = value

    @property
    def downlife(self):
        return self.__downlife

    @downlife.setter
    def downlife(self, value):
        self.__downlife = value

    @property
    def center(self):
        return (self.pos[0]+real_size[self.tipo]/2,
                self.pos[1]+real_size[self.tipo]/2)

    @property
    def vertices(self):
        return move_vertices(vertices[self.tipo], self.pos)

    @property
    def alive(self):
        return self.life > 0

    def attack(self, target):
        target.receive_dmg(self)

    def end_game(self):
        self.stop()
