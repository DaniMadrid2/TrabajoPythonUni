import socket 
import threading
from partida import Partida
from ranking import ListaDoblementeEnlazada
class Cliente:
    def __init__(self,sock,nombre):
        self.nombre = nombre
        self.sock:socket.socket = sock

    def ready(self):
        fin = False

        while not fin:
            try:
                datos = self.sock.recv(1024).decode()
                fin = datos.startswith('Preparado')
            except KeyboardInterrupt:
                break
    def close(self):
        self.sock.close()


class Servidor:

    def __init__(self,host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.lobby =[]
        self.lock = threading.Lock()
        self.partidas_activas = 0
        self.max_partidas = max_partidas
        self.ranking = ListaDoblementeEnlazada()
        self.cargar_ranking(archivo_ranking)

    def cargar_ranking(self, archivo):
        try:
            with open(archivo, "-r") as file:
                for linea in file:
                    nombre,puntuacion = linea.strip().split(":")
                    self.ranking.insertar_ordenado(nombre,int(puntuacion))
        except FileNotFoundError:
            print("Archivo de ranking no encontrado. Se iniciara un nuevo ranking.")

    def guardar_ranking(self,archivo):
        with open(archivo,'w') as file:
            file.write(self.ranking.to_string())
    def cliente_administrar(self,sock_cliente):
        datos = sock_cliente.recv(1024)
        if not datos:
            return 
        nombre = datos.decode()
        cliente = Cliente(sock_cliente,nombre)
        self.lock.acquire()
        try: 
            self.lobby.encolar(cliente)
            while not self.lobby.esta_vacia() and self.partidas_activas < self.max_partidas:
                cliente_uno = self.lobby.desencolar()
                cliente_dos = self.lobby.desencolar()
                if cliente_uno and cliente_dos:
                    partida = Partida(cliente_uno, cliente_dos)
                    hilo_partida = threading.Thread (target = self.iniciar_partida, args = (partida,))
                    hilo_partida.start()
        finally: 
            self.lock.release()
        return
    
    def iniciar_partida(self,partida):
        self.partidas_activas += 1
        partida.jugar()

    def start(self):
        self.server.listen()
        print("servidor a la escucha")
        while True:
            try:
                cliente, direccion = self.server.accept()
                print("se ha conectado un cliente ",direccion)
                if cliente:
                    hilo = threading.Thread(target = self.cliente_administrar, args=(cliente,))
                    hilo.start()
            except KeyboardInterrupt:
                print("Se ha cerrado el servidor")
                self.server.close()
                exit()
            # except:
            #     print("Ha habido un fallo en la conexión, cerrando")

# host = "127.0.0.1"
host=socket.gethostname()
port = 12345
max_partidas = 2
archivo_ranking = "ranking.txt"
servidor = Servidor(host,port,max_partidas)
servidor.start()


