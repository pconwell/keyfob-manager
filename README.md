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
sudo apt install python3-pip python3-flask
pip3 install flask
```


arm.py
``` python
from flask import Flask, request, abort

import RPi.GPIO as g
from time import sleep

things = {'house': 4,
          'bmw': 6,
          'lexus' : 5}

g.setmode(g.BCM)
g.setwarnings(False)
g.setup(things['bmw'],g.OUT)
g.setup(things['lexus'],g.OUT)
g.setup(things['house'],g.OUT)

def activate(pin):
        print("output high, LED on, pressing button")
        g.output(pin,g.HIGH)
        sleep(2)
        print("output low, LED off, released button")
        g.output(pin,g.LOW)
        sleep(1)

app = Flask(__name__)


@app.route('/webhook', methods=['GET'])
def webhook():

    thing = request.args['thing']

    thing = thing.strip().lower()

    try:
        activate(things[thing])
    except ValueError:
        print("that thing doesn't exist")

    return  ''' The thing is: {} '''.format(thing)
    #abort(400)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80, debug=True)
```
