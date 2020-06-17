# Utils

import time
import datetime

v = '1.1'

class RelojLOCAL:
    '''
    Classe para el control personal de los tiempos.
    crea un reloj con la hora local del sistema en el que corre el sistema de registro de datos
    El reloj adquiere la fecha/hora actuales al iniciarse, y
    OJO, solo se actualiza con el metodo update()
    y hasta ese momento mantiene el anterior registro de fecha/hora
    '''
    def __init__(self):
        self.update()
        
    def update(self):        
        #self.tiempo_gmt = time.strftime("%Y_%m_%d-%H:%M:%S", time.gmtime(time.time()))   #hora gmt
        self.tiempo_str = time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime(time.time())) #hora local
        self.tiempo = time.time() #float del tiempo GMT
        self.fechayhora = self.tiempo_str[:]

        self.fecha = self.tiempo_str[0:10]
        self.reloj = self.tiempo_str[11:]

        self.year = self.tiempo_str[0:4]
        self.mes = self.tiempo_str[5:7]
        self.dia = self.tiempo_str[8:10]

        self.hora = self.tiempo_str[11:13]
        self.minuto = self.tiempo_str[14:16]
        self.segundo = self.tiempo_str[17:19]

                
#----------------------------------------------------------------------------------------------------
# FIN BLOQUE DE DEFINICION DE CLASES
#----------------------------------------------------------------------------------------------------


def epochDate(epoch):
    '''
    Funcion para convertir un tiempo epoch en fecha/hora 'humana'
    Usado para imprimir los tiempos que forman parte de los detalles de los telegramas y mensajes de consola
    '''
    fechaHora = time.strftime("%Y-%m-%d , %H:%M:%S", time.localtime(epoch))
    return fechaHora

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  


def getStrDateTime():
    return str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")) 

def getStrDateTimeMilis():
    return str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")) 

def myLog(message):
    print(getStrDateTime()+ " " + message)
