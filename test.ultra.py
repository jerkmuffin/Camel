#!/usr/bin/env python

import time
import threading
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

trig = 14
echo = 2

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

gpio.output(trig, False)
print "Waiting..."
time.sleep(2)

gpio.output(trig, 1)
time.sleep(0.00001)
gpio.output(trig, 0)

while gpio.input(echo) == 0:
    pulse_start = time.time()

while gpio.input(echo) == 1:
    pulse_end = time.time()

duration = pulse_end - pulse_start
distance = duration * 17150
distance = round(distance, 2)

print "distance: %s cm" % distance

gpio.cleanup()
