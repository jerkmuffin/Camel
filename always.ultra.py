#!/usr/bin/env python

import time
import threading
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# trig = 14
# echo = 2
target = 20


class Ultra(object):
    def __init__(self, trig=None, echo=None):
        self.trig = trig
        self.echo = echo
        self.target = target

        print "trig %s" % self.trig
        print "echo %s" % self.echo

        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

    def create(self):
        gpio.output(self.trig, 1)
        time.sleep(0.00001)
        gpio.output(self.trig, 0)

        while gpio.input(self.echo) == 0:
            self.pulse_start = time.time()

        while gpio.input(self.echo) == 1:
            self.pulse_end = time.time()

    def calculate(self):
        duration = self.pulse_end - self.pulse_start
        distance = duration * 17150
        distance = round(distance, 2)
        return distance

    def update(self):
        self.create()
        cm = self.calculate()
        if cm > self.target:
            pass
        else:
            print cm


pairs = [(14, 2), (15, 3), (18, 4)]  # 24/27 25/22
u = Ultra(trig=14, echo=2)
v = Ultra(trig=15, echo=3)


def go(letter):
    while True:
        letter.update()
        time.sleep(.1)


print 'starting u'
t = threading.Thread(target=go, args=(u,))
t.start()

print 'starting v'
x = threading.Thread(target=go, args=(v,))
x.start()
