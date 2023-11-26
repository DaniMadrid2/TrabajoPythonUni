import socket 
import threading
import pickle

class Cliente:
    def __init__(self,sock,nombre):
        self.nombre = nombre
        self.sock = sock

    def ready(self):
        fin = False

        while not fin:
            datos = self.sock.recv(1024)
            fin = datos == 'Preparado'



# sock = server

class Servidor:

    def __init__(self,host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.lobby =[]
        self.lock = threading.Lock()

    def cliente_administrar(self,sock_cliente):
        datos = self.server.recv(1024)
        if not datos:
            return 
        nombre = datos.decode()
        cliente = Cliente(sock_cliente,nombre)
        self.lock.acquire()
        try: 
            if len(self.lobby) == 0:
                self.lobby.append(cliente)
                cliente.sock.sendall('Esperando al otro cliente'.encode())
            else:
                cliente_dos = self.lobby[0]
                self.lobby = []
                partida = Partida(cliente,cliente_dos)
                hilo_partida = threading.Thread(target = partida.jugar(), args = ())
                hilo_partida.start()
        finally: 
            self.lock.release()
        return
    
    def start(self):
        self.server.listen()
        while True:
            try:
                cliente, direccion = self.server.accept()
                if cliente:
                    hilo = threading.Thread(target = self.cliente_administrar, arg = (cliente))
                    hilo.start()
            except KeyboardInterrupt:
                self.server.close()
                break

host = socket.gethostbyname("")
port = 12345

servidor = Servidor(host,port)
servidor.start()


