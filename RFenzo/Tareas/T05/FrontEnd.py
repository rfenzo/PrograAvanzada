import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QMainWindow,
                             QAction, QVBoxLayout, QHBoxLayout, QPushButton,
                             QDesktopWidget, QGridLayout)
from PyQt5.QtGui import (QIcon, QPixmap, QTransform, QPainter,
                         QFont, QPalette, QBrush, QImage, QTransform)
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QCoreApplication
from PyQt5.QtTest import QTest

from BackEnd import MyGame
from Funciones import item_to_text, move_vertices
from Datos import offsets, real_size
from Estructuras import Objeto
from Minions import Minion


class Menu(QWidget):

    def __init__(self, s):
        super().__init__()
        self.menu_signal = s
        self.iniciador()

    def iniciador(self):
        new_game = QPushButton('Iniciar nueva partida', self)
        new_game.setFixedSize(400, 200)
        new_game.setFont(QFont("times", 20))
        new_game.id = 0
        new_game.clicked.connect(self.option)

        clear_history = QPushButton('Borrar el historial de partidas', self)
        clear_history.setFixedSize(400, 200)
        clear_history.setFont(QFont("times", 20))
        clear_history.id = 1
        clear_history.clicked.connect(self.option)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox1.addStretch()
        hbox1.addWidget(new_game)
        hbox1.addStretch()
        hbox2.addStretch()
        hbox2.addWidget(clear_history)
        hbox2.addStretch()

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def option(self):
        self.menu_signal.emit(self.sender().id)


class MyQLabel(QLabel):

    def __init__(self, x):
        super().__init__(x)
        self.setMouseTracking(True)


