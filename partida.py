import random
import threading


class Partida:
    def __init__(self,cliente,cliente_dos):
        self.clientes= (cliente,cliente_dos)
        self.cliente_activo = 0
    

    def jugar(self):
        self.clientes[0].sock.sendall(f"La partida va a comenzar. Te vas a enfrentar a {self.cliente[1].nombre}".encode())
        self.clientes[1].sock.sendall(f"La partida va a comenzar. Te vas a enfrentar a {self.cliente[0].nombre}".encode())
        self.cliente_activo = random.randint(0,1)
        self.clientes[self.cliente_activo].sock.sendall('Es tu turno'.encode())
        self.clientes[self.cliente_activo].sock.sendall('No tu turno'.encode())
        prep1 = threading.Thread(target=self.clientes[0].preparado, args=())
        prep2 = threading.Thread(target=self.clientes[1].preparado, args=())
        prep1.start()
        prep2.start()
        prep1.join()
        prep2.join()
        fin = False
        while not fin:
            datos = self.clientes[self.cliente_activo].sock.recv(1024)
            self.clientes[self.cliente_activo].sock.sendall(datos)
            datos = self.clientes[self.cliente_activo].sock.recv(1024)
            resultado = pickle.loads(datos)
            self.clientes[self.cliente_activo].sock.sendall(datos)
            if resultado:
                fin = resultado['Fin']
            if not fin:
                self.cambiar.cliente_activo()

        for c in self.clientes:
            c.sock.sendall(f'Se acabo la partida. El ganador es {self.clientes[self.activo].nombre}')
            c.sock.close()


        

        