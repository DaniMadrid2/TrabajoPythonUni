
class Informe:
    def __init__(self,accion=1,informacion=[]):
        self.accion=accion
        self.informacion=informacion
        self.terminado=False
        self.hay_info=False
    
    def poner_info(self,info):
        self.informacion.append(info)
        self.hay_info=True
    
    def terminar(self):
        self.terminado=True
    
    def escribir_informe(self):
        for info in self.informacion:
            print(info)
    def hay_informe(self):
        return self.hay_info
    def borar_informe(self):
        self.informacion=[]
        self.hay_info=False