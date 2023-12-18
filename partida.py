import random
import threading
import pickle
from informe import Informe
import socket
import datetime


NUM_PERSONAJES_INICIO=4
class JugadorPartida:
    def __init__(self,sock,nombre,n_vivos=NUM_PERSONAJES_INICIO):
        self.n_personajes_vivos=n_vivos
        self.nombre=nombre
        self.sock:socket.socket=sock
        
    #callback que espera a recibir Preparado cuando un cliente termina de elegir su equipo

    def ready(self):
        fin = False

        while not fin:
            try:
                datos = self.sock.recv(1024).decode()
                fin = datos.startswith('Preparado')
            except KeyboardInterrupt:
                break
            except ConnectionResetError:
                if(callable(self.quitar_punto_fin_partida)):
                    self.quitar_punto_fin_partida()
                exit()
class Partida:
    def __init__(self,cliente,cliente_dos,servidor):
        self.clientes= (JugadorPartida(cliente.sock,cliente.nombre,NUM_PERSONAJES_INICIO)
                        ,JugadorPartida(cliente_dos.sock,cliente_dos.nombre,NUM_PERSONAJES_INICIO))
        self.cliente_activo = 0
        self.num_turnos = 0
        self.servidor = servidor
        

    def jugar(self, fin_partida, quitar_punto_fin_partida):
        self.quitar_punto_fin_partida=quitar_punto_fin_partida
        try:
            self.clientes[0].sock.sendall(f"La partida va a comenzar. Te vas a enfrentar a {self.clientes[1].nombre}".encode())
            self.clientes[1].sock.sendall(f"La partida va a comenzar. Te vas a enfrentar a {self.clientes[0].nombre}".encode())
            print('COMENZAMOS LA PARTIDA')
            self.cliente_activo = random.randint(0,1)
            
            self.clientes[self.cliente_activo].sock.sendall('Es tu turno'.encode())
            self.clientes[int(not self.cliente_activo)].sock.sendall('No es tu turno'.encode())
            prep1 = threading.Thread(target=self.clientes[0].ready, args=())
            prep2 = threading.Thread(target=self.clientes[1].ready, args=())
            prep1.start()
            prep2.start()
            print('Esperamos a que los clientes envien sus equipos')
            prep1.join()
            prep2.join()
            fin = False
            print('Empezamos')
            self.clientes[self.cliente_activo].sock.sendall('Empezamos'.encode())
            self.clientes[int(not self.cliente_activo)].sock.sendall('Empezamos'.encode())
            
            self.num_turnos = 0
            while not fin:
                try:
                    datos = self.clientes[self.cliente_activo].sock.recv(1024)
                    self.clientes[int(not self.cliente_activo)].sock.sendall(datos)
                    
                    datos = self.clientes[int(not self.cliente_activo)].sock.recv(1024)
                    if(not datos): datos=pickle.dumps(Informe(-1)) #Crea un informe vacío
                    resultado:Informe = pickle.loads(datos)
                    self.clientes[self.cliente_activo].sock.sendall(datos)
                    if(datos):
                        if resultado and type(resultado) == Informe:
                            fin = resultado.terminado
                            n_muertos=self.contar_muertos_en_informe(resultado)
                            self.clientes[int(not self.cliente_activo)].n_personajes_vivos-=n_muertos
    
                    if not fin:
                        self.pasar_turno()
                        self.num_turnos += 1 
                except KeyboardInterrupt:
                    self.clientes[0].close()
                    self.clientes[1].close()
                    print("Se cerró la partida (no el sevidor)")
                    return

            #El ganador es el activo 
            fin_partida(
                self.clientes[self.cliente_activo],
                self.clientes[int(not self.cliente_activo)]
            )
            
            for c in self.clientes:
                c.sock.close()
            
        except (ConnectionError, TimeoutError, ConnectionResetError):
            print("Se ha terminado la conexión de un cliente, o la partida inesperadamente, no hay puntos")
            if(callable(self.quitar_punto_fin_partida)):
                self.quitar_punto_fin_partida()
            exit()
        except KeyboardInterrupt:
            print("Se ha terminado la conexión de un cliente, o la partida inesperadamente, no hay puntos")
            return
        if(callable(self.quitar_punto_fin_partida)):
                self.quitar_punto_fin_partida()
        
    def contar_muertos_en_informe(self,informe:Informe):
        num=0
        for info in informe.informacion:
            if(type(info) == str):
                if(info.find("ha sido eliminado")!=-1):
                    num+=1
        return num
    
    def calcular_puntuacion(self,jugador_ganador:JugadorPartida, jugador_perdedor:JugadorPartida):
        puntos_ganador = 1000 # Puntos base por ganar
        puntos_perdedor = 0
        
        #Puntos por turnos
        puntos_ganador += max(0,(20-self.num_turnos))*20
        if self.num_turnos>10:
            puntos_perdedor += (self.num_turnos-10)*20
            
        #Puntos por estado de los equipos      
        
        #nº enemigos eliminados= 4 - oponente.n_personajes_vivos
        jugador_ganador_enemigos_eliminados=NUM_PERSONAJES_INICIO-jugador_perdedor.n_personajes_vivos
        jugador_perdedor_enemigos_eliminados=NUM_PERSONAJES_INICIO-jugador_ganador.n_personajes_vivos
        
        puntos_ganador += 100*jugador_ganador.n_personajes_vivos
        puntos_ganador += 100* jugador_ganador_enemigos_eliminados
        
        puntos_perdedor += 100 * jugador_perdedor.n_personajes_vivos
        puntos_perdedor += 100 * jugador_perdedor_enemigos_eliminados
        
        if puntos_perdedor > puntos_ganador:
            puntos_ganador = 1000
            puntos_perdedor = 900

        return puntos_ganador, puntos_perdedor
    
    def finalizar_partida(self,jugador_ganador:JugadorPartida,jugador_perdedor:JugadorPartida):
    # Supongamos que determinas quién es el ganador y quién el perdedor
        puntos_ganador, puntos_perdedor = self.calcular_puntuacion(jugador_ganador, jugador_perdedor)

    # Actualizar ranking
        fecha=datetime.date.today()
        self.servidor.ranking.insertar_ordenado(jugador_ganador.nombre, puntos_ganador,jugador_perdedor.nombre,fecha.strftime('%Y-%m-%d-%H-%M'))
        self.servidor.ranking.insertar_ordenado(jugador_perdedor.nombre, puntos_perdedor,jugador_ganador.nombre,fecha.strftime('%Y-%m-%d-%H-%M'))
        print(f"Ganador:{jugador_ganador.nombre} con {puntos_ganador} puntos\nPerdedor:{jugador_perdedor.nombre} con {puntos_perdedor} puntos")      

    # Guardar ranking en archivo
        self.servidor.guardar_ranking('archivo_ranking.txt')
    #Enviar puntuaciones
        jugador_ganador.sock.sendall((str(puntos_ganador)).encode())
        jugador_perdedor.sock.sendall((str(texto_ranking)).encode())
        
    # Enviar Ranking
        texto_ranking = self.servidor.ranking.to_string()
        
        self.clientes[0].sock.sendall(texto_ranking.encode())
        self.clientes[1].sock.sendall(texto_ranking.encode())

    def pasar_turno(self):
        self.cliente_activo=int(not self.cliente_activo)

        

        