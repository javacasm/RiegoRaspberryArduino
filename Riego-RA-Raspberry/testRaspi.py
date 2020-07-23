#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Test of Raspi functionality
    Licencia CC by @javacasm    
    Julio de 2020
 """

import raspi

v = '0.3'

raspi.init()

temp = raspi.getTemp()

print('Temperatura: ' + temp)

throttled = raspi.getThrottled()

print('Throtted: ' + throttled)

df = raspi.getDiskUsed()

print('Disk Used: ' + df)
