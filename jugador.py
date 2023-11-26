from personaje import Personaje, Medico, Inteligencia, Artillero, Francotirador  # Importa las otras clases de personajes también
from utils import validar_celda, comprobar_celda_ocupada, validar_celda_contigua
from informe import Informe
class Jugador:
    def __init__(self, default=False):
        self.oponente = None
        self.listapersonajes = [Medico,Artillero,Francotirador,Inteligencia]
        self.equipo = self.crear_equipo(default)
        self.informe = Informe()
        self.acciones = [1,2,3,4,5,6,7,8]
    
    
    def mostrar_estado_equipo(self):
        print("---SITUACION DEL EQUIPO---")
        for personaje in self.equipo:
            print(f"{personaje.nombre} esta en {personaje.posicion} [VIDA {personaje.vida_actual}/{personaje.vida_maxima}]")
    

                
    def coger_personaje(self,clase,equipo):
        for p in equipo:
            if(p.nombre == clase().nombre):
                return p
        return None

    def mover_tropa(self,clase,texposicion):
        tropa=self.coger_personaje(clase,self.equipo)
        posicion = self.pedir_posicion(texposicion+f" (Posicion actual: {tropa.posicion})")
        if(comprobar_celda_ocupada(posicion,self.equipo)):
            print('Ups... la celda ya está ocupada!')
            self.mover_tropa(clase,texposicion)
        elif(not validar_celda_contigua(tropa.posicion, posicion)):
            print('Movimiento no valido')
            self.mover_tropa(clase,texposicion)
        else:
            tropa.mover(posicion)
    
    def pedir_posicion(self, texto="Selecciona una casilla"): #TODO
        print(texto)
        pos= input()
        if(len(pos)!=2):
            pos=self.pedir_posicion()
        pos=pos[0].upper()+pos[1]
        if(not validar_celda(pos)):
            pos=self.pedir_posicion()
        return pos
    
    def revelar_enemigos(self, esquina_superior_izquierda="A1"):
        enemigos_revelados= []
        for p in self.oponente.equipo:
            if(p.esta_en_area(esquina_superior_izquierda)):
                enemigos_revelados.append(p)
        return enemigos_revelados
    
    def validar_accion(self, accion, acciones_posibles):
        return accion>=1 and accion<=len(acciones_posibles)
    
    
    def esta_vivo(self, clase):
        for personaje in self.equipo:
            if(type(personaje) is clase):
                return personaje.vida_actual>0
        return False
        
    def mostrar_acciones(self):
        acciones_validas=[]
        tmpi=1
        if(self.esta_vivo(Medico)):
            print(f"{tmpi}: Mover (Medico) ")    
            tmpi+=1
            acciones_validas.append(1)
            if(self.coger_personaje(Medico,self.equipo).valido_habilidad(self.equipo)):
                print(f"{tmpi}: Curar a un compañero (Medico) ")
                tmpi+=1
                acciones_validas.append(8)
        if(self.esta_vivo(Artillero)):
            print(f"{tmpi}: Mover (Artillero) ")
            tmpi+=1
            acciones_validas.append(2)
            if(self.coger_personaje(Artillero,self.equipo).valido_habilidad(self.equipo)):
                print(f"{tmpi}: Disparar en área (2x2). Daño 1. (Artillero) ")
                tmpi+=1
                acciones_validas.append(3)
        
        if(self.esta_vivo(Francotirador)):
            print(f"{tmpi}: Mover (Francotirador) ")#4
            tmpi+=1
            acciones_validas.append(4)
            if(self.coger_personaje(Francotirador,self.equipo).valido_habilidad(self.equipo)):
                print(f"{tmpi}: Disparar a una celda. Daño 3. (Francotirador) ")#5
                tmpi+=1
                acciones_validas.append(5)
        if(self.esta_vivo(Inteligencia)):
            print(f"{tmpi}: Mover (Inteligencia) ")#6
            tmpi+=1
            acciones_validas.append(6)
            if(self.coger_personaje(Inteligencia,self.equipo).valido_habilidad(self.equipo)):
                print(f"{tmpi}: Revelar a los enemigos en un área 2x2. (Inteligencia) ") #7
                tmpi+=1
                acciones_validas.append(7)
        return acciones_validas
    
    def elegir_accion(self, acciones_posibles):#TODO
        try:
            accion=int(input("Selecciona la acción de este turno:"))
            if(not self.validar_accion(accion,acciones_posibles)):
                return self.elegir_accion(acciones_posibles)
            return acciones_posibles[accion-1]
        except KeyboardInterrupt:
            raise Exception("No se ha seleccionado una acción")
        except:
             return self.elegir_accion(acciones_posibles)
    
    def realizar_accion(self, accion):
        if(accion==1):
            self.mover_tropa(Medico,("Indica la celda a la que mover al Medico:"))
        elif(accion==8):
            self.coger_personaje(Medico,self.equipo).habilidad(self.equipo)
        elif(accion==2):
            self.mover_tropa(Artillero,("Indica la celda a la que mover al Artillero:")) 
        elif(accion==3):
            return self.coger_personaje(Artillero,self.equipo).habilidad(self.oponente,self.pedir_posicion("Indica una casilla a la que disparar con el Artillero en un area 2x2 (Celda superior izquierda)"))#TODO cambiar texto al necesario
        elif(accion==4):
            self.mover_tropa(Francotirador,("Indica la celda a la que mover al Francotirador:"))
        elif(accion==5):
            return self.coger_personaje(Francotirador,self.equipo).habilidad(self.oponente,self.pedir_posicion("Indica una casilla a la que disparar con el Francotirador en un area 1x1:"))
        elif(accion==6):
            self.mover_tropa(Inteligencia,"Indica la celda a la que mover a la Inteligencia:")
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
            
    def eliminar_muertos(self):
        vivos=[]
        for personaje in self.equipo:
            if(personaje.vida_actual>0):
                vivos.append(personaje)
        self.equipo=vivos
            
    def fin_partida(self):
        finDelJuego=True
        for personaje in self.equipo:
            if(type(personaje) != Medico) and personaje.vida_actual>0:
                return False
                
        return finDelJuego

    def recibir_accion(self, accion):
        informacion = Informe()
        informacion.borar_informe()
        self.informe=informacion
        if accion == None:
            return informacion
        celda = str(accion[1]).upper()+accion[2]

        if accion[0] == "F":
            personaje_herido = self.coger_personaje_en_celda(celda,self.equipo)
            if(personaje_herido.vida_actual > 0):
                informacion.poner_info(f"{personaje_herido.nombre} ha sido herido en {celda} [Vida restante:{personaje_herido.vida_actual}]")
            else:
                informacion.poner_info(f"{personaje_herido.nombre} ha sido eliminado") 

        else:
            hay_personaje_en_area=False
            for personaje in self.equipo:
                if personaje.esta_en_area(celda):
                    hay_personaje_en_area=True
                    if accion[0] == "A":
                        if(personaje.vida_actual > 0):
                            informacion.poner_info(f"{personaje.nombre} ha sido herido en {celda} [Vida restante:{personaje.vida_actual}]") 
                        else:
                            informacion.poner_info(f"{personaje.nombre} ha sido eliminado") 
                        
                    if accion[0] == "I":
                        informacion.poner_info(f"{personaje.nombre} ha sido avistado en {personaje.posicion}") 
            if(not hay_personaje_en_area):
                if accion[0] == "A":
                    informacion.poner_info("Ningún personaje ha sido herido")
                if accion[0] == "I":
                    informacion.poner_info("Ningún personaje ha sido revelado")
        informacion.terminado=self.fin_partida() 
        self.eliminar_muertos()
        return informacion
    
    def mostrar_resultado_accion(self, informe):
        if(informe.hay_informe()):
            print("---RESULTADO DE LA ACCION---")
            informe.escribir_informe()
    def mostrar_informe(self):
        print("---INFORME---")
        if(self.informe.hay_informe()):
            self.informe.escribir_informe()
        else:
            print("Nada que reportar")

    def pasar_turno_equipo(self):
        for personaje in self.equipo:
            personaje.pasar_turno()

    def set_oponente (self,jugador):
        self.oponente = jugador

    def turno(self):
        self.mostrar_informe()
        self.mostrar_estado_equipo()
        acciones=self.mostrar_acciones()
        accion = self.elegir_accion(acciones)
        return self.realizar_accion(accion)
    
    def recibir_turno(self,informe):
        self.pasar_turno_equipo()
        self.mostrar_resultado_accion(informe)
        return informe #false si no se ha terminado el juego, true si se ha terminado el juego