class InGame(QWidget):
    dead_img_signal = pyqtSignal(str, bool)
    ctrl_red_contour_signal = pyqtSignal(str, bool)
    pos_signal_struct = pyqtSignal(tuple, str, int, str)
    pos_signal_hero = pyqtSignal(tuple, str, int, str, str)
    pos_signal_minion = pyqtSignal(tuple, str, int, str, str)
    mod_life_signal = pyqtSignal(str, int, int)
    mod_cool_signal = pyqtSignal(str, int, int)
    dead_signal = pyqtSignal(str, bool)
    new_pos_signal = pyqtSignal(str, tuple, bool)
    change_img_signal = pyqtSignal(int, str, str, float, str)
    attack_graphic_signal = pyqtSignal(tuple, float, int, str, str)
    r_attack_graphic_signal = pyqtSignal(str, int)
    money_display_signal = pyqtSignal(str)
    attrs_display_signal = pyqtSignal()
    fin_juego_signal = pyqtSignal(bool)
    sa_graphic_signal = pyqtSignal(str, tuple, tuple, int)
    rem_sa_graphic_signal = pyqtSignal(str, int)

    # tienda
    avisar_signal = pyqtSignal(bool)
    tienda_show_signal = pyqtSignal()
    insuf_money_signal = pyqtSignal()
    actualizar_signal = pyqtSignal()
    items_display_signal = pyqtSignal(Objeto)

    def __init__(self, parent, hero_id):
        super().__init__()
        self.iniciador(parent, hero_id)

    def iniciador(self, parent, hero_id):
        self.dead_img_signal.connect(self.remove_dead_img)
        self.ctrl_red_contour_signal.connect(self.control_red_contour)
        self.pos_signal_struct.connect(self.place_struct)
        self.pos_signal_hero.connect(self.place_hero)
        self.pos_signal_minion.connect(self.place_minion)
        self.mod_life_signal.connect(self.mod_life)
        self.mod_cool_signal.connect(self.mod_cool)
        self.new_pos_signal.connect(self.move)
        self.change_img_signal.connect(self.change_img)
        self.attack_graphic_signal.connect(self.attack_graphic)
        self.r_attack_graphic_signal.connect(self.r_attack_graphic)
        self.money_display_signal.connect(self.act_money)
        self.money_display_signal.connect(self.actualizar_tienda)
        self.sa_graphic_signal.connect(self.sa_graphic)
        self.rem_sa_graphic_signal.connect(self.rem_sa_graphic)
        self.fin_juego_signal.connect(self.end_game)

        # tienda
        self.avisar_signal.connect(self.avisar_tienda)
        self.tienda_show_signal.connect(self.show_tienda)
        self.insuf_money_signal.connect(self.insuf_money)
        self.items_display_signal.connect(self.actualizar_items)
        self.attrs_display_signal.connect(self.actualizar_attrs)

        self.imagenes = {}
        self.imagenes['IMGS/bluebar.png'] = QPixmap('IMGS/bluebar.png')
        self.imagenes['IMGS/emptybar.png'] = QPixmap('IMGS/emptybar.png')
        self.imagenes[
            'IMGS/emptybar_minions.png'] = QPixmap('IMGS/emptybar_minions.png')
        self.imagenes['IMGS/redbar.png'] = QPixmap('IMGS/redbar.png')
        self.imagenes[
            'IMGS/redbar_minions.png'] = QPixmap('IMGS/redbar_minions.png')

        self.refresh_rate = 0.05
        self.setMouseTracking(True)
        self.parent = parent

        fondo = MyQLabel(self)
        img = QPixmap('IMGS/fondo4.jpg')
        self.size = parent.geometry
        razon = self.size[0]/self.size[1]
        img = img.scaled(*self.size)
        fondo.setPixmap(img)

        self.pause = MyQLabel(self)
        img = QPixmap('IMGS/paused.png')
        self.pause.setPixmap(img)
        self.pause.move((self.size[0]-img.width())/2,
                        (self.size[1]-img.height())/2)
        self.pause.hide()

        pos_iniciales = {'Chau': (20, 180), 'Hernan': (20, 180),
                         'Franky': (20, 280),
                         'Tower': (350, 350/razon), 'Nexo': (20, 20/razon),
                         'Inhibidor': (200, 200/razon),
                         'Tienda': (20, 150), 'MinionN': (170, 90),
                         'MinionG': (170, 90)}

        self.game = MyGame(self.size, pos_iniciales,
                           self.refresh_rate, hero_id, parent.move_hero_signal,
                           parent.angle_hero_signal, parent.red_contour_signal,
                           parent.click_signal, parent.cheat_signal,
                           self.dead_img_signal, self.ctrl_red_contour_signal,
                           self.pos_signal_struct, self.pos_signal_hero,
                           self.pos_signal_minion, self.mod_life_signal,
                           self.mod_cool_signal,
                           self.new_pos_signal, self.change_img_signal,
                           self.attack_graphic_signal,
                           self.r_attack_graphic_signal,
                           self.money_display_signal,
                           self.attrs_display_signal, self.fin_juego_signal,
                           self.sa_graphic_signal, self.rem_sa_graphic_signal,
                           self.avisar_signal, self.tienda_show_signal,
                           self.insuf_money_signal,
                           self.items_display_signal)

        self.tienda = Tienda(self)
        # img comprar tienda
        self.tienda_comprar_img = MyQLabel(self)
        img = QPixmap('IMGS/Tienda/message_box.png')
        self.tienda_comprar_img.setPixmap(img)
        pos = self.game.tienda.center
        self.tienda_comprar_img.move(pos[0]+20, pos[1]-80)
        self.tienda_comprar_img.hide()

        # plata actual
        money_label_img = MyQLabel(self)
        img = QPixmap('IMGS/money_background.png')
        money_label_img.setPixmap(img)
        money_label_img.move((self.size[0]-img.width())/2, 0)
        self.money_label = MyQLabel(self)
        self.money_label.setStyleSheet('color: white')
        self.money_label.setFont(QFont("Rockwell", 16))
        self.money_label.setFixedSize(400, 18)
        self.money_label.move((self.size[0]-img.width()+90)/2, 10)
        self.money_label.setText(
            'Dinero disponible: {}'.format(self.game.hero.money))

        # items y status
        status_label_img = MyQLabel(self)
        img = QPixmap('IMGS/status.png')
        status_label_img.setPixmap(img)
        items_esq = (0, self.size[1]-img.height())
        status_label_img.move(*items_esq)

        self.attrs_label = MyQLabel(self)
        self.attrs_label.setFont(QFont("Rockwell", 11))
        self.attrs_label.setStyleSheet('color: white')

        texto = """
        Kills: {}
        Deaths: {}
        Damage: {}
        Attack Speed: {}
        Attack Range: {}
        Movement Speed: {}
        Armor: {}
        SA Cooldown: {}
        """.format(self.game.hero.kills, self.game.hero.deaths,
                   self.game.hero.damage, self.game.hero.attack_speed,
                   self.game.hero.attack_range,
                   self.game.hero.move_speed, self.game.hero.armor,
                   self.game.hero.sa_cooldown)
        self.attrs_label.setText(texto)
        self.attrs_label.move(items_esq[0]+290, items_esq[1]+35)

        self.posiciones = []
        self.posiciones.append((items_esq[0]+40, items_esq[1]+60))
        self.posiciones.append((items_esq[0]+110, items_esq[1]+60))
        self.posiciones.append((items_esq[0]+180, items_esq[1]+60))
        self.posiciones.append((items_esq[0]+40, items_esq[1]+120))
        self.posiciones.append((items_esq[0]+110, items_esq[1]+120))
        self.posiciones.append((items_esq[0]+180, items_esq[1]+120))

        self.startThreads()

    def move(self, iden, pos, heroe=False):
        posx, posy = pos

        obj = getattr(self, 'img_'+iden)
        obj.move(posx, posy)

        # life and cooldown

        lifeemptybar = getattr(self, 'emptylifebar_'+iden)
        x, y = lifeemptybar.offsets
        lifeemptybar.move(posx+x, posy+y)
        redbar = getattr(self, 'redbar_'+iden)
        redbar.move(posx+x+2, posy+y+2)

        if heroe:
            coolemptybar = getattr(self, 'emptycoolbar_'+iden)
            x, y = coolemptybar.offsets
            coolemptybar.move(posx+x, posy+y)
            bluebar = getattr(self, 'bluebar_'+iden)
            bluebar.move(posx+x+2, posy+y+2)

    def sa_graphic(self, tipo, esquina, pos_target, nro_img):
        if not hasattr(self, 'sa_anim_{}_{}'.format(tipo, nro_img)):
            setattr(self, 'sa_anim_{}_{}'.format(tipo, nro_img),
                    MyQLabel(self))

        qlabel = getattr(self, 'sa_anim_{}_{}'.format(tipo, nro_img))
        qlabel.setPixmap(QPixmap('IMGS/{}/sa{}'.format(tipo, nro_img)))

        pos = esquina
        if tipo == 'Franky':
            pos = pos_target
        qlabel.move(*pos)
        qlabel.show()

    def rem_sa_graphic(self, tipo, nro_img):
        getattr(self, 'sa_anim_{}_{}'.format(tipo, nro_img)).hide()

    def end_game(self, win):
        if win:
            self.victory = MyQLabel(self)
            img = QPixmap('IMGS/victory.png')
            self.victory.setPixmap(img)
            self.victory.move((self.size[0]-img.width())/2,
                              (self.size[1]-img.height())/2)
            self.victory.show()
        else:
            self.defeat = MyQLabel(self)
            img = QPixmap('IMGS/defeat.png')
            self.defeat.setPixmap(img)
            self.defeat.move((self.size[0]-img.width())/2,
                             (self.size[1]-img.height())/2)
            self.defeat.show()

    def showpause(self):
        if self.pause.isHidden():
            self.pause.show()
        else:
            self.pause.hide()

    def mod_life(self, iden, life, tot_life):
        if hasattr(self, 'redbar_'+iden):
            barra = getattr(self, 'redbar_'+iden)
            largo = barra.width()*life/tot_life
            img = self.imagenes['IMGS/redbar.png']
            img = img.scaled(largo, 4)
            barra.setPixmap(img)

    def mod_cool(self, iden, sa_time, sa_cooldown):
        if hasattr(self, 'bluebar_'+iden):
            barra = getattr(self, 'bluebar_'+iden)
            largo = barra.width()*sa_time/sa_cooldown
            img = self.imagenes['IMGS/bluebar.png']
            img = img.scaled(largo, 4)
            barra.setPixmap(img)

    def actualizar_items(self, item):
        if not hasattr(self, 'item_'+item.tipo):
            setattr(self, 'item_'+item.tipo, MyQLabel(self))
            qlabel = getattr(self, 'item_'+item.tipo)
            img = QPixmap('IMGS/Tienda/{}.png'.format(
                item.tipo.replace(' ', '_')))
            img = img.scaled(60, 60, Qt.KeepAspectRatio)
            qlabel.setPixmap(img)
            qlabel.pos = self.posiciones.pop(0)
            qlabel.move(*qlabel.pos)

        elif not hasattr(self, 'nro_item_'+item.tipo):
            setattr(self, 'nro_item_'+item.tipo, MyQLabel(self))
            qlabel = getattr(self, 'nro_item_'+item.tipo)
            pos = getattr(self, 'item_'+item.tipo).pos
            qlabel.nro = 2
            qlabel.setFont(QFont("Sheeping Dogs", 15))
            qlabel.setStyleSheet('color: white')
            qlabel.setText('x'+str(qlabel.nro))
            qlabel.move(pos[0]+40, pos[1]+40)
        else:
            qlabel = getattr(self, 'nro_item_'+item.tipo)
            qlabel.nro += 1
            qlabel.setFont(QFont("Sheeping Dogs", 15))
            qlabel.setStyleSheet('color: white')
            qlabel.setText('x'+str(qlabel.nro))

        qlabel.show()

    def remove_dead_img(self, iden, revivible):
        getattr(self, 'img_'+iden).hide()
        getattr(self, 'emptylifebar_'+iden).hide()
        getattr(self, 'redbar_'+iden).hide()

        if hasattr(self, 'emptycoolbar_'+iden):
            getattr(self, 'emptycoolbar_'+iden).hide()
            getattr(self, 'bluebar_'+iden).hide()

        if not revivible:
            delattr(self, 'img_'+iden)
            delattr(self, 'emptylifebar_'+iden)
            delattr(self, 'redbar_'+iden)

    def change_img(self, nro_img, iden, carpeta, angle, tipo_img):
        obj = getattr(self, 'img_'+iden)
        path = 'IMGS/{}/{}{}.png'.format(carpeta, tipo_img, nro_img)
        if path not in self.imagenes:
            img = QPixmap(path)
            img = img.scaled(obj.tamano, obj.tamano, Qt.KeepAspectRatio)
            self.imagenes[path] = img
        else:
            img = self.imagenes[path]

        angle = round(360-angle)
        key = path+str(angle)
        if key not in self.imagenes:
            img = img.transformed(QTransform().rotate(angle),
                                  Qt.SmoothTransformation)
            self.imagenes[key] = img
        else:
            img = self.imagenes[key]

        obj.setPixmap(img)

    def place_red_contour(self, pos, tipo, size, iden):
        self.parent.identificators.append(iden)
        setattr(self, 'red_contour_{}'.format(iden), MyQLabel(self))
        x = getattr(self, 'red_contour_{}'.format(iden), MyQLabel(self))
        img = QPixmap('IMGS/{}_mouse.png'.format(tipo))
        img = img.scaled(size, size, Qt.KeepAspectRatio)
        x.setPixmap(img)
        x.move(*pos)
        x.hide()

    def control_red_contour(self, iden, show):
        if show:
            getattr(self, 'red_contour_{}'.format(iden), MyQLabel(self)).show()
        else:
            getattr(self, 'red_contour_{}'.format(iden), MyQLabel(self)).hide()

    def attack_graphic(self, pos, angle, nro_img, carpeta, iden):
        path = 'IMGS/{}/attack_graphic{}.png'.format(carpeta, nro_img)
        if path not in self.imagenes:
            img = QPixmap(path)
            self.imagenes[path] = img
        else:
            img = self.imagenes[path]

        if not hasattr(self, 'attack_anim{}_{}'.format(nro_img, iden)):
            setattr(self, 'attack_anim{}_{}'.format(nro_img, iden),
                    MyQLabel(self))
            qlabel = getattr(self, 'attack_anim{}_{}'.format(nro_img, iden))
            diag = (img.width()**2 + img.height()**2)**0.5
            qlabel.setMinimumSize(diag, diag)
            qlabel.setAlignment(Qt.AlignCenter)
        else:
            qlabel = getattr(self, 'attack_anim{}_{}'.format(nro_img, iden))

        angle = round(360-angle)
        key = path+str(angle)
        if key not in self.imagenes:
            img = img.transformed(QTransform().rotate(angle),
                                  Qt.SmoothTransformation)
            self.imagenes[key] = img
        else:
            img = self.imagenes[key]

        qlabel.setPixmap(img)
        qlabel.move(*pos)
        qlabel.show()

    def r_attack_graphic(self, iden, nro_img):
        getattr(self, 'attack_anim{}_{}'.format(nro_img, iden)).hide()

    def place_hero(self, pos, tipo, size, iden, team):
        setattr(self, 'img_'+iden, MyQLabel(self))
        qlabel = getattr(self, 'img_'+iden)
        qlabel.tamano = size
        img = QPixmap('IMGS/{}/{}_move0.png'.format(tipo, team))
        img = img.scaled(size, size, Qt.KeepAspectRatio)
        diag = (img.width()**2 + img.height()**2)**0.5
        qlabel.setMinimumSize(diag, diag)
        qlabel.setAlignment(Qt.AlignCenter)
        qlabel.setPixmap(img)
        qlabel.move(*pos)
        qlabel.show()

        setattr(self, 'emptylifebar_'+iden, MyQLabel(self))
        img = self.imagenes['IMGS/emptybar.png']
        qlabel = getattr(self, 'emptylifebar_'+iden)
        qlabel.setPixmap(img)
        x, y = offsets[tipo]
        qlabel.offsets = (x, y)
        qlabel.move(pos[0]+x, pos[1]+y)
        qlabel.show()

        setattr(self, 'redbar_'+iden, MyQLabel(self))
        img = self.imagenes['IMGS/redbar.png']
        qlabel = getattr(self, 'redbar_'+iden)
        qlabel.setPixmap(img)
        qlabel.move(pos[0]+x+2, pos[1]+y+2)
        qlabel.show()

        setattr(self, 'emptycoolbar_'+iden, MyQLabel(self))
        img = self.imagenes['IMGS/emptybar.png']
        qlabel = getattr(self, 'emptycoolbar_'+iden)
        qlabel.setPixmap(img)
        x, y = offsets[tipo]
        qlabel.offsets = (x, y+6)
        qlabel.move(pos[0]+x, pos[1]+y+6)
        qlabel.show()

        setattr(self, 'bluebar_'+iden, MyQLabel(self))
        img = self.imagenes['IMGS/bluebar.png']
        qlabel = getattr(self, 'bluebar_'+iden)
        qlabel.setPixmap(img)
        qlabel.move(pos[0]+x+2, pos[1]+y+8)
        qlabel.show()

    def place_struct(self, pos, tipo, size, iden):
        setattr(self, 'img_'+iden, MyQLabel(self))
        qlabel = getattr(self, 'img_'+iden)
        img = QPixmap('IMGS/{}.png'.format(tipo))
        img = img.scaled(size, size, Qt.KeepAspectRatio)
        qlabel.setPixmap(img)

        qlabel.move(*pos)
        qlabel.show()

        if tipo != 'Tienda':
            self.place_red_contour(pos, tipo, size, iden)
            setattr(self, 'emptylifebar_'+iden, MyQLabel(self))
            img = self.imagenes['IMGS/emptybar.png']
            qlabel = getattr(self, 'emptylifebar_'+iden)
            qlabel.setPixmap(img)
            x, y = offsets[tipo]
            qlabel.offsets = (x, y)
            qlabel.move(pos[0]+x, pos[1]+y)
            qlabel.show()

            setattr(self, 'redbar_'+iden, MyQLabel(self))
            img = self.imagenes['IMGS/redbar.png']
            qlabel = getattr(self, 'redbar_'+iden)
            qlabel.setPixmap(img)
            qlabel.move(pos[0]+x+2, pos[1]+y+2)
            qlabel.show()

    def place_minion(self, pos, tipo, size, iden, team):
        setattr(self, 'img_'+iden, MyQLabel(self))
        qlabel = getattr(self, 'img_'+iden)
        qlabel.tamano = size

        path = 'IMGS/{}/{}_move0.png'.format(tipo, team)
        if path not in self.imagenes:
            img = QPixmap(path)
            img = img.scaled(size, size, Qt.KeepAspectRatio)
            self.imagenes[path] = img
        else:
            img = self.imagenes[path]

        diag = (img.width()**2 + img.height()**2)**0.5
        qlabel.setMinimumSize(diag, diag)
        qlabel.setAlignment(Qt.AlignCenter)
        qlabel.setPixmap(img)
        qlabel.move(*pos)
        qlabel.show()

        setattr(self, 'emptylifebar_'+iden, MyQLabel(self))
        img = self.imagenes['IMGS/emptybar_minions.png']
        qlabel = getattr(self, 'emptylifebar_'+iden)
        qlabel.setPixmap(img)
        x, y = offsets[tipo]
        qlabel.offsets = (x, y)
        qlabel.move(pos[0]+x, pos[1]+y)
        qlabel.show()

        setattr(self, 'redbar_'+iden, MyQLabel(self))
        img = self.imagenes['IMGS/redbar_minions.png']
        qlabel = getattr(self, 'redbar_'+iden)
        qlabel.setPixmap(img)
        x, y = offsets[tipo]
        qlabel.move(pos[0]+x+2, pos[1]+y+2)
        qlabel.show()

    def startThreads(self):
        self.game.start()
        self.game.hero.start()
        self.game.hero_bot.start()
        self.game.tienda.start()
        for thread in self.game.estructuras:
            thread.start()

    def avisar_tienda(self, bool):
        if bool:
            self.tienda_comprar_img.show()
        else:
            self.tienda_comprar_img.hide()

    def show_tienda(self):
        self.tienda.show()

    def insuf_money(self):
        self.tienda.dinero.setText('No tienes suficiente dinero')
        QTest.qWait(2000)
        self.tienda.dinero.setText('Dinero disponible: {}'
                                   .format(self.game.hero.money))

    def actualizar_tienda(self, attr):
        self.tienda.actualizar(attr)

    def actualizar_attrs(self):
        texto = """
        Kills: {}
        Deaths: {}
        Damage: {}
        Attack Speed: {}
        Attack Range: {}
        Movement Speed: {}
        Armor: {}
        SA Cooldown: {}
        """.format(self.game.hero.kills, self.game.hero.deaths,
                   self.game.hero.damage, self.game.hero.attack_speed,
                   self.game.hero.attack_range,
                   self.game.hero.move_speed, self.game.hero.armor,
                   self.game.hero.sa_cooldown)

        self.attrs_label.setText(texto)
        self.attrs_label.show()

    def act_money(self):
        self.money_label.setText(
            'Dinero disponible: {}'.format(self.game.hero.money))


