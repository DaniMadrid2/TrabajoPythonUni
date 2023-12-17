class Nodo:
    def __init__ (self,valor):
        self.valor = valor
        self.siguiente =  None
class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
    
    def encolar(self,valor):
        nuevo_nodo = Nodo(valor)
        if self.ultimo:
            self.ultimo.siguiente = nuevo_nodo
        self.ultimo = nuevo_nodo

        if not self.primero:
            self.primero = nuevo_nodo

    def desencolar(self):
        if self.vacia():
            return None
        valor = self.primero.valor
        self.primero = self.primero.siguiente
        if not self.primero:
            self.ultimo = None
        return valor

    def buscar(Self,valor):
        actual = self.primero
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.siguiente
        return Flase

    def vacia(self):
        return self.primero is None

if __name__ == "__main__":
    cola = Cola()
    cola.encolar(2)
    cola.encolar(5)

    print(cola.desencolar())