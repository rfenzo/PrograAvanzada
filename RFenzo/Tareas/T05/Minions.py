from UnidadesBase import UnitTimer
from Funciones import (nearest, get_angle, angle_mouse, closest_distance,
                       proyectile_pos)
from math import sin, cos, degrees, radians


class Minion(UnitTimer):

    def __init__(self, *args):
        super().__init__(*args)

        if self.team == 'team_bot':
            self.inhibidor = self.mygame.bot_inhibidor
            self.targets = self.mygame.team_player
            self.hero = self.mygame.hero_bot
            self.nexo = self.mygame.nexo
            self.inhi = self.mygame.inhibidor

        else:
            self.inhibidor = self.mygame.inhibidor
            self.targets = self.mygame.team_bot
            self.hero = self.mygame.hero
            self.nexo = self.mygame.bot_nexo
            self.inhi = self.mygame.bot_inhibidor

        self.move_speed = 40  # 8
        self.attack_speed = 1
        self.respawn = 10

        if self.tipo == 'MinionN':
            self.attack_range = 5
        else:
            self.attack_range = 20

        if self.team == 'team_player':
            self.inhibidor = self.mygame.bot_inhibidor
            self.hero = self.mygame.hero
        else:
            self.inhibidor = self.mygame.inhibidor
            self.hero = self.mygame.hero_bot

        self.stack_img_attack = []

    @property
    def tot_life(self):
        if self.tipo == 'MinionN':
            return 45
        elif self.inhibidor.alive:
            return 60
        return 120

    @property
    def life(self):
        return self.tot_life - self.dano_recibido

    @property
    def damage(self):
        if self.tipo == 'MinionN':
            return 2
        elif self.inhibidor.alive:
            return 4
        # self.minion_power_signal.emit()
        return 10

    def receive_dmg(self, agresor):
        self.dano_recibido += agresor.damage
        self.mod_life_signal.emit(self.id, self.life, self.tot_life)

    def get_target(self):
        # defender heroe
        if len(self.hero.attackers) > 0:
            for attacker in self.hero.attackers:
                if (closest_distance(self.vertices, attacker.vertices) <
                        self.attack_range):
                    return attacker

        # atacar mas cercano
        if len(self.targets) != 0:
            nro, dist = nearest(self.targets, self.vertices)[0]

            if dist < self.attack_range+100:
                return self.targets[nro]
            elif self.inhi.alive:
                return self.inhi

        return self.nexo

    def ciclo(self):
        # habilidad chau
        if not self.mygame.pause:
            if self.freeze > 0:
                self.freeze -= self.refresh_rate
            else:
                # habilidad franky
                if self.downlife > 0:
                    self.downlife -= self.refresh_rate
                    self.dano_recibido += 1.5

                self.dx, self.dy = 0, 0

                self.target = self.get_target()

                d, angle = get_angle(self.target.vertices, self.vertices)
                vangle = angle_mouse(self.target.center, self.center)

                if d >= self.attack_range:
                    self.dx = -self.move_speed*self.refresh_rate*cos(angle)
                    self.dy = self.move_speed*self.refresh_rate*sin(angle)
                else:
                    if (int(self.i % (self.nro_ciclos /
                                      self.attack_speed)) == 0):
                        self.attack(self.target)
                        self.atacando = True

                self.pos = (self.pos[0] + self.dx,
                            self.pos[1] + self.dy)

                # imagenes
                if self.i % 2 == 0:

                    if self.dx != 0 and self.dy != 0:
                        self.change_img_signal.emit(self.nro_img, self.id,
                                                    self.tipo, degrees(
                                                        vangle),
                                                    self.team+'_move')
                        self.nro_img += 1
                        if self.nro_img > 6:
                            self.nro_img = 0

                    elif not self.atacando or self.img_attack > 3:
                        self.nro_img = 0
                        self.img_attack = 0
                        self.atacando = False
                        self.change_img_signal.emit(self.nro_img, self.id,
                                                    self.tipo, degrees(
                                                        vangle),
                                                    self.team+'_move')
                    else:
                        x, y = self.target.center
                        pos = (x-35, y-35)

                        if self.tipo == 'MinionN':
                            if self.img_attack == 2:

                                self.attack_graphic.emit(pos,
                                                         degrees(vangle),
                                                         0, self.tipo,
                                                         self.id)
                                self.stack_img_attack.append((self.id, 0))
                            text = self.team+'_attack'
                            self.change_img_signal.emit(self.img_attack,
                                                        self.id,
                                                        self.tipo,
                                                        degrees(vangle),
                                                        text)

                        elif self.tipo == 'MinionG':
                            if self.img_attack == 0:
                                pos = proyectile_pos(self.target.center,
                                                     self.center, 70)

                            self.attack_graphic.emit(pos, degrees(vangle),
                                                     self.img_attack,
                                                     self.tipo,
                                                     self.id)
                            self.stack_img_attack.append((self.id,
                                                          self.img_attack))

                        self.img_attack += 1

                # remover de imagen de ataque
                if len(self.stack_img_attack) != 0 and self.i % 5 == 0:
                    self.r_attack_graphic.emit(*self.stack_img_attack.pop(0))

                self.i += 1

            if not self.alive:
                self.mygame.dead_id(self, False)
                self.stop()
