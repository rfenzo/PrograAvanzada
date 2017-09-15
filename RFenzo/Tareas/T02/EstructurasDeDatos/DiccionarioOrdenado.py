from EstructurasDeDatos.MiLista import MiLista


class DiccionarioOrdenado():

    def __init__(self):
        self.keys = MiLista()

    @property
    def values(self):
        x = MiLista()
        for key, value in self:
            x.append(value)
        return x

    def append(self, key, valor):  # genera una lista si la key ya existe
        if hasattr(self, str(key)):
            if type(getattr(self, str(key))) != MiLista:
                setattr(self, str(key), MiLista(getattr(self, str(key))))
            getattr(self, str(key)) + valor

        else:
            self.__setitem__(str(key), valor)

    def get_by_position(self, position):
        return self[self.keys[position]]

    def get_key(self, valor):
        for key, valors in self:
            if valors == valor:
                return key
        return None

    def pop(self, posicion=0):
        dict = DiccionarioOrdenado()
        i = 0
        for key, value in self:
            if i != posicion:
                dict.append(key, value)
            else:
                llave, valor = key, value
            i += 1
        self.change_dictionary(dict)
        return llave, valor

    def sort_values(self):
        x = DiccionarioOrdenado()
        valores = self.values.sort()
        for j in valores:
            key = self.get_key(j)
            x[key] = j
        self.change_dictionary(x)
        return self

    def change_dictionary(self, dictionary):
        for key, valor in self:
            delattr(self, key)
        self.keys = MiLista()

        for key, value in dictionary:
            self.append(key, value)

    def __iter__(self):
        for key in self.keys:
            yield key, getattr(self, key)

    def __len__(self):
        return len(self.keys)

    def __setitem__(self, key, valor):  # si ya existe la key, entonces le modifica el valor
        if not hasattr(self, str(key)):
            self.keys.append(str(key))
        setattr(self, str(key), valor)

    def __getitem__(self, key):
        for keys in self.keys:
            if str(key) == keys:
                return getattr(self, str(key))
        return None

    def __repr__(self):
        x = "{"
        y = "}"
        for key, valor in self:
            x += "'{}'".format(str(key)) + ": "+str(valor) + ", "
        if len(x) != 1:
            x = x[:-2]
        return x+y
