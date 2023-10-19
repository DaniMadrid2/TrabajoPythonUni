from personaje import Personaje, Medico, Inteligencia, Artillero, Francotirador  # Importa las otras clases de personajes también
from utils import validar_celda, comprobar_celda_ocupada
class Jugador:
    def __init__(self):
        self.oponente = None
        self.listapersonajes = [Medico,Artillero,Francotirador,Inteligencia]
        self.equipo = self.crear_equipo()
        self.informe = ""

    def mostrar_informe(self):
        print ("---INFORME---")
        for personaje in self.equipo:
            print(f"{personaje.nombre} ha sido herido en {personaje.posicion}[Vida{personaje.vida_actual/{personaje.vida_maxima}}]")
    
    def mostrar_estado_equipo(self):
        print("---SITUACION DEL EQUIPO---")
        for personaje in self.equipo:
            print(f"{personaje.nombre} esta en {personaje.posicion} [VIDA {personaje.vida_actual}/{personaje.vida_maxima}]")
    
    def mostrar_acciones(self):
            print("1: Mover (Medico)")    
            print("2: Mover (Artillero")
            print("3: Disparar en área (2x2). Daño 1. (Artillero")
            print("4: Mover (Francotirador")
            print("5: Disparar a una celda. Daño 3. (Francotirador)")
            print("6: Mover (Inteligencia)")
            print("7: Revelar a los enemigos en un área 2x2. (Inteligencia)")
    
    def coger_personaje(self,clase,equipo=self.equipo):
        for p in equipo:
            if(p.name is clase):
                return p
        return None
    
    def mover_tropa(self,clase,posicion):
        tropa=self.coger_personaje(clase)
        if(not comprobar_celda_ocupada(posicion,self.equipo)):
            tropa.posicion=posicion
            
    def ser_disparado_area(self,ataque=1,posicion="A1"):
        for p in self.equipo:
            if(p.esta_en_area(posicion)):
                p.herir(ataque)
        
    
    def elegir_accion(self, accion):
        accion=input("Selecciona la acción de este turno:")
        

    def crear_equipo(self):
        self.equipo=[]
        self.posicionar_equipo()
        return self.equipo

    def posicionar_equipo(self):
        # Implementa la lógica de posicionamiento inicial aquí
        personajes_a_posicionar = 4
        
        for i in range(personajes_a_posicionar):
            posicion_valida = False
            while not posicion_valida:
                posicion = input(f"Indica la celda (A-D,1-4) en la que posicionar al {self.listapersonajes[i]().nombre}:")

                if not validar_celda(posicion):
                    print('Ups... valor de celda incorrecto.')
                    continue

                if comprobar_celda_ocupada(posicion,self.equipo):
                    print('Ups... la celda ya está ocupada!')
                    continue
                personaje = self.crear_personaje (posicion,self.listapersonajes[i])
                self.equipo.append(personaje)
                posicion_valida = True

    def crear_personaje(self,posicion , clase):
        return clase(posicion)

    def realizar_accion(self):
        # Implementa la lógica para realizar una acción aquí
        pass

    def resultado_accion(self, accion):
        pass

    def imprimir_informe_accion(self):
        print("---RESULTADO DE LA ACCION---")

    def set_oponente (self,jugador):
        self.oponente = jugador

    def turno(self):
        self.mostrar_estado_equipo()
        self.mostrar_acciones()
        accion = self.elegir_accion()
        resultado = self.realizar_accion(accion)
        self.imprimir_informe_accion()
        self.mostrar_informe()
        return resultado  # Puedes hacer que esto devuelva información sobre el estado del juego, por ejemplo, si el juego ha terminado.
