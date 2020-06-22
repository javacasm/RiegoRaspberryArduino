"""
Todo lo relacionado con la camara
"""


from picamera import PiCamera
from time import sleep
from datetime import datetime
import config
import utils

v = '0.9.5'

def initCamera():
    camera = PiCamera() # creamos el objeto camara
    return camera
    

def getImage(camera, preview = False):
    if preview :
        camera.start_preview() # muestra la previsualizacion
        sleep(1) # espera 5 segundos
    now = datetime.now() 
    date_time = now.strftime("%Y%d%m-%H%M%S")
    fileName = 'image' + date_time + '.jpg'
    fullName = config.ImagesDirectory + fileName
    utils.myDebug("image - " + fullName)

    camera.capture(fullName) # guarda la imagen
    
    if preview : camera.stop_preview() # cierra la previsualizacion
    
    return fullName