from utils import comprobar_celda_disponible,validar_celda
from direccion import Direccion

class Personaje:
    def __init__(self,nombre, vida_maxima, danyo, posicion):
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima
        self.danyo = danyo
        self.posicion = posicion #Ej: "c2"
        self.enfriamiento_restante = 0
        self.nombre= nombre
        self.equipo = []

    def mover(self, dir):
        # Implementa la lógica de movimiento aquí
        dir=Direccion.textoADireccion(dir)
        pos2=self.posicion
        if(dir.dx!=0):
            pos2[0]=chr(int(pos2[0])+dir.dx)
        if(dir.dy!=0):
            pos2[1]=chr(int(pos2[1])+dir.dy)
        
        if(validar_celda(pos2),comprobar_celda_disponible(pos2)):
            self.pos=pos2
            
        pass

    def habilidad(self):
        # Implementa la habilidad especial de cada personaje aquí
        pass

class Medico(Personaje):
    nombre="Médico"
    def habilidad(self):
        # Implementa la habilidad especial del médico aquí
        pass

class Inteligencia(Personaje):
    nombre="Inteligencia"
    def habilidad(self):
        # Investigar las posiciones en un area 2x2 del equipo contrario
        # Pasarlas por consola
        pass
class Artillero(Personaje):
    nombre="Artillero"
    def habilidad(self):
        #
        pass

class Francotirador(Personaje):
    nombre="Francotirador"

    
    def habilidad(self):
        
        pass
