import time
import serial  
import config
import utils
import arduinoUtils

v = '0.5'




PAUSA = 0.5
RESET  = 5
try:
    arduinoSerialPort = serial.Serial('/dev/ttyUSB0', config.VELOCIDAD_PUERTO_SERIE)

    time.sleep(RESET * PAUSA)

    datos = arduinoUtils.readAllData(arduinoSerialPort)
    utils.myLog(datos)

    # getData
    arduinoUtils.sendCommand(arduinoSerialPort, config.getDataCommand)

    time.sleep(PAUSA)

    datos = arduinoUtils.readAllData(arduinoSerialPort)
    utils.myLog(datos)

    # Turn On Rele 3
    command = config.setReleCommand + str(3).encode('utf-8') + config.releOnCommand 
    arduinoUtils.sendCommand(arduinoSerialPort,command)

    time.sleep(PAUSA)

    datos = arduinoUtils.readAllData(arduinoSerialPort)
    utils.myLog(datos)

    # Turn On Rele 5
    command = config.setReleCommand + str(5).encode('utf-8') + config.releOnCommand 
    arduinoUtils.sendCommand(arduinoSerialPort,command)

    time.sleep(PAUSA)

    datos = arduinoUtils.readAllData(arduinoSerialPort)
    utils.myLog(datos)

    # getData
    arduinoUtils.sendCommand(arduinoSerialPort,config.getDataCommand)

    time.sleep(PAUSA)

    datos = arduinoUtils.readAllData(arduinoSerialPort)
    utils.myLog(datos)    

    # get help
    arduinoUtils.sendCommand(arduinoSerialPort,config.helpCommand)

    time.sleep(PAUSA)

    datos = arduinoUtils.readAllData(arduinoSerialPort)
    utils.myLog(datos)    

        
except Exception as error:
    utils.myLog("Error: " + str(error))