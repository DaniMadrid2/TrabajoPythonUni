from personaje import Personaje, Medico  # Importa las otras clases de personajes también
from utils import validar_celda, comprobar_celda_disponible
class Jugador:
    def __init__(self):
        self.oponente = None
        self.equipo = self.crear_equipo()
        self.informe = ""
        self.nombre = nombre

    def mostrar_informe(self):
        print ("---INFORME---")
        for personaje in self.equipo:
            print(f"{personaje.nombre} ha sido herido en {personaje.posicion}[Vida{personaje.vida_actual/{personaje.vida_maxima}}]")
    
    def mostrar_estado_equipo(self):
        print("---SITUACION DEL EQUIPO---")
        for personaje in self.equipo:
            print(f"{personaje.nombre} esta en {personaje.posicion} [VIDA {personaje.vida_actual}/{personaje.vida_max}]")
    
    def mostrar_acciones(self):
            print("1: Mover (Medico)")    
            print("2: Mover (Artillero")
            print("3: Disparar en área (2x2). Daño 1. (Artillero")
            print("4: Mover (Francotirador")
            print("5: Disparar a una celda. Daño 3. (Francotirador)")
            print("6: Mover (Inteligencia)")
            print("7: Revelar a los enemigos en un área 2x2. (Inteligencia)")
    
    def elegir_accion(self, accion):
        pass

    # def preguntarPersonaje(clase):
    #     input("Introduce la posición de tu ")

    # def anyadirPersonaje(self,personaje):
    #     self.equipo.append(personaje)
    #     pass

    def crear_equipo(self):
        equipo=[]


        return equipo

    def posicionar_equipo(self):
        # Implementa la lógica de posicionamiento inicial aquí
        personajes_a_posicionar = 4
        
        for i in range(personajes_a_posicionar):
            posicion_valida = False
            while not posicion_valida:
                posicion = input(f"Ingrese la posicion para el personaje {i+1},(Formato: 'A1','B2', etc):")

                if not validar_celda(posicion):
                    print('Celda incorrecta. Porfavor, elija otra celda')
                    continue

                if not comprobar_celda_disponible(posicion,self.equipo):
                    print('Celda ocupado.Porfavor elije otra celda')
                    continue
                personaje = self.crear_personaje (posicion,i+1)
                self.equipo.append(personaje)
                posicion_valida = True

        input('Jugador 1, pulsa INTRO para terminar tu turno')

    def turno(self):
        # Implementa la lógica del turno aquí
        self.mostrar_informe()
        self.mostrar_estado_equipo()
        accion = self.elegir_accion()
        resultado = self.realizar_accion()
        return resultado #Devuelve informacion sobre el estado del juego.

    def realizar_accion(self):
        # Implementa la lógica para realizar una acción aquí
        pass

    def recibir_accion(self, accion):
        # Implementa la lógica para recibir una acción aquí
        pass

    def turno(self):
        self.mostrar_informe()
        self.mostrar_estado_equipo()
        accion = self.elegir_accion()
        resultado = self.realizar_accion(accion)
        return resultado  # Puedes hacer que esto devuelva información sobre el estado del juego, por ejemplo, si el juego ha terminado.