class Tienda(QWidget):
    tienda_buy_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.iniciador(parent)

    def iniciador(self, parent):
        self.parent = parent
        self.items = parent.game.tienda.items
        self.tienda_buy_signal.connect(parent.game.tienda.comprar)
        buyicon = QIcon('IMGS/Tienda/buy.png')

        vbox = QVBoxLayout()

        hbox0 = QHBoxLayout()
        self.dinero = QLabel('Dinero disponible: {}'
                             .format(parent.game.hero.money))
        hbox0.addWidget(self.dinero)
        hbox0.setAlignment(Qt.AlignCenter)

        hbox1 = QHBoxLayout()
        weap1 = QLabel()
        img = QPixmap('IMGS/Tienda/arma_de_mano.png')
        img = img.scaled(120, 120, Qt.KeepAspectRatio)
        weap1.setPixmap(img)
        self.info1 = QLabel(item_to_text(
            'Arma de mano', self.items['Arma de mano']))
        self.buy1 = QPushButton()
        self.buy1.text = 'Arma de mano'
        self.buy1.setIcon(buyicon)
        self.buy1.setIconSize(QSize(60, 60))
        self.buy1.setFixedSize(60, 60)
        self.buy1.clicked.connect(self.objeto_clickeado)
        hbox1.addWidget(weap1)
        hbox1.addWidget(self.info1)
        hbox1.addWidget(self.buy1)

        hbox2 = QHBoxLayout()
        weap2 = QLabel()
        img = QPixmap('IMGS/Tienda/arma_de_distancia.png')
        img = img.scaled(120, 120, Qt.KeepAspectRatio)
        weap2.setPixmap(img)
        self.info2 = QLabel(item_to_text('Arma de distancia',
                                         self.items['Arma de distancia']))
        self.buy2 = QPushButton()
        self.buy2.text = 'Arma de distancia'
        self.buy2.setIcon(buyicon)
        self.buy2.setIconSize(QSize(60, 60))
        self.buy2.setFixedSize(60, 60)
        self.buy2.clicked.connect(self.objeto_clickeado)
        hbox2.addWidget(weap2)
        hbox2.addWidget(self.info2)
        hbox2.addWidget(self.buy2)

        hbox3 = QHBoxLayout()
        weap3 = QLabel()
        img = QPixmap('IMGS/Tienda/botas.png')
        img = img.scaled(120, 120, Qt.KeepAspectRatio)
        weap3.setPixmap(img)
        self.info3 = QLabel(item_to_text('Botas', self.items['Botas']))
        self.buy3 = QPushButton()
        self.buy3.text = 'Botas'
        self.buy3.setIcon(buyicon)
        self.buy3.setIconSize(QSize(60, 60))
        self.buy3.setFixedSize(60, 60)
        self.buy3.clicked.connect(self.objeto_clickeado)
        hbox3.addWidget(weap3)
        hbox3.addWidget(self.info3)
        hbox3.addWidget(self.buy3)

        hbox4 = QHBoxLayout()
        weap4 = QLabel()
        img = QPixmap('IMGS/Tienda/baculo.png')
        img = img.scaled(120, 120, Qt.KeepAspectRatio)
        weap4.setPixmap(img)
        self.info4 = QLabel(item_to_text('Baculo', self.items['Baculo']))
        self.buy4 = QPushButton()
        self.buy4.text = 'Baculo'
        self.buy4.setIcon(buyicon)
        self.buy4.setIconSize(QSize(60, 60))
        self.buy4.setFixedSize(60, 60)
        self.buy4.clicked.connect(self.objeto_clickeado)
        hbox4.addWidget(weap4)
        hbox4.addWidget(self.info4)
        hbox4.addWidget(self.buy4)

        hbox5 = QHBoxLayout()
        weap5 = QLabel()
        img = QPixmap('IMGS/Tienda/armadura.png')
        img = img.scaled(120, 120, Qt.KeepAspectRatio)
        weap5.setPixmap(img)
        self.info5 = QLabel(item_to_text('Armadura', self.items['Armadura']))
        self.buy5 = QPushButton()
        self.buy5.text = 'Armadura'
        self.buy5.setIcon(buyicon)
        self.buy5.setIconSize(QSize(60, 60))
        self.buy5.setFixedSize(60, 60)
        self.buy5.clicked.connect(self.objeto_clickeado)
        hbox5.addWidget(weap5)
        hbox5.addWidget(self.info5)
        hbox5.addWidget(self.buy5)

        hbox6 = QHBoxLayout()
        weap6 = QLabel()
        img = QPixmap('IMGS/Tienda/earthstone.png')
        img = img.scaled(120, 120, Qt.KeepAspectRatio)
        weap6.setPixmap(img)
        self.info6 = QLabel(item_to_text(
            'Earthstone', self.items['Earthstone']))
        self.buy6 = QPushButton()
        self.buy6.text = 'Earthstone'
        self.buy6.setIcon(buyicon)
        self.buy6.setIconSize(QSize(60, 60))
        self.buy6.setFixedSize(60, 60)

        self.buy6.clicked.connect(self.objeto_clickeado)
        hbox6.addWidget(weap6)
        hbox6.addWidget(self.info6)
        hbox6.addWidget(self.buy6)

        hbox7 = QHBoxLayout()
        self.close = QPushButton('Leave Shop')
        self.close.text = 'Leave Shop'
        self.close.clicked.connect(self.objeto_clickeado)
        hbox7.addWidget(self.close)

        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        self.setFixedSize(450, 750)
        self.setWindowTitle('Tienda')
        self.setLayout(vbox)

    def objeto_clickeado(self):
        text = self.sender().text
        if text == 'Leave Shop':
            self.hide()
        else:
            self.tienda_buy_signal.emit(text)

    def actualizar(self, attr_earthstone):
        self.dinero.setText('Dinero disponible: {}'
                            .format(self.parent.game.hero.money))
        self.info1.setText(item_to_text(
            'Arma de mano', self.items['Arma de mano']))
        self.info2.setText(item_to_text('Arma de distancia',
                                        self.items['Arma de distancia']))
        self.info3.setText(item_to_text('Botas', self.items['Botas']))
        self.info4.setText(item_to_text('Baculo', self.items['Baculo']))
        self.info5.setText(item_to_text('Armadura', self.items['Armadura']))
        text = item_to_text('Earthstone', self.items['Earthstone'])
        if attr_earthstone:
            text += '\nLast effect on {}'.format(attr_earthstone)
        self.info6.setText(text)


