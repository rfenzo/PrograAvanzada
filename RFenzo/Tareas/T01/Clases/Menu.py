class Menu:

    def __init__(self, *args):
        self.menu = []
        k = 1
        for j in args:
            x = []
            x.extend((str(k), j))
            self.menu.append(x)
            k += 1

    def revisar_input(self):
        encontrado = False
        for j in self.menu:
            if self.input == j[0]:
                encontrado = True
        return encontrado

    def append(self, numero, opcion):  # permite agregar opciones manualmente
        x = []
        x.extend((str(numero), opcion))
        self.menu.append(x)
        return ""

    def display(self):
        # mostrar menu
        print("Selecciona una opción:\n")
        for j in self.menu:
            print(str(j[0]) + ". " + j[1])

        # revisar input
        self.input = (input())
        while not Menu.revisar_input(self):
            print("Error, ingresa un numero correcto\n")
            self.input = (input())

        return ""

    def __eq__(self, other):
        return int(self.input) == other
