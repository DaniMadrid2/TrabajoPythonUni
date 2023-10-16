from personaje import Personaje, Medico  # Importa las otras clases de personajes también
from utils import comprobar_celda_disponible
class Jugador:
    def __init__(self):
        self.oponente = None
        self.equipo = self.crear_equipo()
        self.informe = ""


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
        for personaje in self.equipo:
            posicion_validaa = False
            while not posicion_valida:
                posicion = input (f'Ingrese la posicion para {personaje.nombre}(Formato: 'A1','B2', etc):')

                if not validar


    def turno(self):
        # Implementa la lógica del turno aquí
        pass

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
