import RPi.GPIO as g
from time import sleep

pin = 25

g.setmode(g.BCM)
g.setwarnings(False)
g.setup(pin,g.OUT)

g.output(pin,g.HIGH)
print "output HIGH, LED on"
sleep(2)


g.output(pin,g.LOW)
print "output LOW, LED off"
sleep(444)
