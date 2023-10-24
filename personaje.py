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

    def mover(self, pos):
        # Implementa la lógica de movimiento aquí
        if(validar_celda(pos) and not comprobar_celda_ocupada(pos, self.equipo)):
            self.posicion=pos
            
        pass

    def herir(self, danio):
        self.vida_actual

    def habilidad(self):
        # Implementa la habilidad especial de cada personaje aquí
        pass
    

            
    def esta_en_area(self, posicion):
        for dx in range(2):  # Check positions right and current column
            for dy in range(2):  # Check positions up and current row
                col = chr(ord(self.posicion[0]) + dx)
                row = chr(ord(self.posicion[1]) + dy)
                if col + row == posicion:
                    return True
        return False

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