class User:

    def __init__(self, iden, username, puntaje):
        self.type = 'account'
        self.id = iden
        self.username = username
        self.puntaje = puntaje
        self.aciertos_salas = {}

    @property
    def top_sala(self):
        if len(self.aciertos_salas) != 0:
            x = max(self.aciertos_salas.items(), key=lambda x: x[1])[0]
            if x != 0:
                return x
        return 'Ninguna'

    @property
    def worst_sala(self):
        if len(self.aciertos_salas) != 0:
            x = min(self.aciertos_salas.items(), key=lambda x: x[1])[0]
            if x != self.top_sala:
                return x
        return 'Ninguna'
