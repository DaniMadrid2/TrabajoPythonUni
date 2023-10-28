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
        self.turnos_enfriamiento=1
        self.ha_usado_la_habilidad=False

    def mover(self, pos):
        # Implementa la lógica de movimiento aquí
        if(validar_celda(pos) and not comprobar_celda_ocupada(pos, self.equipo)):
            self.posicion=pos

    def herir(self, danio):
        self.vida_actual-=danio

    def habilidad(self):
        # Implementa la habilidad especial de cada personaje aquí
        self.ha_usado_la_habilidad=True
        pass
    def pasar_turno(self):
        if(self.enfriamiento_restante==0 and (not self.ha_usado_la_habilidad)): return
        self.ha_usado_la_habilidad=False
        self.enfriamiento_restante+=1
        if(self.enfriamiento_restante>=(self.turnos_enfriamiento+1)):
            self.enfriamiento_restante=0
    
    def valido_habilidad(self,equipo):
        return self.enfriamiento_restante==0
    # def coger_personaje_en_celda(self,celda,equipo, excluido= "Medico"):
    #     for personaje in equipo:
    #         if(personaje.posicion == celda and personaje != "Medico"):
    #             return personaje
    #     return None
            
    def esta_en_area(self, posicion):
        for dx in range(2):  # Check positions right and current column
            for dy in range(2):  # Check positions up and current row
                col = chr(ord(self.posicion[0].upper()) + dx-1)
                row = chr(ord(self.posicion[1]) + dy-1)
                if col + row == posicion:
                    return True
        return False

class Medico(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Medico",1,0,posicion)
        
    def coger_personajes_heridos(self,equipo):
        personajes_heridos=[]
        tmpi=1
        for personaje in equipo:
            if(personaje != self and personaje.vida_actual<personaje.vida_maxima and personaje.vida_actual>0):
                print(f"{tmpi}: {personaje.nombre} [{personaje.vida_actual}/{personaje.vida_maxima}]")
                personajes_heridos.append(personaje)
                tmpi=tmpi+1
        return personajes_heridos
    
    def valido_habilidad(self,equipo):
        if(not super().valido_habilidad(equipo)):
            return False
        return len(self.coger_personajes_heridos(equipo))>0
        
    def habilidad(self,equipo):
        super().habilidad()
        personajes_heridos=self.coger_personajes_heridos(equipo)
        tmpi=-1
        while(tmpi>len(personajes_heridos) and tmpi<1):
            tmpi=input('Selecciona el personaje a curar: ')
        personaje_a_curar = personajes_heridos[tmpi]
        
        personaje_a_curar.vida_actual = personaje_a_curar.vida_maxima
        return "M"+ (personaje_a_curar.posicion)

        

class Inteligencia(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Inteligencia",2,0,posicion)
    def habilidad(self,celda,equipo_contrario):
        super().habilidad()
        for p in equipo_contrario:
            if p.esta_en_area(celda): 
                return "I"+celda      
    
class Artillero(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Artillero",2,1,posicion)
    def habilidad(self,oponente,esquina_superior_izquierda="A1"):
        super().habilidad()
        for p in oponente.equipo:
            if(p.esta_en_area(esquina_superior_izquierda)):
                p.herir(self.danyo)
        
        return 'A'+esquina_superior_izquierda

class Francotirador(Personaje):
    def __init__(self, posicion="A1"):
        super().__init__("Francotirador",3,3,posicion)
    def habilidad(self,oponente,celda="AI"):   
        super().habilidad()
        for p in oponente.equipo:
            if(p.posicion == celda):
                p.herir(self.danyo)
        return 'F'+celda
