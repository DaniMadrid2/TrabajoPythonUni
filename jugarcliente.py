from utils import limpiar_terminal
from jugador import Jugador


def main():
    servidor=conectConServidor()
    nombre2=esperarConexion()
    empezar(nombre2)
    pass
    
def empezar(nombre2):
    print('Bienvenidos a Tactical Battle. A jugar!\n')
    input('Turno del Jugador 1. Pulsa intro para comenzar')
    j1 = Jugador()

    input('Jugador 1, pulsa terminar tu turno')
    limpiar_terminal()
    enviarEquipo()

    j2=esperarEquipoContrincante()
            
    input('Jugador 2, pulsa terminar tu turno')
    limpiar_terminal()

    j1.set_oponente(j2)
    j2.set_oponente(j1)

    final = False
    while not final:
        input('Turno del Jugador 1. Pulsa intro para comenzar')
        final = j1.turno()
        
        if final:
            print("***** El jugador 1 ha ganado la partida! *****")
            return 0

        input('Jugador 1, pulsa intro para terminar tu turno')
        limpiar_terminal()

        print('Esperando turno oponente')
        
        final = EsperarTurnoOponente()
        if final:
            print("***** El jugador 2 ha ganado la partida! *****")
            return 0

        input('Jugador 2, pulsa intro para terminar tu turno')
        limpiar_terminal()


if __name__ == '__main__':
    main()
