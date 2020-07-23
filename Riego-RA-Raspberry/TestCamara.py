#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Test of cámara functionality
    Licencia CC by @javacasm    
    Julio de 2020
 """


import camara
from time import sleep

camera = camara.initCamera() # creamos el objeto camara


def testISO():
    for iso in range(100,900,100):
        message = 'ISO:' + str(iso)
        print(message)
        camara.addText(message)
        camara.setIso(iso)
        camara.getImage()

def testImage():
    for i in range(1, 3):
        camara.addDate()
        camara.getImage()
        sleep(5)

def testImageNight():
    for i in range(1, 3):
        camara.addDateNight()
        camara.getImageNight()
        sleep(5)


testImageNight()

