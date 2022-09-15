import RPi.GPIO as g
from time import sleep

house = 4
bmw = 6
lexus = 5

g.setmode(g.BCM)
g.setwarnings(False)
g.setup(bmw,g.OUT)
g.setup(lexus,g.OUT)
g.setup(house,g.OUT)



def activate(pin):
	print("output high, LED on, pressing button")
	g.output(pin,g.HIGH)
	sleep(2)
	print("output low, LED off, released button")
	g.output(pin,g.LOW)
	sleep(1)

activate(bmw)
activate(lexus)
activate(house)
