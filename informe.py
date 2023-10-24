
class Informe:
    def __init__(self,accion=1,informacion=[]):
        self.accion=accion
        self.informacion=informacion
        self.terminado=False
        pass
    
    def poner_info(self,info):
        self.informacion.append(info)
    
    def terminar(self):
        self.terminado=True
    
    def escribir_informe(self):
        for info in self.informacion:
            print(info)
