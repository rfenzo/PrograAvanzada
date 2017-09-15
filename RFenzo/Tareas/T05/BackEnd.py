from Campeones import Chau, Hernan, Franky, freeze, earthquake, lifesteal
from Datos import sizes
from Funciones import (get_bot_pos, dot_inside_area)
from Minions import Minion
from Heroes import MyHero, NoobBot, RageBot, NormalBot
from Estructuras import Tower, Nexo, Inhibidor, Tienda
from random import choice
from PyQt5.QtCore import QTimer
from datetime import datetime as dt
from datetime import timedelta as td
import time


class MyGame(QTimer):

    def __init__(self, size, pos_i,
                 refresh_rate, hero_id, move_hero_signal,
                 angle_hero_signal, red_contour_signal, click_signal,
                 cheat_signal, dead_img_signal, ctrl_red_contour_signal,
                 pos_signal_struct, pos_signal_hero,
                 pos_signal_minion, mod_life_signal, mod_cool_signal,
                 new_pos_signal,
                 change_img_signal, attack_graphic, r_attack_graphic,
                 money_display_signal, attrs_display_signal, fin_juego_signal,
                 sa_graphic_signal, rem_sa_graphic_signal, avisar_signal,
                 tienda_show_signal,
                 insuf_money_signal, items_display_signal):
        super().__init__()
        self.timeout.connect(self.ciclo)
        self.start(refresh_rate*1000)

        self.size = size
        self.pos_i = pos_i

        self.dead_img_signal = dead_img_signal
        self.ctrl_red_contour_signal = ctrl_red_contour_signal
        self.pos_signal_struct = pos_signal_struct
        self.pos_signal_hero = pos_signal_hero
        self.pos_signal_minion = pos_signal_minion
        self.mod_life_signal = mod_life_signal
        self.mod_cool_signal = mod_cool_signal
        self.new_pos_signal = new_pos_signal
        self.change_img_signal = change_img_signal
        self.attack_graphic = attack_graphic
        self.r_attack_graphic = r_attack_graphic
        self.money_display_signal = money_display_signal
        self.attrs_display_signal = attrs_display_signal
        self.fin_juego_signal = fin_juego_signal
        self.sa_graphic_signal = sa_graphic_signal
        self.avisar_signal = avisar_signal
        self.tienda_show_signal = tienda_show_signal
        self.insuf_money_signal = insuf_money_signal
        self.items_display_signal = items_display_signal
        self.rem_sa_graphic_signal = rem_sa_graphic_signal

        self.red_contour_signal = red_contour_signal
        self.red_contour_signal.connect(self.mouse_move_event)
        self.click_signal = click_signal
        self.click_signal.connect(self.click_event)
        self.cheat_signal = cheat_signal
        self.cheat_signal.connect(self.check_cheat)

        self.pause = False
        self.refresh_rate = refresh_rate
        # self.areas_ocupadas = {str(i): None for i in range(200)}
        # self.areas_ocupadas['Tienda'] = None
        self.hero, self.hero_bot = self.create_heroes(hero_id)

        self.hero_signals(move_hero_signal, angle_hero_signal)

        self.inicializador()

    def hero_signals(self, move_hero_signal, angle_hero_signal):

        self.move_hero_signal = move_hero_signal
        self.move_hero_signal.connect(self.hero.move)
        self.angle_hero_signal = angle_hero_signal
        self.angle_hero_signal.connect(self.hero.set_angle)

    def inicializador(self):
        # team player
        self.sa_sender = None
        self.tower = Tower(self.attack_graphic, self.r_attack_graphic, self,
                           self.pos_i['Tower'], 'Tower', 'team_player')
        self.nexo = Nexo(self, self.pos_i['Nexo'], 'Nexo', 'team_player')
        self.inhibidor = Inhibidor(self, self.pos_i['Inhibidor'],
                                   'Inhibidor', 'team_player')
        self.team_player = [self.hero, self.tower, self.inhibidor]

        # team bot
        self.bot_nexo = Nexo(self, get_bot_pos('Nexo', self.size,
                                               self.pos_i), 'Nexo',
                             'team_bot')
        self.bot_tower = Tower(self.attack_graphic, self.r_attack_graphic,
                               self, get_bot_pos('Tower', self.size,
                                                 self.pos_i),
                               'Tower', 'team_bot')
        self.bot_inhibidor = Inhibidor(self,
                                       get_bot_pos('Inhibidor', self.size,
                                                   self.pos_i),
                                       'Inhibidor', 'team_bot')
        self.team_bot = [self.hero_bot, self.bot_tower, self.bot_inhibidor]

        self.tienda = Tienda(self)

        self.estructuras = [self.tower, self.bot_tower, self.nexo,
                            self.bot_nexo, self.inhibidor, self.bot_inhibidor]
        self.destruidos = []

        self.nro_sa_img = 0
        self.count_hero = 0
        self.counting_hero = False
        self.count_hero_bot = 0
        self.counting_hero_bot = False
        self.count_inhibidor = 0
        self.counting_inhibidor = False
        self.count_bot_inhibidor = 0
        self.counting_bot_inhibidor = False
        self.stack_sa_img = []
        self.i = 0

    def pausar(self):
        self.pause = not self.pause

    def ir_tienda(self):
        if not self.pause:
            if self.hero.alive:
                self.hero.left_click(self.tienda)
            else:
                self.tienda.show()

    def dead_id(self, thread, revivible):
        if thread in self.team_bot:
            self.team_bot.remove(thread)
            self.dead_img_signal.emit(thread.id, revivible)
            self.ctrl_red_contour_signal.emit(thread.id, False)

        elif thread in self.team_player:
            if isinstance(thread, Tower) or isinstance(thread, Inhibidor):
                self.destruidos.append(thread)
            self.team_player.remove(thread)
            self.dead_img_signal.emit(thread.id, revivible)
            self.ctrl_red_contour_signal.emit(thread.id, False)

        if isinstance(thread, Nexo):
            self.dead_img_signal.emit(thread.id, revivible)
            self.ctrl_red_contour_signal.emit(thread.id, False)

        # self.areas_ocupadas[thread.id] = None

    def create_heroes(self, iden):
        if iden == 1:
            hero = MyHero(self, self.pos_i['Chau'], 'team_player', **Chau)
        elif iden == 2:
            hero = MyHero(self, self.pos_i['Hernan'], 'team_player', **Hernan)
        else:
            hero = MyHero(self, self.pos_i['Franky'], 'team_player', **Franky)

        r_hero = choice([Chau, Hernan, Franky])
        perso = choice(['Noob', 'Normal', 'Ragequitter'])
        print('Personalidad del heroe enemigo: ', perso)
        if perso == 'Noob':
            hero_bot = NoobBot(self,
                               get_bot_pos(r_hero['tipo'], self.size,
                                           self.pos_i),
                               'team_bot', **r_hero)
        elif perso == 'Normal':
            hero_bot = NormalBot(self,
                                 get_bot_pos(r_hero['tipo'], self.size,
                                             self.pos_i),
                                 'team_bot',
                                 **r_hero)
        else:
            hero_bot = RageBot(self,
                               get_bot_pos(r_hero['tipo'], self.size,
                                           self.pos_i),
                               'team_bot',
                               **r_hero)

        return hero, hero_bot

    def create_minions(self):
        pos = self.pos_i['MinionN']
        for i in range(4):
            pos = pos[0]+20*(i+1)*(-1)**i, pos[1]-20*(i+1)*(-1)**i
            minion = Minion(self, pos, 'MinionN', 'team_player')
            self.team_player.append(minion)

        pos = self.pos_i['MinionG']
        minion = Minion(self, pos, 'MinionG', 'team_player')
        self.team_player.append(minion)

        pos = get_bot_pos('MinionN', self.size, self.pos_i)
        for i in range(4):
            pos = pos[0]+20*(i+1)*(-1)**i, pos[1]-20*(i+1)*(-1)**i
            minion = Minion(self, pos, 'MinionN', 'team_bot')
            self.team_bot.append(minion)

        pos = get_bot_pos('MinionG', self.size, self.pos_i)
        minion = Minion(self, pos, 'MinionG', 'team_bot')
        self.team_bot.append(minion)

    def click_event(self, nro_click, pos_mouse):
        if nro_click == 1:
            # revisar click en tienda:
            if dot_inside_area(pos_mouse, self.tienda.center,
                               self.tienda.tamano):
                if self.tienda.allowed:
                    self.tienda.show()

            # hero attack
            for thread in self.team_bot:
                if dot_inside_area(pos_mouse, thread.center, thread.tamano):
                    self.hero.left_click(thread)

            if not self.bot_inhibidor.alive:
                if dot_inside_area(pos_mouse, self.bot_nexo.center,
                                   self.bot_nexo.tamano):
                    self.hero.left_click(self.bot_nexo)

        else:
            # poder especial
            target = None
            for thread in self.team_bot:
                if dot_inside_area(pos_mouse, thread.center, thread.tamano):
                    target = thread
            self.hero.right_click(target)

    def mouse_move_event(self, pos, hidden_ids):
        vivos = [z for z in [self.bot_tower, self.bot_inhibidor] if z.alive]

        for x in vivos:
            if dot_inside_area(pos, x.center, x.tamano):
                if hidden_ids[x.id]:

                    self.ctrl_red_contour_signal.emit(x.id, True)
            else:
                if not hidden_ids[x.id]:
                    self.ctrl_red_contour_signal.emit(x.id, False)

        iden = self.bot_nexo.id
        if (dot_inside_area(pos, self.bot_nexo.center, self.bot_nexo.tamano)
                and not self.bot_inhibidor.alive):
            if hidden_ids[iden]:
                self.ctrl_red_contour_signal.emit(iden, True)
        else:
            if not hidden_ids[iden]:
                self.ctrl_red_contour_signal.emit(iden, False)

    def check_cheat(self, keys):
        if keys == 'lif':
            for thread in self.team_player:
                thread.dano_recibido = 0
                self.mod_life_signal.emit(thread.id, thread.life,
                                          thread.tot_life)
        elif keys == 'ret':
            if not self.hero.alive:
                self.counting_hero = False
                self.hero.revive()
                self.team_player.append(self.hero)
        elif keys == 'rec':
            for _ in range(len(self.destruidos)):
                thread = self.destruidos.pop()
                thread.dano_recibido = thread.tot_life/2
                thread.start()
                thread.pos_signal.emit(thread.pos, thread.tipo,
                                       sizes[thread.tipo], thread.id)
                self.mod_life_signal.emit(thread.id, thread.life,
                                          thread.tot_life)
                self.team_player.append(thread)

    def sa_request(self, thread):
        self.sa_imgs = 3
        if thread.tipo == 'Franky' and hasattr(thread, 'target'):
            self.sa_target = thread.target.pos
        else:
            self.sa_target = (0, 0)
        self.sa_sender = thread

    def ciclo(self):
        if not self.hero.alive:
            if self.counting_hero != True:
                self.counting_hero = True
                self.count_hero = 0
            elif int(self.count_hero % (self.hero.respawn /
                                        self.refresh_rate)) == 0:
                self.counting_hero = False
                self.hero.revive()
                self.team_player.append(self.hero)

        if not self.hero_bot.alive:
            if self.counting_hero_bot != True:
                self.counting_hero_bot = True
                self.count_hero_bot = 0
            elif int(self.count_hero_bot % (self.hero_bot.respawn /
                                            self.refresh_rate)) == 0:
                self.counting_hero_bot = False
                self.hero_bot.revive()
                self.team_bot.append(self.hero_bot)

        if not self.inhibidor.alive:
            if self.counting_inhibidor != True:
                self.counting_inhibidor = True
                self.count_inhibidor = 0
            elif int(self.count_inhibidor % (self.inhibidor.respawn /
                                             self.refresh_rate)) == 0:
                self.counting_inhibidor = False
                self.inhibidor.revive()
                self.team_player.append(self.inhibidor)

        if not self.bot_inhibidor.alive:
            if self.counting_bot_inhibidor != True:
                self.counting_bot_inhibidor = True
                self.count_bot_inhibidor = 0
            elif int(self.count_bot_inhibidor %
                     (self.bot_inhibidor.respawn /
                      self.refresh_rate)) == 0:
                self.counting_bot_inhibidor = False
                self.bot_inhibidor.revive()
                self.team_bot.append(self.bot_inhibidor)

        if self.sa_sender:
            if self.nro_sa_img >= self.sa_imgs:
                self.sa_sender = None
                self.nro_sa_img = 0
            else:
                self.sa_graphic_signal.emit(self.sa_sender.tipo,
                                            self.sa_sender.pos,
                                            self.sa_target,
                                            self.nro_sa_img)
                self.stack_sa_img.append((self.sa_sender.tipo,
                                          self.nro_sa_img))
                self.nro_sa_img += 1

        if len(self.stack_sa_img) != 0 and self.i % 5 == 0:
            self.rem_sa_graphic_signal.emit(*self.stack_sa_img.pop(0))

        if self.i % (10/self.refresh_rate) == 0:
            self.create_minions()

        self.i += 1
        self.count_hero += 1
        self.count_hero_bot += 1
        self.count_inhibidor += 1
        self.count_bot_inhibidor += 1

        if not self.nexo.alive or not self.bot_nexo.alive:
            self.fin_juego_signal.emit(self.nexo.alive)
            for timer in self.team_player:
                timer.end_game()
            for timer in self.team_bot:
                timer.end_game()
            self.inhibidor.end_game()
            self.bot_inhibidor.end_game()
            self.nexo.end_game()
            self.bot_nexo.end_game()
            self.tienda.end_game()
            self.stop()
