#!/usr/bin/env python

import OSC as osc
import threading
import random
import time

ip = "192.168.11.159"
port = 8000
brain = 1

o = osc.OSCClient()
o.connect((ip, port))
m = osc.OSCMessage()
# m.setAddress("/fart/channel")


def activate(channel):
    m.setAddress("/%s/%s" % (brain, channel))

    m.append(1)
    print m
    o.send(m)
    m.clearData()

    time.sleep(5)

    m.append(0)
    print m
    o.send(m)
    m.clearData()


n = random.Random()
while True:
    num = n.randint(1, 5)
    t = threading.Thread(target=activate, args=(num,))
    t.start()
    time.sleep(.5)
