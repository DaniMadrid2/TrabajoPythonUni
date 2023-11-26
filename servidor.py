import socket 
import threading
from partida import Partida

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

    def cliente_administrar(self,sock_cliente):
        datos = sock_cliente.recv(1024)
        if not datos:
            return 
        nombre = datos.decode()
        cliente = Cliente(sock_cliente,nombre)
        self.lock.acquire()
        try: 
            if len(self.lobby) == 0:
                self.lobby.append(cliente)
                print('Enviamos esperando al otro cliente al cliente que espera en el lobby')
                cliente.sock.sendall('Esperando al otro cliente'.encode())
            else:
                cliente_dos = self.lobby[0]
                self.lobby = []
                partida = Partida(cliente,cliente_dos)
                hilo_partida = threading.Thread(target = partida.jugar, args = ())
                hilo_partida.start()
        finally: 
            self.lock.release()
        return
    
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

servidor = Servidor(host,port)
servidor.start()


