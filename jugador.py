from personaje import Personaje, Medico, Inteligencia, Artillero, Francotirador  # Importa las otras clases de personajes también
from utils import validar_celda, comprobar_celda_ocupada
from informe import Informe
class Jugador:
    def __init__(self, default=False):
        self.oponente = None
        self.listapersonajes = [Medico,Artillero,Francotirador,Inteligencia]
        self.equipo = self.crear_equipo(default)
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
    
                
    def coger_personaje(self,clase,equipo):
        for p in equipo:
            if(p.nombre == clase().nombre):
                return p
        return None
    
    def mover_tropa(self,clase,posicion,informe=Informe()):
        tropa=self.coger_personaje(clase,self.equipo)
        if(not comprobar_celda_ocupada(posicion,self.equipo)):
            tropa.mover(posicion)
            informe.poner_info(f"{tropa.nombre} se ha movido a {tropa.posicion}.")
        else:
            print('Movimiento no valido')
        return informe;
            
    def disparar_en_area(self,ataque=1,esquina_superior_izquierda="A1",informe=Informe()):
        for p in self.oponente.equipo:
            if(p.esta_en_area(esquina_superior_izquierda)):
                p.herir(ataque)
                informe.poner_info(f"{p.nombre} ha sido herido en la casilla {p.posicion}")
        return informe
        
    def disparar_franco(self,ataque=3, celda="A1",informe=Informe()):
        hasidoatacado=False
        for p in self.oponente.equipo:
            if(p.posicion == celda):
                p.herir(ataque)
                hasidoatacado=True
                informe.poner_info(f"{p.nombre} del oponente ha sido herido por franco en la casilla {p.posicion}")
        if(hasidoatacado):
            informe.poner(f"franco ha disparado en la celda {celda} y no ha hecho daño")
        return informe
    def pedir_posicion(self, texto="Selecciona una casilla"): #TODO
        pos= input(texto)
        if(not validar_celda(pos)):
            pos=self.pedir_posicion()
        return pos
    
    def revelar_enemigos(self, esquina_superior_izquierda="A1"):
        enemigos_revelados= []
        for p in self.oponente.equipo:
            if(p.esta_en_area(esquina_superior_izquierda)):
                enemigos_revelados.append(p)
        return enemigos_revelados
    
    def validar_accion(self, accion=-1):
        return accion>=0 and accion<=7
    
    
    def elegir_accion(self, accion=0):#TODO
        accion=int(input("Selecciona la acción de este turno:"))
        if(not self.validar_accion(accion)):
            accion=self.elegir_accion(accion)
        return accion
    def realizar_accion(self, accion):
        if(accion==1):
            return self.mover_tropa(Medico,self.pedir_posicion("Indica la posicion a la que mover el medico"))
        elif(accion==2):
            return self.mover_tropa(Artillero,self.pedir_posicion("Indica la posicion a la que mover el artillero"))
            
        elif(accion==3):
            return self.disparar_en_area(self.pedir_posicion("Indica una casilla a la que disparar en un area 2x2 (celda superior izquierda)"))#TODO cambiar texto al necesario
        elif(accion==4):
            return self.mover_tropa(Francotirador,self.pedir_posicion("Indica la posicion a la que mover el francotirador"))
        elif(accion==5):
            return self.disparar_franco(self.coger_personaje(Francotirador,self.equipo).danyo, self.pedir_posicion("Indica una casilla a la que disparar con el franco"))
        elif(accion==6):
            return self.mover_tropa(Inteligencia,self.pedir_posicion("Indica la posicion a la que mover a la inteligencia"))
        elif(accion==7):
            return self.revelar_enemigos(self.pedir_posicion("Indica una posicion a la que revelar usan doa a la inteligencia"))
    def crear_equipo(self, default=False):
        self.equipo=[]
        self.posicionar_equipo(default)
        return self.equipo

    def posicionar_equipo(self,default=False):
        # Implementa la lógica de posicionamiento inicial aquí
        personajes_a_posicionar = 4
        
        for i in range(personajes_a_posicionar):
            posicion_valida = False
            while not posicion_valida:
                if(not default):
                    posicion = input(f"Indica la celda (A-D,1-4) en la que posicionar al {self.listapersonajes[i]().nombre}:")
                else:
                    posicion=str(chr(ord("A")+i))+str(i+1)
                    print(posicion)

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
        resultado.escribir_informe()
        return resultado.terminado #false si no se ha terminado el juego, true si se ha terminado el juego
