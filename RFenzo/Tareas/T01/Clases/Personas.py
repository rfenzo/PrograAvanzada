from Clases.Recursos import Recurso
from Funciones.custom_csv import csv_to_dict, print_csv, input_to_csv


class Persona():

    def __init__(self, id_recurso, nombre, fecha_actual):
        self.id_recurso = id_recurso
        self.nombre = nombre
        self.fecha_actual = fecha_actual

    @property
    def recurso(self):
        if self.id_recurso == "":
            return None
        else:
            recursos = csv_to_dict("recursos.csv")
            for j in recursos:
                if self.id_recurso == j["id"]:
                    return Recurso(j)

    @property
    def tipo(self):
        if self.id_recurso == "":
            return "Anaf"
        elif self.recurso.tipo == 'AVION' or self.recurso.tipo == 'HELICOPTERO':
            return "Piloto"
        else:
            return "Jefe"

    def ver(self, archivo):
        if self.tipo == "Piloto" or self.tipo == "Jefe":
            if self.recurso.incendio and archivo.nombre_archivo == "incendios.csv":
                print(self.recurso.incendio)

            elif archivo == "recursos.csv":
                print(self.recurso)
            else:
                print("No tienes permiso para acceder a esa información")
        else:
            print_csv(archivo, self.fecha_actual)

        return ""

    def modificar_archivo(self, archivo):
        input_to_csv(archivo)
        return ""
