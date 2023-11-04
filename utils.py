def limpiar_terminal():
    print(chr(27) + "[2J")

def validar_celda(celda="a2", max_col= 'D', max_row= 4):
    # Implementa la lógica de validación de celda aquí
    if len(celda) != 2:
        return False
    col,row = celda[0].upper(), celda[1]
    valido = 'A' <= col<= max_col and '1'<= row <= str(max_row)
    return valido

def comprobar_celda_ocupada(celda, equipo):
    #Comprueba si una celda esta ocupada
     
    for p in equipo:
         if(p.posicion == celda ):
           return True

    return False
         
def convertir_a_coordenadas (celda):
    #Convertir la celda en formato letra+numero a coordenadas (x,y).

    fila = ord(celda[0].upper()) - ord('A')
    columna = int(celda[1:]) -1 

    return fila, columna

def validar_celda_contigua(celda1,celda2):
    #Verifica si dos celdas son contiguas
    fila1, columna1 = convertir_a_coordenadas(celda1)
    fila2, columna2 = convertir_a_coordenadas(celda2)
    
    return abs(fila1 - fila2) <= 1 and abs(columna1-columna2) <= 1 and (fila1,columna1) != (fila2,columna2)





