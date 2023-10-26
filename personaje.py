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

    def herir(self, danio):
        self.vida_actual

    def habilidad(self):
        # Implementa la habilidad especial de cada personaje aquí
        pass
    
    def coger_personaje_en_celda(self,celda,equipo, excluido= "Medico"):
        for personaje in equipo:
            if(personaje.posicion == celda and personaje != "Medico"):
                return personaje
        return None
            
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
      celda= input('Ingrese la celda en la que se encuentra el personaje que desea curar: ')
      personaje_a_curar = self.coger_personaje_en_celda(celda)
      if personaje_a_curar is None:
        print ('No hay nadie a quien curar')
        return self.habilidad()
      elif personaje_a_curar == Medico:
        print('El medico no se puede curar a si mismo')
        return self.habilidad()
      else:
            personaje_a_curar.vida_actual = personaje_a_curar.vida_maxima
      return "M"+ celda

        

class Inteligencia(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Inteligencia",2,0,posicion)
    def habilidad(self,celda,equipo_contrario):
        for p in equipo_contrario:
            if p.esta_en_area(celda): 
                return "I"+celda      
    
class Artillero(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Artillero",2,1,posicion)
    def habilidad(self,oponente,esquina_superior_izquierda="A1"):
        personaje_dado = False
        for p in oponente.equipo:
            if(p.esta_en_area(esquina_superior_izquierda)):
                p.herir(self.danyo)
                personaje_dado = True

        if personaje_dado:
            return 'A'+esquina_superior_izquierda

class Francotirador(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Francotirador",3,3,posicion)
    def habilidad(self,oponente,celda="AI"):   
        personaje_dado=False
        for p in oponente.equipo:
            if(p.posicion == celda):
                p.herir(self.danyo)
                personaje_dado= True
        if personaje_dado:
            return 'F'+celda
