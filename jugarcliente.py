from utils import limpiar_terminal
from jugador import Jugador
import socket
import pickle
from informe import Informe

def main():
    try:
        port=12345
        host = socket.gethostname()
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(70.0) #Añadimos un timeout de minuto y 10 segundos
        
        try:
            cliente.connect((host,port))
        except socket.timeout:
            cliente.close()
            print("no se pudo conectar con el servidor, tiempo de espera excedido")
            exit()

        nombre=""
        while(not nombre):
            try:
                nombre = input('Introduce tu nombre\n')
            except KeyboardInterrupt:
                print("Se paró la ejecución")
                exit()
            

        cliente.sendall(nombre.encode())
        
        mensaje = cliente.recv(1024).decode()
        if mensaje.startswith('Esperando'):
            print('Estás en el lobby esperando a que otro cliente se una a la partida')
            mensaje = cliente.recv(1024).decode()

        nombre2 = mensaje.split("La partida va a comenzar. Te vas a enfrentar a ")[1]
        mensaje = cliente.recv(1024).decode()

        turno_1 = mensaje.startswith('Es tu turno')
                                    
        empezar(nombre,turno_1,nombre2,cliente)
    except KeyboardInterrupt:
        print("Has parado la ejecución")
        cliente.close()
    # except:
    #     print("No se ha podido conectar con el servidor")



    

  
    
def empezar(nombre,es_turno,nombre2,cliente: socket.socket):
    print('Bienvenidos a Tactical Battle. A jugar!\n')
    input('Turno del Jugador 1. Pulsa intro para comenzar')
    j1 = Jugador(cliente)

    cliente.sendall('Preparado'.encode())

    empezamos=False
    while(not empezamos):
        try:
            datos=cliente.recv(1024)
            if(not datos): continue
            datos=datos.decode()
            empezamos=datos.startswith("Empezamos")
        except KeyboardInterrupt:
            print("Se ha cerrado el cliente mientras empezaba")
            cliente.close()
            exit()

    limpiar_terminal()
            
            
            
    final = False
    tiempo_de_espera_excedido=False
    while not final:
        try:
            if(es_turno):
                input('Es tu turno, pulsa intro para comenzar')
                resultado = j1.turno()
                if(not resultado): resultado="M"
                cliente.sendall(resultado.encode())
                    
                #Recibir informe con pickle
                try:
                    informe = cliente.recv(1024)
                    informe=pickle.loads(informe)
                    if(informe and isinstance(informe,Informe)):
                        j1.recibir_turno(informe)
                        print("Ha terminado tu turno ")
                        final=informe.terminado
                        if(final):
                            print(f'Se acabo la partida. El ganador es {nombre}')
                except socket.timeout:
                    tiempo_de_espera_excedido=True
                    print("Tiempo de espera excedido, cierre automático de la partida")
                    exit()
            
            else:
                print(f'Es el turno del oponente ({nombre2}), esperandoo...')
                accion=""
                while(not (accion!="")):
                    try:
                        accion=cliente.recv(1024)
                        if(accion):
                            accion=accion.decode()
                    except KeyboardInterrupt:
                        print('se cerró la ejecución')
                        cliente.close()
                        exit()
                    except socket.timeout:
                        print("Tiempo de espera excedido, cierre automático de la partida")
                        tiempo_de_espera_excedido=True
                        exit()
                        
                if( not tiempo_de_espera_excedido):
                    informe=j1.recibir_accion(accion)
                    if(informe and isinstance(informe, Informe)):
                        j1.informe=informe
                    #Enviar informe con pickle
                    cliente.sendall(pickle.dumps(informe))
                    final=informe.terminado
                    if(final):
                        print(f'Se acabo la partida. El ganador es {nombre2}')
                
            es_turno=not es_turno
        except KeyboardInterrupt:
            break
        except socket.timeout:
            print("Tiempo de espera excedido, cierre automático de la partida")
            es_turno=not es_turno
            exit()
            # continue
        
    print("se cerró el cliente")
    cliente.close()

if __name__ == '__main__':
    main()
