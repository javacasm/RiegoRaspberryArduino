# Test de cmara

import camara
from time import sleep

camera = camara.initCamera() # creamos el objeto camara

for i in range(1, 3):
    camara.getImage(camera)
    sleep(1)