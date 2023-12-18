import socket 
import threading
from partida import Partida
from ranking import ListaDoblementeEnlazada
from cola import Cola
import sys

class Cliente:
    def __init__(self,sock,nombre):
        self.nombre = nombre
        self.sock:socket.socket = sock

    def close(self):
        self.sock.close()
        
    def ready(self):
        fin = False

        while not fin:
            try:
                datos = self.sock.recv(1024).decode()
                fin = datos.startswith('Preparado')
            except KeyboardInterrupt:
                break
            except ConnectionResetError:
                exit()
class Servidor:

    def __init__(self,host, port, max_partidas):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.lobby:Cola =Cola()
        self.lock = threading.Lock()
        self.partidas_activas = 0
        self.max_partidas = max_partidas
        self.ranking = ListaDoblementeEnlazada()
        self.running = True
        self.cargar_ranking(fichero_ranking)
            
    #Entre la lista de Clientes, quita al que tenga el mismo socket que sock_cliente
    def quitar_cliente(self,sock_cliente):
        self.lobby.quitar((lambda cliente : cliente.valor.sock==sock_cliente))
        
    #Recibe el nombre y encola al cliente
    def recibir_y_encolar_cliente(self,sock_cliente):
        datos = sock_cliente.recv(1024)
        if not datos:
            return 
        nombre = datos.decode()
        cliente = Cliente(sock_cliente,nombre)
        self.lobby.encolar(cliente)
        
    def hay_partida_y_dos_jugadores(self):
        return (self.lobby.longitud>=2) and self.partidas_activas < self.max_partidas
        
    def crear_partida(self):
        self.lock.acquire()
        try:
            cliente_uno = self.lobby.desencolar()
            cliente_dos = self.lobby.desencolar()
            if cliente_uno and cliente_dos:
                partida = Partida(cliente_uno, cliente_dos,self)
                hilo_partida = threading.Thread (target = self.iniciar_partida, args = (partida,))
                hilo_partida.start()
                
        except (ConnectionError, TimeoutError):
            print("Se ha eliminado un cliente")
            self.quitar_cliente(cliente_uno)
            self.quitar_cliente(cliente_dos)
            if(hilo_partida.is_alive()):
                self.partidas_activas-=1
                
            exit()
        finally:
            self.lock.release()
    
    def iniciar_partida(self,partida:Partida):
        self.partidas_activas += 1
        partida.jugar(partida.finalizar_partida)
        self.partidas_activas -=1 

    def escuchar_clientes(self):
        cliente=False
        while self.running:
            self.server.settimeout(10)
            try:
                cliente, direccion = self.server.accept()
                print("Se ha conectado un cliente ",direccion)
                self.server.settimeout(None)
                if cliente:
                    self.recibir_y_encolar_cliente(cliente)
                        
            except (ConnectionError, TimeoutError,socket.error):
                a=2 #evitar el error timeout
                
            except KeyboardInterrupt:
                print("Se ha cerrado el servidor")
                self.server.close()
                self.running=False
        print("Se ha parado el bucle escuchar clientes")
        
    def bucle_empezar_partidas(self):
        while self.running:
            try:
                if self.hay_partida_y_dos_jugadores():
                    self.crear_partida()
                
            except KeyboardInterrupt:
                print("Se ha cerrado el servidor")
                self.server.close()
                self.running=False
                exit()
        print("Se ha parado el bucle empezar partidas")
        
    def start(self):
        self.server.listen()
        print("Servidor a la escucha")
        hilo_escuchar_clientes = threading.Thread (target = self.escuchar_clientes, args = ())
        hilo_empezar_partidas = threading.Thread (target = self.bucle_empezar_partidas, args = ())
        try:
            hilo_escuchar_clientes.start()
            hilo_empezar_partidas.start()
            while self.running:
                a=2 #Cualquier línea, para que no se cierre la ejecución
        except KeyboardInterrupt:
            print("Cerrando servidor...")
            self.running = False  # Indicar a los hilos que terminen
            hilo_escuchar_clientes.join()
            hilo_empezar_partidas.join()

    def cargar_ranking(self, archivo):
        archivo = 'archivo_ranking.txt'
        try:
            with open(archivo, "r") as file:
                for linea in file:
                    valores=linea.strip().split(":")
                    nombre=""
                    puntuacion=0
                    oponente=""
                    fecha=""
                    if(valores[0]):
                        nombre=valores[0].replace(" ","")
                    else: continue
                    if(valores[1]):
                        puntuacion=valores[1].replace(" ","")
                    else: continue
                    if(valores[2]):
                        oponente=valores[2].replace(" ","")
                    if(valores[3]):
                        fecha=valores[3].replace(" ","")

                    self.ranking.insertar_ordenado(nombre,int(puntuacion),oponente,fecha)

        except FileNotFoundError:
            print("Archivo de ranking no encontrado. Se iniciara un nuevo ranking.")
            
    def guardar_ranking(self,archivo):
        archivo = 'archivo_ranking.txt'
        with open(archivo,'w') as file:
            file.write(self.ranking.to_string())
            
# host = "127.0.0.1"
host=socket.gethostname()
port = 12345

argumentos = sys.argv[1:]
if(len(argumentos)>=1):
    try:
        port=int(argumentos[0])
        if(port>65535 or port < 0):
            raise Exception("Puerto inválido")
    except:
        print(f'Argumentos nº{1} inválido, no está entre 0-65565')
else:
    print("No has pasado el puerto como argumento. Se asumirá como puerto:",port)

if(len(argumentos)>=2):
    try:
        max_partidas=int(argumentos[1])
    except:
        print(f'Argumentos nº{2} inválido, no está')
else:
    max_partidas = int(input("Indica el máximo de partidas del servidor:")) or 2

if(len(argumentos)>=3 and argumentos[2]):
    port=argumentos[2]
else:
    fichero_ranking = "ranking.txt"
    print("No has pasado el fichero de ranking. Se asumirá por defecto:",fichero_ranking)


servidor = Servidor(host,port,max_partidas)
servidor.start()


