from personaje import Personaje, Medico, Inteligencia, Artillero, Francotirador  # Importa las otras clases de personajes también
from utils import validar_celda, comprobar_celda_ocupada, validar_celda_contigua
from informe import Informe
class Jugador:
    def __init__(self, default=False):
        self.oponente = None
        self.listapersonajes = [Medico,Artillero,Francotirador,Inteligencia]
        self.equipo = self.crear_equipo(default)
        self.informe = ""

    def mostrar_informe(self):
        print ("---INFORME---")
        self.recibir_accion
    
    def mostrar_estado_equipo(self):
        print("---SITUACION DEL EQUIPO---")
        for personaje in self.equipo:
            print(f"{personaje.nombre} esta en {personaje.posicion} [VIDA {personaje.vida_actual}/{personaje.vida_maxima}]")
    
    def mostrar_acciones(self):
            print("1: Mover (Medico): ")    
            print("2: Mover (Artillero): ")
            print("3: Disparar en área (2x2). Daño 1. (Artillero): ")
            print("4: Mover (Francotirador): ")
            print("5: Disparar a una celda. Daño 3. (Francotirador): ")
            print("6: Mover (Inteligencia): ")
            print("7: Revelar a los enemigos en un área 2x2. (Inteligencia): ")
    
                
    def coger_personaje(self,clase,equipo):
        for p in equipo:
            if(p.nombre == clase().nombre):
                return p
        return None

    def mover_tropa(self,clase,texposicion):
        posicion = self.pedir_posicion(texposicion)
        tropa=self.coger_personaje(clase,self.equipo)
        if(not comprobar_celda_ocupada(posicion,self.equipo)) and validar_celda_contigua(tropa.posicion, posicion):
            tropa.mover(posicion)
        else:
            print('Movimiento no valido')
            self.mover_tropa(clase,texposicion)
    
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
        return accion>=0 and accion<=8
    
    
    def elegir_accion(self, accion=0):#TODO
        accion=int(input("Selecciona la acción de este turno:"))
        if(not self.validar_accion(accion)):
            accion=self.elegir_accion(accion)
        return accion
    def realizar_accion(self, accion):
        if(accion==1):
            self.mover_tropa(Medico,("Indica la posicion a la que mover el Medico:"))
        elif(accion==2):
            self.mover_tropa(Artillero,("Indica la posicion a la que mover el Artillero:")) 
        elif(accion==3):
            return self.coger_personaje(Artillero,self.equipo).habilidad(self.oponente,self.pedir_posicion("Indica una casilla a la que disparar con el Artillero en un area 2x2 (Celda superior izquierda)"))#TODO cambiar texto al necesario
        elif(accion==4):
            self.mover_tropa(Francotirador,("Indica la posicion a la que mover el Francotirador:"))
        elif(accion==5):
            return self.coger_personaje(Francotirador,self.equipo).habilidad(self.oponente,self.pedir_posicion("Indica una casilla a la que disparar con el Francotirador en un area 1x1:"))
        elif(accion==6):
            self.mover_tropa(Inteligencia,self.pedir_posicion("Indica la posicion a la que mover a la Inteligencia:"))
        elif(accion==7):
            return self.coger_personaje(Inteligencia,self.equipo).habilidad(self.pedir_posicion("Indica una posicion a la que revelar usando a la Inteligencia:"),self.oponente.equipo)
    
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
    
    def coger_personaje_en_celda(self,celda,equipo):
        for personaje in equipo:
            if(personaje.posicion == celda):
                return personaje
        return None
            
    def fin_partida():
        pass

    def recibir_accion(self, accion):
        if accion == None:
            return
        celda = accion[2]+accion[3]
        informacion = Informe()

        if accion[1] == "F":
            personaje_herido = self.coger_personaje_en_celda(celda,self.equipo)
            informacion.poner_info(f"{personaje_herido.nombre} ha sido herido en {celda} [Vida restante:{personaje_herido.vida_actual}]")

        else:
            for personaje in self.equipo:
                if personaje.esta_en_area(celda):
                    personaje_herido = self.coger_personaje_en_celda(celda,self.equipo)
                    informacion.poner_info(f"{personaje_herido.nombre} ha sido herido en {celda} [Vida restante:{personaje_herido.vida_actual}]") 

        self.fin_partida(informacion) 
        return informacion
    
    def imprimir_informe_accion(self):
        print("---RESULTADO DE LA ACCION---")

    def set_oponente (self,jugador):
        self.oponente = jugador

    def turno(self):
        self.mostrar_estado_equipo()
        self.mostrar_acciones()
        accion = self.elegir_accion()
        resultado = self.realizar_accion(accion)
        resultado = self.recibir_accion(accion)
        print("----RESULTADO DE LA ACCION ----")
        return resultado.terminado #false si no se ha terminado el juego, true si se ha terminado el juego
