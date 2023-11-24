import socket 
import threading
import pickle

class Cliente:
    def __init__(self,sock,nombre):
        self.nombre = nombre
        self.sock = sock




# sock = server

class Servidor:

    def __init__(self,conexion):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(host,port)
        self.lobby =[]
        self.lock = threading.lock()

    def cliente_administrar(self,sock_cliente):
        datos = server.recv(1024)
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
                cliente, direccion = self.sock.accept()
                if cliente:
                    hilo = threading.Thread(target = self.cliente_administrar, arg = (cliente))
                    hilo.start()
            except KeyboardInterrupt:
                self.server.close()
                break

host = socket.gethostbyname()
port = 12345

servidor = Server(host,port)
servidor.start()


