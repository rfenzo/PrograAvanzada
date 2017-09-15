class Menu:
    '''
    esta clase es un menu que es utilizado para administrar de mejor forma los 
    inputs del usuario, simplifica el codigo en Simulacion.py
    '''

    def __init__(self, *args):
        '''
        guarda en menu una lista de tuplas, con las opciones y sus numeros

        param *args: son strings que representan las opciones que tiene el 
        usuario | tipo: str

        var menu: lista de tuplas que guardas las opciones.
        '''
        self.menu = []
        k = 1
        for j in args:
            x = []
            x.extend((str(k), j))
            self.menu.append(x)
            k += 1

    def revisar_input(self):
        '''
        revisa que el input ingresado por el usuario sea una opcion factible

        return True si es factible
        return tipo: bool
        '''
        encontrado = False
        for j in self.menu:
            if self.input == j[0]:
                encontrado = True
        return encontrado

    def append(self, numero, opcion):
        '''
        permite agregar opciones manualmente, no solo a travez del init

        param numero: numero de la opcion | tipo: int
        param opcion: texto a desplegar como opcion | tipo: str

        return none
        return tipo none
        '''
        x = []
        x.extend((str(numero), opcion))
        self.menu.append(x)

    def display(self):
        '''
        despliega el menu que se a almacenado en self.menu y espera por un
        input que luego sera revisado por revisar_input

        return none
        return tipo: none
        '''
        # mostrar menu
        print()
        print("Selecciona una opción:\n")
        for j in self.menu:
            print(str(j[0]) + ". " + j[1])

        # revisar input
        self.input = input()
        while not Menu.revisar_input(self):
            print("Error, ingresa un numero correcto\n")
            self.input = input()

    def __eq__(self, other):
        return int(self.input) == other
