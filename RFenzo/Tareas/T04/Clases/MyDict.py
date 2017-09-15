from collections import OrderedDict


class MyDict(OrderedDict):
    '''
    Este es un Diccionario Ordenado que ademas tiene el metodo append que 
    permite ir agregando mas de un valor dentro de una misma key, en el formato
    de una lista.
    '''

    def __init__(self, *args):
        super().__init__(*args)

    def append(self, key, valor):
        '''
        permite agregar mas de un elemento a una key,  haciendole append a una
        lista dentro de self[key]. El diccionario se ve de la siguiente forma:
        x = MyDict()
        x.append('Hola',1)
        print(x) ----------->{'Hola':[1]}
        x.append('Hola','chao')
        print(x) ----------->{'Hola':[1,'chao']}

        param key: key donde se desea guardar | tipo: any
        param valor: el valor que se desea guarda | tipo: any

        return none
        return tipo:nones
        '''
        if key in self:
            self[key].append(valor)
        else:
            self[key] = [valor]
