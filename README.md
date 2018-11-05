# keyfob-manager
raspberry pi to control keyfobs (car, house alarm, etc)

## Intro
First and foremost, this is a semi-destructive project - meaning that you will need to 'sacrifice' your keyfob(s) because you will be soldering in leads. This is not a big deal with some cheap keyfobs, such as the [Honeywell 5834-4](https://www.amazon.com/dp/B00SZ304ZK/?coliid=IP6QMZRKBK948) but can be quite a bit more expensive for things like car keyfobs.

Next, the reason this project started is because I have had multiple incidences in which someone has tried to break into my car. I wanted a way to trigger a car lock signal every night at X time. Due to modern security measures, you can't just 'send a signal' to the car. The remotes would be very difficult to mimic, so I believe the easiest approach is to just solder in a transistor that is connected to a raspberry pi.

Once the transistor is wired across the button on the keyfob, it will mimic a button press just as if you had actually physically pressed the button on the fob.

From here, you can simply program the pi in whatever way you want. You can have it press the button at a certain time, or certain conditions or use ifttt webhooks... really, whatever you can imagine.

## temp

![Alt text](layout.png)

```
sudo apt update && sudo apt upgrade -y
sudo apt install python-pip python-flask
pip -u install flask
```


arm.py
``` python
# python 3
import RPi.GPIO as g
from time import sleep

pin = 25

g.setmode(g.BCM)
g.setwarnings(False)
g.setup(pin,g.OUT)

g.output(pin,g.HIGH)
print("output HIGH, LED on, arming house")
sleep(2)


g.output(pin,g.LOW)
print("output LOW, LED off, button released")
#sleep(444)

```
