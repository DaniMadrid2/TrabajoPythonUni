import random
import threading
import pickle
from informe import Informe

class Partida:
    def __init__(self,cliente,cliente_dos):
        self.clientes= (cliente,cliente_dos)
        self.cliente_activo = 0
    

    def jugar(self):
        try:
            self.clientes[0].sock.sendall(f"La partida va a comenzar. Te vas a enfrentar a {self.clientes[1].nombre}".encode())
            self.clientes[1].sock.sendall(f"La partida va a comenzar. Te vas a enfrentar a {self.clientes[0].nombre}".encode())
            print('Comenzamos la partida, se han enviado textos')
            self.cliente_activo = random.randint(0,1)
            
            self.clientes[self.cliente_activo].sock.sendall('Es tu turno'.encode())
            self.clientes[int(not self.cliente_activo)].sock.sendall('No tu turno'.encode())
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
            while not fin:
                try:
                    datos = self.clientes[self.cliente_activo].sock.recv(1024)
                    self.clientes[int(not self.cliente_activo)].sock.sendall(datos)
                    
                    datos = self.clientes[int(not self.cliente_activo)].sock.recv(1024)
                    if(not datos): datos=pickle.dumps({"terminado":False})
                    resultado:Informe = pickle.loads(datos)
                    self.clientes[self.cliente_activo].sock.sendall(datos)
                    if(datos):
                        if resultado:
                            fin = resultado.terminado
                    if not fin:
                        self.pasar_turno()
                except KeyboardInterrupt:
                    self.clientes[0].close()
                    self.clientes[1].close()
                    print("se cerró la partida (no el sevidor)")
                    return
                

            for c in self.clientes:
                c.sock.sendall(f'Se acabo la partida. El ganador es {self.clientes[self.cliente_activo].nombre}')
                c.sock.close()
        except KeyboardInterrupt:
            return
    def pasar_turno(self):
        self.cliente_activo=int(not self.cliente_activo)

        

        