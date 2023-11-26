from utils import limpiar_terminal
from jugador import Jugador
import socket
import pickle

def main():
    host = socket.gethostname()
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(host,port)

    nombre = input('Introduce tu nombre')

    cliente.sendall(nombre.encode())
    
    mensaje = cliente.recv(1024).decode()
    if mensaje.startswith('Esperando'):
        mensaje = cliente.recv(1024).decode()
    print (mensaje)
    nombre2 = mensaje.split("La partida va a comenzar. Te vas a enfrentar a ")[1]
    mensaje = cliente.recv(1024).decode()

    turno_1 = mensaje.startswith('Es tu turno')
                                
    empezar(nombre,turno_1,nombre2,cliente)



    

  
    
def empezar(nombre,es_turno,nombre2,cliente):
    print('Bienvenidos a Tactical Battle. A jugar!\n')
    input('Turno del Jugador 1. Pulsa intro para comenzar')
    j1 = Jugador(cliente)

    cliente.sendall('Preparado'.encode())

    input('Jugador 1, pulsa para terminar tu turno')
    limpiar_terminal()
            
    final = False
    while not final:
        if(es_turno):
            input('Es tu turno, pulsa intro para comenzar')
            resultado = j1.turno()
            cliente.sendall(resultado.encode())
            informe=#Recibir informe con pickle
            cliente.recibir_turno(informe)
            
            final=informe.terminado
            if(final):
                print('Ha ganado tu oponente')
        
        else:
            print('Es el turno del oponente, esperandoo...')
            accion=cliente.recv(1024).decode()
            informe=j1.recibir_accion(accion)
            #Enviar informe con pickle
            
            final=informe.terminado
            if(final):
                print('Felicidades, has ganado')
            

if __name__ == '__main__':
    main()
