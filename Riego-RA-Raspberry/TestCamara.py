# Test de cmara

from picamera import PiCamera
from time import sleep
from datetime import datetime
import config

camera = PiCamera() # creamos el objeto camara

camera.start_preview() # muestra la previsualizacion
sleep(1) # espera 5 segundos
now = datetime.now() 
date_time = now.strftime("%Y%d%m-%H%M%S")
print("date and time:",date_time)
camera.capture(config.ImagesDirectory + 'image.jpg') # guarda la imagen
camera.stop_preview() # cierra la previsualizacion
