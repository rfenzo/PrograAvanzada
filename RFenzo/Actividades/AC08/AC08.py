__author__ = "cotehidalgov"
__coauthor__ = "Diego Andai"
# -*- coding: utf-8 -*-
import random

###############################################################################
# Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
# será penalizada con nota 1.0


class MetaPerson(type):

    def __new__(cls, name, bases, dic):
        bases = (Person,)
        if name == 'Chef':
            def cook(self):
                plato = Plate()
                self.choose_food(plato)
                self.choose_drink(plato)
                return plato
            dic['cook'] = cook
        else:
            def eat(self, plato):
                if (not isinstance(plato.food, Food)):
                    print('Mi plato tiene dos bebidas')
                elif (not isinstance(plato.drink, Drink)):
                    print('Mi plato tiene dos comidas')
                else:
                    calidad = (plato.drink.quality + plato.food.quality)/2
                    if calidad > 50:
                        print('Que delicia!')
                    else:
                        print('Esto no es digno de mi paladar')

            dic['eat'] = eat
        return super().__new__(cls, name, bases, dic)


class MetaRestaurant(type):

    def __new__(meta, name, bases, dic):
        def llega_cliente(self, cliente):
            if isinstance(cliente, Client):
                self.clients.append(cliente)
        dic['llega_cliente'] = llega_cliente

        def cliente_se_va(self, nombre_cliente):
            for cliente in self.clients:
                if cliente.name == nombre_cliente:
                    self.clients.remove(cliente)
        dic['cliente_se_va'] = cliente_se_va

        def start(self):
            if self.clients == []:
                print('{} no tiene clientes, que pena'.format(self.name))
            else:
                for i in range(1):  # Se hace el estudio por 5 dias
                    print("----- Día {} -----".format(i + 1))
                    plates = []
                    for chef in self.chefs:
                        for j in range(3):  # Cada chef cocina 3 platos
                            # Retorna platos de comida y bebida
                            plates.append(chef.cook())

                    for client in self.clients:
                        for plate in plates:
                            client.eat(plate)
        dic['start'] = start

        return super().__new__(meta, name, bases, dic)

    def __call__(cls, *args, **kwargs):
        if len(args) > 2:
            if len(args[1]) > 1:
                for chef in args[1]:
                    chef.restaurant = args[0]
                texto = ''
                for i in args[1]:
                    texto += ' '+i.name
                print('Instanciacion exitosa,' +
                      ' los chefs son:', texto)
                return super().__call__(*args, **kwargs)
        if len(args) == 2:
            return super().__call__(args[0], args[1], [], **kwargs)
        else:
            return super().__call__(args[0], [], [], **kwargs)


###############################################################################
# De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:

    def __init__(self, name):
        self.name = name


class Food:

    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients

    @property
    def quality(self):
        return self._quality * random.random()


class Drink:

    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass=MetaRestaurant):

    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients

    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    # Retorna platos de comida y bebida
                    plates.append(chef.cook())

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):

    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):

    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):

    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):

    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:

    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):

    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(
                    random.choice(
                        ["pepperoni", "piña",
                         "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(
                    random.choice(
                        ["crutones", "espinaca",
                         "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):

    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
               Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()