class ChooseHero(QWidget):

    def __init__(self, s):
        super().__init__()
        self.choose_signal = s
        self.iniciador()

    def iniciador(self):
        # self.showMaximized()
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        choose = QLabel('Choose Wisely')
        choose.setAlignment(Qt.AlignCenter)
        choose.setFont(QFont("times", 30))
        vbox.addWidget(choose)

        franky, chau, hernan = QLabel(
            'FRANKY'), QLabel('CHAU'), QLabel('HERNAN')
        franky.setAlignment(Qt.AlignCenter)
        franky.setFont(QFont("times", 20))
        chau.setAlignment(Qt.AlignCenter)
        chau.setFont(QFont("times", 20))
        hernan.setAlignment(Qt.AlignCenter)
        hernan.setFont(QFont("times", 20))
        hbox1.addWidget(franky)
        hbox1.addWidget(chau)
        hbox1.addWidget(hernan)

        vbox.addLayout(hbox1)

        i = 0
        for text in ['Franky', 'Chau', 'Hernan']:
            hero = QPushButton('', self)
            hero.setIcon(QIcon("IMGS/{}/team_player_move0.png".format(text)))
            hero.setIconSize(QSize(400, 400))
            hero.id = i
            hero.clicked.connect(self.opcion)
            hbox2.addWidget(hero)
            i += 1

        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def opcion(self):
        self.choose_signal.emit(self.sender().id)


