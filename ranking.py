import datetime
class NodoRanking:
    def __init__(self, nombre, puntuacion, oponente, fecha = None):
        self.nombre = nombre
        self.puntuacion = puntuacion
        self.anterior = None
        self.siguiente = None
        self.oponente = oponente
        self.fecha = fecha if fecha else datetime.datetime.now()

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar_ordenado(self, nombre, puntuacion,oponente):
        nuevo_nodo = NodoRanking(nombre, puntuacion)
        if not self.cabeza or nuevo_nodo.puntuacion >= self.cabeza.puntuacion:
            nuevo_nodo.siguiente = self.cabeza
            if self.cabeza:
                self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
            if not self.cola:
                self.cola = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente and actual.siguiente.puntuacion > puntuacion:
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            nuevo_nodo.anterior = actual
            actual.siguiente = nuevo_nodo
            if nuevo_nodo.siguiente:
                nuevo_nodo.siguiente.anterior = nuevo_nodo

    def to_string(self):
        ranking = ""
        actual = self.cabeza
        while actual:
            ranking += f"{actual.nombre}: {actual.puntuacion}, Oponente: {actual.oponente}, Fecha: {actual.fecha.strftime('%Y-%m-%d %H:%M:%S')}\n"
            actual = actual.siguiente
        return ranking
