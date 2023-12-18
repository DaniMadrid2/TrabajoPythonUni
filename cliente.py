from utils import limpiar_terminal, pedir_string
from jugador import Jugador
import socket
import pickle
from informe import Informe

PREPARADO_STR='Ready'

DEFAULT_TIMEOUT=70.0
DEFAULT_PORT=12345
DEFAULT_HOST = socket.gethostname()

def ConectarCliente(puerto=DEFAULT_PORT, host=DEFAULT_HOST):
    cliente: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.settimeout(DEFAULT_TIMEOUT) #Añadimos un timeout de minuto y 10 segundos
    try:
        cliente.connect((host,puerto))
    except (ConnectionError, TimeoutError) :
        CerrarConexion(cliente)
        print("No se pudo conectar con el servidor, tiempo de espera excedido")
        exit()
    return cliente

def EsperarConexionContrincante(nombre:str, cliente:socket.socket):
    cliente.sendall(nombre.encode()) #Enviamos nombre
    
    cliente.settimeout(None)
    mensaje_recibido = cliente.recv(1024).decode()
    esperando=mensaje_recibido.startswith('Esperando')
    
    if esperando:
        print('Estás en el lobby esperando a que otro cliente se una a la partida')
        mensaje_recibido = cliente.recv(1024).decode()
    cliente.settimeout(DEFAULT_TIMEOUT)
    return mensaje_recibido

def RecibirEsTurno(cliente:socket.socket):
    mensaje_recibido: str = cliente.recv(1024).decode()
    return mensaje_recibido.startswith('Es tu turno')

def CogerNombreContrincante(mensaje:str):
    #Comenzar Partida
    return mensaje.split("La partida va a comenzar. Te vas a enfrentar a ")[1]

def CerrarConexion(cliente:socket.socket):
    cliente.close()

def RecibirEmpezamos(cliente:socket.socket):
    cliente.settimeout(None)
    datos=cliente.recv(1024)
    cliente.settimeout(DEFAULT_TIMEOUT)
    if(not datos): return False
    datos=datos.decode()
    return datos.startswith("Empezamos")
def EsperarComienzoPartida(cliente:socket.socket):
    empezamos=False
    while(not empezamos):
        try:
            empezamos=RecibirEmpezamos(cliente)
        except KeyboardInterrupt:
            print("Se ha cerrado el cliente")
            CerrarConexion(cliente)

def BuclePrincipal(jugador:Jugador,cliente:socket.socket,es_turno:bool, nombre:str, nombre_contrincante:str):
    final = False
    tiempo_de_espera_excedido=False
    
    while not final:
        if(es_turno):
            input('Es tu turno, pulsa intro para comenzar')
            resultado = jugador.turno()
            cliente.sendall(resultado.encode())
            if(not resultado): resultado="M"
                
            #Recibir informe con pickle
            try:
                informe = cliente.recv(1024)
                informe=pickle.loads(informe)
                if(informe and isinstance(informe,Informe)):
                    jugador.recibir_turno(informe)
                    print("Ha terminado tu turno ")
                    final=informe.terminado
                    if(final):
                        print(f'Se acabo la partida. El ganador es {nombre}')
            except TimeoutError :
                tiempo_de_espera_excedido=True
                print("Tiempo de espera excedido, cierre automático de la partida")
                exit()
            except KeyboardInterrupt:
                print('Se cerró la ejecución')
                CerrarConexion(cliente)
                break
        
        else:
            print(f'Es el turno de ({nombre_contrincante}), esperando...')
            accion=""
            while(accion==""):
                try:
                    accion=cliente.recv(1024)
                    if(accion):
                        accion=accion.decode()
                except KeyboardInterrupt:
                    print('Se cerró la ejecución')
                    CerrarConexion(cliente)
                    break
                except TimeoutError :
                    print("Tiempo de espera excedido, cierre automático de la partida")
                    tiempo_de_espera_excedido=True
                    
            if( not tiempo_de_espera_excedido):
                informe=jugador.recibir_accion(accion)
                if(informe and isinstance(informe, Informe)):
                    jugador.informe=informe
                #Enviar informe con pickle
                cliente.sendall(pickle.dumps(informe))
                final=informe.terminado
                if(final):
                    print(f'Se acabo la partida. El ganador es {nombre_contrincante}')
        
        print("")
        es_turno=not es_turno

def main():
    #Conectar con el server
    cliente: socket.socket = ConectarCliente()
    print('Bienvenidos a Tactical Battle. A jugar!\n')
    
    nombre: str = pedir_string("Inserte un nombre:")
    
    #Esperando 
    print("Esperando la conexión con el contrincante")
    mensaje_recibido_contrincante: str = EsperarConexionContrincante(nombre,cliente)
    nombre_contrincante: str = CogerNombreContrincante(mensaje_recibido_contrincante)
    print("Tu contrincante es: "+nombre_contrincante)
    
    #Comenzar Partida
    es_turno:bool = RecibirEsTurno(cliente)

    #Comenzar Turno
    input(f'Posiciona tu equipo antes de empezar. Pulsa intro para comenzar.')
    j1 = Jugador(True)

    cliente.sendall('Preparado'.encode())
    
    print("Has posicionado tu equipo. Esperando a que inicie la partida.")
    try:
        EsperarComienzoPartida(cliente)
    except KeyboardInterrupt:
        print("Se ha cerrado el cliente")
        CerrarConexion(cliente)
    except ConnectionError:
        print("Ha fallado la conexión con el servidor")
        exit()
    limpiar_terminal()
                   
    BuclePrincipal(j1,cliente,es_turno,nombre,nombre_contrincante)
    print('PUNTUACIONES:')
    print(cliente.recv(1024).decode())

    print("Se cerró el cliente")
    CerrarConexion(cliente)
    
    

if __name__ == '__main__':
    main()