class MainWindow(QMainWindow):
    menu_signal = pyqtSignal(int)
    choose_signal = pyqtSignal(int)
    move_hero_signal = pyqtSignal(str)
    angle_hero_signal = pyqtSignal(tuple)
    click_signal = pyqtSignal(int, tuple)
    red_contour_signal = pyqtSignal(tuple, dict)
    cheat_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.iniciador()

    def iniciador(self):
        self.setWindowTitle('League of Progra')
        x = QDesktopWidget().screenGeometry()
        self.geometry = (x.width()*0.85, x.height()*0.85)
        self.setFixedSize(*self.geometry)

        self.pressed_keys = []
        self.identificators = []
        self.setMouseTracking(True)

        self.menu_signal.connect(self.menu)

        menu = Menu(self.menu_signal)
        self.setCentralWidget(menu)

    def menu(self, id):
        if id == 0:
            self.choose_signal.connect(self.start_game)
            self.choose_hero = ChooseHero(self.choose_signal)
            self.setCentralWidget(self.choose_hero)

        else:
            print('clear history')

    def start_game(self, hero_id):
        self.ingame = InGame(self, hero_id)
        self.setCentralWidget(self.ingame)

        menubar = self.menuBar()
        salir = QAction('Salir', self)
        salir.triggered.connect(QCoreApplication.instance().quit)
        tienda = QAction('Tienda', self)
        tienda.setShortcut('O')
        tienda.triggered.connect(self.ingame.game.ir_tienda)
        pause = QAction('Pausar', self)
        pause.setShortcut('P')
        pause.triggered.connect(self.ingame.game.pausar)
        pause.triggered.connect(self.ingame.showpause)

        menubar.addAction(tienda)
        menubar.addAction(pause)
        menubar.addAction(salir)

    def keyPressEvent(self, event):
        self.firstrelease = True
        key = event.text()
        self.pressed_keys.append(key)
        x = ''.join(self.pressed_keys[-3:])
        self.cheat_signal.emit(x)

        if key in 'asdw':
            self.move_hero_signal.emit(key)
        if key == 'i':
            if len(self.pressed_keys) > 1:
                if self.pressed_keys[-2] != 'l':
                    QCoreApplication.instance().quit()
            else:
                QCoreApplication.instance().quit()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.NoButton:
            hiddens_iden = {}
            for iden in self.identificators:
                x = getattr(self.ingame,
                            'red_contour_{}'.format(iden)).isHidden()
                hiddens_iden[iden] = x
            self.angle_hero_signal.emit((event.x(), event.y()))
            self.red_contour_signal.emit((event.x(), event.y()), hiddens_iden)

    def mousePressEvent(self, event):
        self.click_signal.emit(event.button(), (event.x(), event.y()))

if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
