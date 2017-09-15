from UnidadesBase import UnitTimer
from Funciones import (angle_mouse, nearest, get_angle, closest_distance)
from Datos import sizes, real_size
from math import sin, cos, degrees
from numpy import pi
from Estructuras import Tower, Nexo, Tienda, Inhibidor
from Minions import Minion


class Hero(UnitTimer):

    def __init__(self, mygame, pos, team, tipo, tot_life,
                 move_speed, attack_speed, attack_range, special_attack,
                 sa_cooldown, armor, damage, respawn):
        super().__init__(mygame, pos, tipo, team)

        self.move_speed = move_speed
        self.attack_speed = attack_speed
        self.attack_range = attack_range
        self.special_attack = special_attack
        self.sa_cooldown = sa_cooldown
        self.sa_time = self.sa_cooldown
        self.respawn_inicial = respawn
        self.respawn = self.respawn_inicial
        self.tot_life = tot_life
        self.armor = armor
        self.damage = damage
        self.money = 0
        self.objetos = []
        self.attackers = []
        self.deaths = 0
        self.kills = 0
        self.waiting_sa = False
        self.__uplife = 0
        self.sa_target = None

    @property
    def life(self):
        return self.tot_life - self.dano_recibido

    @property
    def uplife(self):
        return self.__uplife

    @uplife.setter
    def uplife(self, value):
        self.__uplife = value

    def revive(self):
        self.respawn = 1.1**self.deaths + self.respawn_inicial
        self.dano_recibido = 0
        self.pos = self.pos_inicial
        self.pos_signal.emit(self.pos, self.tipo, sizes[self.tipo], self.id,
                             self.team)
        self.start()

    def cooldown_recovery(self):
        if self.sa_time < self.sa_cooldown:
            self.sa_time += self.refresh_rate
            self.mod_cool_signal.emit(self.id, self.sa_time,
                                      self.sa_cooldown)

    def elim_dead_attackers(self):
        for agresor in self.attackers:
            if not agresor.alive or agresor.target != self:
                self.attackers.remove(agresor)

    def elim_target_nexo(self):
        if isinstance(self.target, Nexo) and self.inhibidor.alive:
            self.target = None

    def left_click(self, target):
        if target:
            if self.sa_target != target:
                self.waiting_sa = False

            self.target = target
            self.d, self.angle = get_angle(self.target.vertices, self.vertices)
            self.vangle = angle_mouse(self.target.center, self.center)

            if self.waiting_sa and self.d <= self.attack_range:
                self.mygame.sa_request(self)
                self.right_click(self.target)
                self.target = None
                self.waiting_sa = False


