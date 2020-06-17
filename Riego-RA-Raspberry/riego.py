
import config
import arduinoUtils
import utils


v = '0.1'

arduinoSerialPort = None

def init(portArduino):
    arduinoSerialPort == portArduino

def bombaOn():
    enciendeRele(config.ReleBomba)

def bombaOff():
    apagaRele(config.ReleBomba)    
    
def riegoOn():
    for i in config.Sectores:
        riegonOnSector(i)

def riegoOff():
    for i in config.Sectores:
        riegonOffSector(i)

def riegoOnSector(sectorID):
    if sectorID not in config.Sectores:
        utils.myLog("Sector {} no definido".format(sectorID))
    enciendeRele(sectorID)
    bombaOn()

def riegoOffSector(sectorID):
    if sectorID not in config.Sectores:
        utils.myLog("Sector {} no definido".format(sectorID))
    apagaRele(sectorID)
    bombaOff()

def enciendeRele(releID):
    global arduinoSerialPort
    if arduinoSerialPort != None:
        arduinoUtils.sendCommand(config.setReleCommand + str(releID) + config.releOnCommand)
    else:
        utils.myLog('arduinoSerialPort == None')

def apagaRele(releID):
    global arduinoSerialPort
    if arduinoSerialPort != None:
        arduinoUtils.sendCommand(config.setReleCommand + str(releID) + config.releOffCommand)
    else:
        utils.myLog('arduinoSerialPort == None')      

def getFullData():
    arduinoUtils.getDataArduino(arduinoSerialPort,config.TimeoutRespuesta)