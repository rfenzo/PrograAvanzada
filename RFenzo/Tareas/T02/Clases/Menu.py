from EstructurasDeDatos.DiccionarioOrdenado import DiccionarioOrdenado
class Menu():
    def __init__(self,*args):
        self.menu = DiccionarioOrdenado()
        i = 1
        for opcion in args:
            self.menu.append(str(i),opcion)
            i+=1

    def revisar_input(self):
        encontrado = False
        for nro,opcion in self.menu:
            if self.input == nro:
                encontrado = True
        return encontrado

    def display(self):
        # mostrar menu
        print("Selecciona una opción:\n")
        for nro,opcion in self.menu:
            print(nro + ". " + opcion)

        # revisar input
        self.input = (input())
        while not Menu.revisar_input(self):
            print("Error, ingresa un numero correcto\n")
            self.input = (input())

        return self.menu[self.input]

    def append(self, numero, opcion):  # permite agregar opciones manualmente
        self.menu.append(numero,opcion)
        return opcion

    def __eq__(self, other):
        return int(self.input) == other