class MyHero(Hero):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.money_display_signal = self.mygame.money_display_signal
        self.attrs_display_signal = self.mygame.attrs_display_signal

    def set_angle(self, center_obj):
        if not self.target:
            self.angle = angle_mouse(center_obj, self.center)

    def receive_dmg(self, agresor):
        self.dano_recibido += agresor.damage-self.armor
        self.attackers.append(agresor)
        self.mod_life_signal.emit(self.id, self.life, self.tot_life)

    def move(self, key):
        self.target = None
        if key == 'w':
            self.dx = -self.move_speed*self.refresh_rate*cos(self.angle)
            self.dy = self.move_speed*self.refresh_rate*sin(self.angle)
        elif key == 'd':
            self.dx = -self.move_speed*self.refresh_rate*cos(0.5*pi-self.angle)
            self.dy = -self.move_speed*self.refresh_rate*sin(0.5*pi-self.angle)
        elif key == 's':
            self.dx = +self.move_speed*self.refresh_rate*cos(self.angle)
            self.dy = -self.move_speed*self.refresh_rate*sin(self.angle)
        elif key == 'a':
            self.dx = self.move_speed*self.refresh_rate*cos(0.5*pi-self.angle)
            self.dy = self.move_speed*self.refresh_rate*sin(0.5*pi-self.angle)

    def adquirir_item(self, objeto):
        objeto.affect(self)

    def right_click(self, target):
        if self.sa_time >= self.sa_cooldown:
            if self.tipo == 'Chau':
                self.special_attack(self.targets, self)
            elif self.tipo == 'Hernan':
                self.special_attack(self.targets, self)
            elif target:
                self.special_attack(target, self)
                self.sa_target = target

    def ciclo(self):
        self.inhibidor = self.mygame.bot_inhibidor
        self.targets = self.mygame.team_bot
        if not self.mygame.pause:
            # habilidad chau
            if self.freeze > 0:
                self.freeze -= self.refresh_rate
            else:
                # habilidad de franky
                if self.uplife > 0:
                    self.uplife -= self.refresh_rate
                    self.dano_recibido -= 1.5
                    self.mod_life_signal.emit(self.id, self.life,
                                              self.tot_life)
                # habilidad de franky
                if self.downlife > 0:
                    self.downlife -= self.refresh_rate
                    self.dano_recibido += 1.5
                    self.mod_life_signal.emit(self.id, self.life,
                                              self.tot_life)

                # barra mana
                self.cooldown_recovery()

                # eliminar agresores muertos
                self.elim_dead_attackers()

                # inicio de mover el qlabel
                if self.target:
                    # eliminar target nexo si hay inhibidor
                    self.elim_target_nexo()

                    # click event
                    if self.d > self.attack_range:
                        z = self.move_speed*self.refresh_rate
                        self.left_click(self.target)
                        self.dx = -z*cos(self.angle)
                        self.dy = z*sin(self.angle)

                    elif int(self.i % (self.nro_ciclos /
                                       self.attack_speed)) == 0:
                        if not isinstance(self.target, Tienda):
                            self.atacando = True
                            self.attack(self.target)
                            # eliminar target muerto
                            if not self.target.alive:
                                self.money += 1
                                if isinstance(self.target, Hero):
                                    self.money += 4
                                    self.kills += 1
                                elif not isinstance(self.target, Minion):
                                    self.money += 14
                                self.money_display_signal.emit(None)
                                self.attrs_display_signal.emit()
                                self.target = None
                        else:
                            pos = self.mygame.tienda.center
                            self.mygame.click_event(1, pos)
                            self.target = None

                self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)
                # termino de mover el qlabel

                # inicio imagenes
                if self.i % 2 == 0:
                    if self.dx != 0 and self.dy != 0:
                        self.change_img_signal.emit(self.nro_img, self.id,
                                                    self.tipo,
                                                    degrees(self.angle),
                                                    self.team+'_move')
                        self.nro_img += 1
                        if self.nro_img > 6:
                            self.nro_img = 0

                    elif not self.atacando:
                        self.nro_img = 0
                        if hasattr(self, 'vangle') and self.target:
                            self.change_img_signal.emit(self.nro_img, self.id,
                                                        self.tipo,
                                                        degrees(self.vangle),
                                                        self.team+'_move')
                        else:
                            self.change_img_signal.emit(self.nro_img, self.id,
                                                        self.tipo,
                                                        degrees(self.angle),
                                                        self.team+'_move')
                    else:
                        self.change_img_signal.emit(self.img_attack, self.id,
                                                    self.tipo,
                                                    degrees(self.vangle),
                                                    self.team+'_attack')

                        self.img_attack += 1
                        if self.img_attack > 3:
                            self.img_attack = 0
                            self.atacando = False
                # termino imagenes

                self.dx, self.dy = 0, 0
                self.i += 1

        if not self.alive:
            self.mygame.dead_id(self, True)
            self.deaths += 1
            self.stop()


