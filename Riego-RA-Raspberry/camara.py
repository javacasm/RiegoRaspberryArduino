#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Todo lo relacionado con la camara
    Licencia CC by @javacasm    
    Julio de 2020
"""

# Documentacion https://picamera.readthedocs.io/en/release-1.13/recipes1.html

from picamera import PiCamera, Color
from time import sleep
from datetime import datetime
from fractions import Fraction
import config
import utils

v = '1.0.4'

camera = None

def initCamera():
    global camera
    camera = PiCamera() # creamos el objeto camara
    utils.myLog('Init camara')
    return camera

def resolucionMD():
    global camera
    camera.resolution = (1280, 720)

def resolucionHD():
    global camera
    camera.resolution = (2592, 1944)

def resolucionLD():
    global camera
    camera.resolution = (80, 480)

def addText(texto):
    global camera
    # camera.annotate_background = Color('white')
    camera.annotate_foreground = Color('black')
    camera.annotate_text_size = 50
    camera.annotate_text = texto

def addTextNight(texto):
    global camera
    # camera.annotate_background = Color('white')
    camera.annotate_foreground = Color('white')
    camera.annotate_text_size = 50
    camera.annotate_text = texto


def setIso(ISO):
    # 100-200 daylight
    # 400-800 night
    global camera
    camera.iso = ISO
    # Give the camera a good long time to set gains and
    # measure AWB (you may wish to use fixed AWB instead)
    sleep(10)

def addDate():
    addText(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

def addDateNight():
    addTextNight(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

def setStaticPref():
    # https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-consistent-images
    global camera
    camera.iso = 100
    # Wait for the automatic gain control to settle
    sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g

def getImageNight():
    # https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-in-low-light
    global camera
    prevFramerate = camera.framerate
    camera.framerate = Fraction(1,6)
    prevSensorMode = camera.sensor_mode
    camera.sensor_mode = 3
    prevShutter_speed = camera.shutter_speed
    camera.shutter_speed = 6000000
    prevIso = camera.iso
    camera.iso = 800
    # Give the camera a good long time to set gains and
    # measure AWB (you may wish to use fixed AWB instead)
    sleep(30)
    camera.exposure_mode = 'off'
    imageFile = getImage()
    camera.framerate = prevFramerate
    camera.sensor_mode = prevSensorMode
    camera.shutter_speed = prevShutter_speed
    camera.iso = prevIso
    return imageFile

def getImage( preview = False):
    global camera
    if preview :
        camera.start_preview() # muestra la previsualizacion
        sleep(1) # espera 5 segundos
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    fileName = 'image' + date_time + '.jpg'
    fullName = config.ImagesDirectory + fileName
    utils.myDebug("image - " + fullName)
    camera.capture(fullName) # guarda la imagen
    if preview : camera.stop_preview() # cierra la previsualizacion
    return fullName

def closeCamera():
    global camera
    if camera != None:
        camera.close()
    return None
