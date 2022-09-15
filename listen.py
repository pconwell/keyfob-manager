from flask import Flask, request, abort

import RPi.GPIO as g
from time import sleep
import logging
import graypy
import requests

my_logger = logging.getLogger('Keyfob Manager')
my_logger.setLevel(logging.DEBUG)

handler = graypy.GELFUDPHandler('192.168.10.101', 12201)
my_logger.addHandler(handler)


things = {'house': 4,
          'alarm': 4,
          'bmw': 6,
          'lexus' : 5}

g.setmode(g.BCM)
g.setwarnings(False)
g.setup(things['bmw'],g.OUT)
g.setup(things['alarm'],g.OUT)
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
    my_logger.debug(f"WEBHOOK_REQUEST: '{thing}'")

    if thing in ["adblocker","ad blocker","%20ad%20blocker"]:
        requests.get('http://192.168.1.103/admin/api.php?disable=900&auth=')
        return f'{{"TYPE":"WEBHOOK_REQUEST","object":"{thing}"}}'

    else:

        try:
            activate(things[thing])
            my_logger.debug(f"WEBHOOK_REQUEST: valid {thing}")
            return f'{{"TYPE":"WEBHOOK_REQUEST","object":"{thing}"}}'
        except KeyError:
            #print("that thing doesn't exist")
            my_logger.debug(f"WEBHOOK_REQUEST: invalid {thing}")
            abort(404)

        #return f"'WEBHOOK_REQUEST': '{thing}'"
        #abort(400)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=False)