class Bot(Hero):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__escapar = 0

    @property
    def escapar(self):
        return self.__escapar

    @escapar.setter
    def escapar(self, value):
        self.__escapar = value

    def receive_dmg(self, agresor):
        if isinstance(agresor, Tower) and self.target != agresor:
            self.atacando = False
            for thread in self.mygame.team_bot:
                if thread.tipo in ['MinionG', 'MinionN']:
                    if thread.target == agresor:
                        self.atacando = True
                        break
            if not self.atacando:
                self.target = self.mygame.bot_inhibidor
                self.escapar = 4
        self.dano_recibido += agresor.damage-self.armor
        self.attackers.append(agresor)
        self.mod_life_signal.emit(self.id, self.life, self.tot_life)

    def sa(self):
        if (isinstance(self, NormalBot) and
                (self.life >= 0.5*self.tot_life or
                    self.target_hero.life <= 0.5*self.target_hero.tot_life) and
                self.i > 20):

            if self.sa_time >= self.sa_cooldown:
                if self.tipo == 'Chau':
                    self.special_attack(self.targets, self)
                elif self.tipo == 'Hernan':
                    self.special_attack(self.targets, self)
                elif self.target_hero.alive:
                    self.special_attack(self.target_hero, self)
                    self.sa_target = self.target_hero

    def ciclo(self):
        self.targets = self.mygame.team_player
        self.target_hero = self.mygame.hero
        self.inhibidor = self.mygame.inhibidor

        if not self.mygame.pause:
            # habilidad chau
            if self.freeze > 0:
                self.freeze -= self.refresh_rate

            else:
                # habilidad de franky
                if self.uplife > 0:
                    self.uplife -= self.refresh_rate
                    self.dano_recibido -= 1.5
                    self.mod_life_signal.emit(self.id, self.life,
                                              self.tot_life)
                # habilidad de franky
                if self.downlife > 0:
                    self.downlife -= self.refresh_rate
                    self.dano_recibido += 1.5
                    self.mod_life_signal.emit(self.id, self.life,
                                              self.tot_life)
                # barra mana
                self.cooldown_recovery()
                # eliminar agresores muertos
                self.elim_dead_attackers()
                # eliminar target nexo si hay inhibidor
                self.elim_target_nexo()
                # revisar quitter
                if (isinstance(self, RageBot) and
                        self.deaths - self.kills > 3):
                    self.target = None
                else:
                    if self.escapar > 0:
                        self.escapar -= self.refresh_rate
                    else:
                        self.target = self.get_target()

                # ataque especial de bot
                self.sa()

                self.d, self.angle = get_angle(
                    self.target.vertices, self.vertices)
                self.vangle = angle_mouse(self.target.center, self.center)

                if self.d >= self.attack_range:
                    self.dx = -self.move_speed * \
                        self.refresh_rate*cos(self.angle)
                    self.dy = self.move_speed*self.refresh_rate*sin(self.angle)

                elif (int(self.i % (self.nro_ciclos /
                                    self.attack_speed)) == 0):
                    if self.target != self.mygame.bot_inhibidor:
                        self.atacando = True
                        self.attack(self.target)
                        # aumentar kills
                        if not self.target.alive:
                            if isinstance(self.target, Hero):
                                self.kills += 1

                self.pos = (self.pos[0] + self.dx,
                            self.pos[1] + self.dy)
                # imagenes
                if self.i % 2 == 0:
                    if self.dx != 0 and self.dy != 0:
                        self.change_img_signal.emit(self.nro_img, self.id,
                                                    self.tipo,
                                                    degrees(self.vangle),
                                                    self.team+'_move')
                        self.nro_img += 1
                        if self.nro_img > 6:
                            self.nro_img = 0
                    elif not self.atacando:
                        self.nro_img = 0
                        self.change_img_signal.emit(self.nro_img, self.id,
                                                    self.tipo,
                                                    degrees(self.vangle),
                                                    self.team+'_move')

                    else:
                        self.change_img_signal.emit(self.img_attack,
                                                    self.id,
                                                    self.tipo,
                                                    degrees(self.vangle),
                                                    self.team+'_attack')

                        self.img_attack += 1
                        if self.img_attack > 3:
                            self.img_attack = 0
                            self.atacando = False

                # termino imagenes
                self.dx, self.dy = 0, 0
                self.i += 1

        if not self.alive:
            self.mygame.dead_id(self, True)
            self.deaths += 1
            self.stop()


class NoobBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_target(self):
        if len(self.targets) != 0:
            return self.targets[nearest(self.targets, self.vertices)[0][0]]
        else:
            return self.mygame.nexo


class NormalBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_target(self):

        if len(self.targets) != 0:
            attack_inhi = True
            ordenados = nearest(self.targets, self.vertices)

            for x in ordenados:
                posible = self.targets[x[0]]

                if isinstance(posible, Tower):
                    attack_inhi = False
                    for thread in self.mygame.team_bot:
                        if isinstance(thread, Minion):
                            if thread.target == posible:
                                return posible
                else:
                    if isinstance(posible, Inhibidor) and not attack_inhi:
                        continue

                    for thread in self.mygame.team_bot:
                        if (closest_distance(self.vertices,
                                             thread.vertices) <
                                self.attack_range) and thread.id != self.id:
                            return posible

                    if self.life >= 0.2*self.tot_life:
                        return posible
                    if (self.damage > posible.damage and
                            self.life > posible.life):
                        return posible

        return self.mygame.nexo


class RageBot(NormalBot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
