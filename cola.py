class Nodo:
    def __init__ (self,valor):
        self.valor = valor
        self.siguiente =  None
class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.longitud = 0
        
    
    
    def encolar(self,valor):
        nuevo_nodo = Nodo(valor)
        if self.ultimo:
            self.ultimo.siguiente = nuevo_nodo
        self.ultimo = nuevo_nodo 
        self.longitud += 1

        if not self.primero:
            self.primero = nuevo_nodo

    def desencolar(self):
        if self.vacia():
            return None
        valor = self.primero.valor
        self.primero = self.primero.siguiente
        self.longitud -= 1
        
        if not self.primero:
            self.ultimo = None
        return valor

    def buscar(self,valor):
        actual = self.primero
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.siguiente
        return False

    def vacia(self):
        return self.primero is None


