class MiLista():
    def __init__(self,*args):
        self.contador = 0
        for arg in args:
            self.append(arg)

    def append(self,valor):
        setattr(self,str(self.contador),valor)
        self.contador += 1

    def pop(self,posicion = 0):
        eliminado = self[posicion]
        delattr(self,str(posicion))
        self.contador -= 1
        x = posicion
        while x < self.contador:
            setattr(self,str(x),self[x+1])
            x+=1
        return eliminado

    def remove(self,valor):
        i=0
        p = None
        for j in self:
            if j==valor:
                p = self.pop(i)
                break
            i+=1
        return p

    def insert(self,posicion,valor):
        x = self.contador-1
        self.contador += 1
        while x >= posicion:
            setattr(self, str(x+1), self[x])
            x -= 1
        setattr(self,str(posicion),valor)

    def sort(self):
        for i in range(len(self)):
            for j in range(len(self) - 1 - i):
                a = getattr(self,str(j))
                a1 = getattr(self,str(j+1))
                if a < a1:
                    setattr(self,str(j),a1)
                    setattr(self, str(j+1), a)
        return self

    def __len__(self):
        return self.contador

    def __add__(self, other):
        self.append(other)

    def __iter__(self):
        current = 0
        while current != self.contador:
            yield self[current]
            current +=1

    def __getitem__(self, item):
        if item < 0:
            x= len(self)+item
        else:
            x=item
        return getattr(self,str(x))

    def __setitem__(self, key, value):
        return setattr(self,str(key),value)

    def __repr__(self):
        x= ""
        for j in range(self.contador):
            x+= str(self[j]) + ", "
        return "[" + x[:-2] + "]"