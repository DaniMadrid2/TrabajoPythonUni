from utils import comprobar_celda_ocupada,validar_celda

class Personaje:
    def __init__(self,nombre, vida_maxima=1, danyo=1, posicion="A1"):
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima
        self.danyo = danyo
        self.posicion = posicion #Ej: "c2"
        self.enfriamiento_restante = 0
        self.nombre= nombre
        self.equipo = []

    def mover(self, dir):
        # Implementa la lógica de movimiento aquí
        
        pos2=self.posicion
        if(dir.dx!=0):
            pos2[0]=chr(int(pos2[0])+dir.dx)
        if(dir.dy!=0):
            pos2[1]=chr(int(pos2[1])+dir.dy)
        
        if(validar_celda(pos2),comprobar_celda_ocupada(pos2)):
            self.pos=pos2
            
        pass

    def habilidad(self):
        # Implementa la habilidad especial de cada personaje aquí
        pass

class Medico(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Medico",1,0,posicion)
    def habilidad(self):
        # Implementa la habilidad especial del médico aquí
        pass

class Inteligencia(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Inteligencia",2,0,posicion)
    def habilidad(self):
        # Investigar las posiciones en un area 2x2 del equipo contrario
        # Pasarlas por consola
        pass

class Artillero(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Artillero",2,1,posicion)
    def habilidad(self):
       
        pass

class Francotirador(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Francotirador",3,3,posicion)
    def habilidad(self):   
        pass