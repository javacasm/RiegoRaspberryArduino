# Arduino stuff from inopya

import sys

# ACCESO AL PUERTO SERIE (para comunicarse con Arduino)
import serial  
import time
import config
import utils

v = '0.75'

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
    
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES ARDUINO / SERIAL
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

def detectarPuertoArduino():   #version mejorada 2018
    '''
    Funcion para facilitar la deteccion del puerto Serie en distintos sistemas operativos
    Escanea los posibles puertos y retorna el nombre del puerto con el que consigue comunicarse
    '''

    #Reconocer el tipo de sistema operativo
    sistemaOperativo = sys.platform
    
    #Definir los prefijos de los posibles puertos serie disponibles tanto en linux como windows
    puertosWindows = ['COM']
    puertosLinux = ['/dev/ttyUSB', '/dev/ttyACM',   '/dev/ttyAMA','/dev/ttyS', '/dev/ttyACA']
    
#    puertoSerie = ''
    if (sistemaOperativo == 'linux' or sistemaOperativo == 'linux2'):
        listaPuertosSerie = puertosLinux
        index = 0
    else:
        listaPuertosSerie = puertosWindows
        index = 4  # Windows suele reservar los 3 primeros puertos. Cambiar este indice si no detectamos nada
        
    for sufijo in listaPuertosSerie:
        for n in range(index, 5):
            try:
                # intentar crear una instancia de Serial para 'dialogar' con ella
                nombrePuertoSerie = sufijo + '%d' %n
                print ("Probando... ", nombrePuertoSerie)
                #time.sleep(0.5)
                serialTest = serial.Serial(nombrePuertoSerie, config.VELOCIDAD_PUERTO_SERIE)
                # serialTest.close()
                # return nombrePuertoSerie
                return serialTest,nombrePuertoSerie
            except NameError as error:
                pass
            except Exception as error:
                print('Exception',error)
                pass
        
    return None, ''  #si llegamos a este punto es que no hay Arduino disponible

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def sendCommand(arduinoSerialPort, command,PAUSA):
    arduinoSerialPort.write(command)
    getDataArduino(arduinoSerialPort,PAUSA)


def readAllData(arduinoSerialPort):
    codificado = ''
    while arduinoSerialPort.inWaiting()>0 :  
        datos = arduinoSerialPort.readline()
        codificado += datos.decode("utf-8")
        time.sleep(0.1)

    return codificado

def sendCommand(arduinoSerialPort, command):
    arduinoSerialPort.write(command + config.endCommand)


def getDataArduino(arduinoSerialPort,PAUSA):
    '''
    Funcion para acceso a ARDUINO y obtencion de datos en tiempo real   ---
    version mejorada para evitar errores de comunicacion
    ante eventuales fallos de la conexion.
    '''
   #  global arduinoSerialPort
    FLAG_buscandoConexion = False

    try:
        arduinoSerialPort.flushInput() #eliminar posibles restos de lecturas anteriores
        arduinoSerialPort.flushOutput()#abortar comunicaciones salientes que puedan estar a medias

    except Exception as e :
        utils.myLog ("Error getDataArduino: " + str(e))
 
    try:
        #enviar comando para que ARDUINO reaccione. El prefijo b (byte) es opcional en python 2.x pero obligatorio en 3.x
        sendCommand(config.getDataCommand) 
        utils.myLog("Sent " + str(config.getDataCommand) + ' command')
        #pausa para que arduino tenga tiempo de reaccionar y dejar la informacion en el puerto Serie
        time.sleep(PAUSA)
        #revisar si hay datos en el puerto serie
        datos = readAllData(arduinoSerialPort)
    except Exception as e:
        utils.myLog('Error: ' + str(e))
        #si llegamos aqui es que se ha perdido la conexion con Arduino  :(
        print ("\n_______________________________________________")
        if FLAG_buscandoConexion == False:      #primera vez que llegamos aqui
            print ("\n == CONEXION PERDIDA == ")
            FLAG_buscandoConexion = True        #para no repetir el texto mientras se reestablece la conexion

        tiempoInicio = time.time()
        ActualTime = time.time()
        print ("    Reconectando...")
        while (ActualTime - tiempoInicio < 10): #Control del tiempo entre consultas de ARDUINO  :)
            arduinoSerialPort.close() #cerrar puerto anterior por seguridad
            arduinoSerialPort,puertoDetectado = detectarPuertoArduino() #detactamos automaticamente el puerto
            ActualTime = time.time()
            if (puertoDetectado != ''):
               # arduinoSerialPort = serial.Serial(puertoDetectado, VELOCIDAD_PUERTO_SERIE) #usamos el puerto detectado
                print ("\n")
                FLAG_buscandoConexion = False
                print (" ** COMUNICACION REESTABLECIDA en "  + puertoDetectado + " ** \n")
                print (utils.epochDate(time.time()))
                print ("_______________________________________________\n\n")
                break
    print ("Arduino sin datos disponibles")
    return None   # notificamos un problema de lectura de datos para que se intente tomar otra muestra lo antes posible

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  
     