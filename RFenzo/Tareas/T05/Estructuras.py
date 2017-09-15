from UnidadesBase import StructureTimer
from Funciones import closest_distance, move_vertices, angle_mouse
from PyQt5.QtCore import QTimer
from Datos import area_real, real_size, vertices, sizes, parametros, items
from math import degrees
from random import choice


class Inhibidor(StructureTimer):

    def __init__(self, *args):
        super().__init__(*args)
        self.respawn = 30

    def revive(self):
        self.dano_recibido = 0
        self.pos_signal.emit(self.pos, self.tipo, sizes[self.tipo], self.id)
        self.start()

    def ciclo(self):
        if self.team == 'team_player':
            self.inhibidor = self.mygame.bot_inhibidor
            self.hero = self.mygame.hero
        else:
            self.inhibidor = self.mygame.inhibidor
            self.hero = self.mygame.hero_bot
        if not self.alive:
            self.mygame.dead_id(self, True)
            self.stop()


class Tower(StructureTimer):

    def __init__(self, attack_graphic, r_attack_graphic, *args):
        super().__init__(*args)
        self.damage = 30
        self.attack_speed = 1
        self.attack_range = 60
        self.attack_graphic = attack_graphic
        self.r_attack_graphic = r_attack_graphic
        self.target = None
        self.stack_img_attack = []

    def attack(self, target):
        target.receive_dmg(self)

    def get_target(self):
        # defender heroe
        if len(self.hero.attackers) > 0 and (self.target not in
                                             self.hero.attackers):
            for posible in self.hero.attackers:
                if (closest_distance(self.vertices, posible.vertices) <
                        self.attack_range):
                    return posible

        # atacar minionG, minionN, hero
        posibleN = None
        posibleHero = None
        for obj in self.targets:
            if (closest_distance(self.vertices, obj.vertices) <
                    self.attack_range):
                if obj.tipo == 'MinionG':
                    return obj
                elif obj.tipo == 'MinionN':
                    posibleN = obj
                else:
                    posibleHero = obj

        if posibleN:
            return posibleN
        elif posibleHero:
            return posibleHero

        return None

    def ciclo(self):
        if self.team == 'team_player':
            self.inhibidor = self.mygame.bot_inhibidor
            self.hero = self.mygame.hero
            self.targets = self.mygame.team_bot
        else:
            self.inhibidor = self.mygame.inhibidor
            self.hero = self.mygame.hero_bot
            self.targets = self.mygame.team_player

        if not self.mygame.pause:
            self.target = self.get_target()
            if self.target:
                if (int(self.i % (self.nro_ciclos /
                                  self.attack_speed)) == 0):

                    self.attack(self.target)
                    vangle = angle_mouse(self.target.center, self.center)

                    self.attack_graphic.emit(self.target.center,
                                             degrees(vangle), 0, self.tipo,
                                             self.id)
                    self.stack_img_attack.append((self.id, 0))

            # remover de imagen de ataque
            if len(self.stack_img_attack) != 0 and self.i % 30 == 0:
                self.r_attack_graphic.emit(*self.stack_img_attack.pop(0))

            self.i += 1

        if not self.alive:
            self.mygame.dead_id(self, False)
            self.stop()


class Nexo(StructureTimer):

    def __init__(self, *args):
        super().__init__(*args)

    def ciclo(self):
        if self.team == 'team_player':
            self.inhibidor = self.mygame.bot_inhibidor
            self.hero = self.mygame.hero
        else:
            self.inhibidor = self.mygame.inhibidor
            self.hero = self.mygame.hero_bot
        if not self.alive:
            self.mygame.dead_id(self, False)
            self.stop()


class Objeto:

    def __init__(self, name, price, attr, bonus):
        self.tipo = name
        self.price = price
        self.bonus = bonus
        self.attr = attr

    def affect(self, player):
        player.objetos.append(self)
        attr_ant = getattr(player, self.attr)

        if self.attr == 'sa_cooldown':
            x = round(attr_ant-self.bonus, 1)
        else:
            x = round(attr_ant+self.bonus, 1)
        setattr(player, self.attr, x)
        player.money -= self.price


class Tienda(QTimer):

    def __init__(self, mygame):
        super().__init__()
        self.timeout.connect(self.ciclo)
        self.start(mygame.refresh_rate*1000)
        self.mygame = mygame
        self.pos = mygame.pos_i['Tienda']
        self.tamano = area_real['Tienda']
        self.player = mygame.hero
        self.center = (self.pos[0]+real_size['Tienda']/2,
                       self.pos[1]+real_size['Tienda']/2)
        # mygame.areas_ocupadas['Tienda'] = Area(self.pos, self.tamano)
        self.refresh_rate = mygame.refresh_rate

        self.save_signals()

        self.buy_range = parametros['Tienda']['buy_range']
        self.items = items
        self.vertices = move_vertices(vertices['Tienda'], self.pos)

    def save_signals(self):
        self.pos_signal = self.mygame.pos_signal_struct
        self.pos_signal.emit(self.pos, 'Tienda', sizes['Tienda'], str(999))
        self.avisar_signal = self.mygame.avisar_signal
        self.tienda_show_signal = self.mygame.tienda_show_signal
        self.money_display_signal = self.mygame.money_display_signal
        self.insuf_money_signal = self.mygame.insuf_money_signal
        self.items_display_signal = self.mygame.items_display_signal
        self.attrs_display_signal = self.mygame.attrs_display_signal

    def show(self):
        self.tienda_show_signal.emit()

    def end_game(self):
        self.stop()

    def comprar(self, tipo):
        if self.player.money >= items[tipo][0]:
            attr = None
            if tipo == "Earthstone":
                attr = choice(["damage", "attack_range", "attack_speed",
                               "armor", "move_speed", "sa_cooldown"])
                precio, _, bonus = items[tipo]
                objeto = Objeto(tipo, precio, attr, bonus)
            else:
                objeto = Objeto(tipo, *self.items[tipo])

            self.items[tipo][0] += self.items[tipo][0]/2
            self.items[tipo][2] = round(1.1*self.items[tipo][2], 1)

            self.player.adquirir_item(objeto)
            self.money_display_signal.emit(attr)
            self.items_display_signal.emit(objeto)
            self.attrs_display_signal.emit()
        else:
            self.insuf_money_signal.emit()

    def ciclo(self):
        d = closest_distance(self.player.vertices, self.vertices)
        if d <= self.buy_range or not self.player.alive:
            self.allowed = True
            self.avisar_signal.emit(True)
        else:
            self.allowed = False
            self.avisar_signal.emit(False)
