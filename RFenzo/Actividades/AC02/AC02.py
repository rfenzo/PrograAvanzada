__author__ = "cotehidalgov"

#Herencia
# -*- coding: utf-8 -*-

import random
from abc import ABCMeta, abstractmethod


class Plate:
	def __init__(self, food, drink):
		self.food = food
		self.drink = drink


class Food(metaclass=ABCMeta):
	def __init__(self, ingredients=[]):
		self.calidad = random.randint(50,200)
		self.ingredients = ingredients

	def check_ingredients(self):
		for ing in self.ingredients:
			if ing == "pepperoni":
				self.calidad += 50
			if ing == "piña":
				self.calidad -= 50
			if ing == "crutones":
				self.calidad += 20
			if ing == "manzana":
				self.calidad -= 20

	def check_time(self, tiempo):
		if tiempo >= 30:
			self.calidad -= 30


class Pizza(Food):
	def __init__(self):
		super().__init__()
		self.tiempo = random.randint(20,100)
		self.check_time(self.tiempo)
		#self.calidad = super().calidad
		#self.ingredients = super().ingredients
		self.ingredients.append('queso')
		self.ingredients.append('salsa de tomate')


class Salad(Food):
	def __init__(self):
		super().__init__()
		self.tiempo = random.randint(5,60)
		self.check_time(self.tiempo)


class Drink(metaclass=ABCMeta):
	def __init__(self):
		self.calidad = random.randint(50,150)


class Juice(Drink):
	def __init__(self):
		super().__init__()
		self.calidad = self.calidad + 30


class Soda(Drink):
	def __init__(self):
		super().__init__()
		self.calidad = self.calidad - 30


class Person(metaclass=ABCMeta): # Solo los clientes tienen personalidad en esta actividad
	def __init__(self, name):
		self.name = name


class Client(Person):
	def __init__(self, nombre, personalidad):
		self.nombre = nombre
		self.personalidad = personalidad

	def eat(self,plate):
		self.personalidad.react(plate)


class Personality(metaclass=ABCMeta):
	def react(self, plate):
		calidad = (plate.food.calidad + plate.drink.calidad) / 2
		if calidad >= 100:
			self.im_happy()
		else:
			self.im_mad()

	@abstractmethod
	def im_happy(self):
		pass

	@abstractmethod
	def im_mad(self):
		pass


class Cool(Personality):
	def im_happy(self):
		print("Yumi! Que rico")

	def im_mad(self):
		print("Preguntaré si puedo cambiar el plato")


class Hater(Personality):
	def im_happy(self):
		print("No está malo, pero igual prefiero Pizza x2")

	def im_mad(self):
		print("Nunca más vendré a Daddy Juan's!")


class Chef(Person):
	def __init__(self, nombre):
		self.nombre = nombre
		self.plato = Plate('', '')
		self.opciones_pizza = ['pepperoni', 'piña', 'cebolla', 'tomate', 'jamon', 'pollo']
		self.opciones_salad = ['crutones', 'espinaca', 'manzana', 'zanahoria']

	def cook(self):
		if random.randint(1,2) == 1:
			self.plato.food = Pizza()
			a = random.randint(0,5)
			self.plato.food.ingredients.append(self.opciones_pizza[a])
			a = random.randint(0, 5)
			self.plato.food.ingredients.append(self.opciones_pizza[a])
			a = random.randint(0, 5)
			self.plato.food.ingredients.append(self.opciones_pizza[a])
		else:
			self.plato.food = Salad()
			a = random.randint(0,3)
			self.plato.food.ingredients.append(self.opciones_salad[a])
			a = random.randint(0, 3)
			self.plato.food.ingredients.append(self.opciones_salad[a])
		if random.randint(1,2) == 1:
			self.plato.drink = Juice()
		else:
			self.plato.drink = Soda()
		return self.plato


class Restaurant:
	def __init__(self, chefs, clients):
		self.chefs = chefs
		self.clients = clients

	def start(self):
		for i in range(3): # Se hace el estudio por 3 dias
			print("----- Día {} -----".format(i + 1))
			plates = []
			for chef in self.chefs: 
				for j in range(3):  # Cada chef cocina 3 platos
					plates.append(chef.cook()) # Retorna platos de comida y bebida

			for client in self.clients:
				for plate in plates:
					client.eat(plate)



if __name__ == '__main__':
	chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]
	clients = [Client("Bastian", Hater()), Client("Flori", Cool()), 
				Client("Antonio", Hater()), Client("Felipe", Cool())]

	restaurant = Restaurant(chefs, clients)
	restaurant.start()





