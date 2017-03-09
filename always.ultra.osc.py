#!/usr/bin/env python

import time
import threading
import RPi.GPIO as gpio
import OSC as osc

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

# trig = 14
# echo = 2
target = 20


class SendOsc(object):
    def __init__(self, ip=None, port=None, address=None):
        # self.ip = ip
        # self.port = port
        self.osc = osc.OSCClient()
        self.msg = osc.OSCMessage()

        self.osc.connect((ip, port))
        self.msg.setAddress(address)

    def note_on(self):
        self.msg.append(1)
        self.osc.send(self.msg)
        print "sending: %s" % self.msg
        self.msg.clearData()

    def note_off(self):
        self.msg.append(0)
        self.osc.send(self.msg)
        print "sending: %s" % self.msg
        self.msg.clearData()


class Ultra(object):
    def __init__(self, trig=None, echo=None, osc_object=None):
        self.trig = trig
        self.echo = echo
        self.target = target
        self.osc_object = osc_object

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
            self.osc_object.note_off()
        else:
            print cm
            self.osc_object.note_on()


pairs = [(14, 2), (15, 3), (18, 4)]  # 24/27 25/22

oscu = SendOsc("192.168.11.159", 8000, "/fart/u")
oscv = SendOsc("192.168.11.159", 8000, "/fart/v")

u = Ultra(trig=14, echo=2, osc_object=oscu)
v = Ultra(trig=15, echo=3, osc_object=oscv)


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
