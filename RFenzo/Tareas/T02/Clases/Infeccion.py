class Infeccion:
    def __init__(self,tipo):
        self.tipo = tipo

    @property
    def contagiosidad(self):
        if self.tipo == "Virus":
            return 1.5
        elif self.tipo == "Bacteria":
            return 1.
        else:
            return 0.5

    @property
    def mortalidad(self):
        if self.tipo == "Virus":
            return 1.2
        elif self.tipo == "Bacteria":
            return 1.
        else:
            return 1.5

    @property
    def resistencia_a_medicina(self):
        if self.tipo == "Virus":
            return 1.5
        elif self.tipo == "Bacteria":
            return 0.5
        else:
            return 1.

    @property
    def visibilidad(self):
        if self.tipo == "Virus":
            return 0.5
        elif self.tipo == "Bacteria":
            return 0.7
        else:
            return 0.45