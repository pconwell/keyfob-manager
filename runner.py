import RPi.GPIO as GPIO
import requests
from time import sleep
import logging
import graypy


# Setup logging
my_logger = logging.getLogger('Keyfob Manager')
my_logger.setLevel(logging.DEBUG)
handler = graypy.GELFUDPHandler('192.168.10.101', 12201)
my_logger.addHandler(handler)


# create dictionary of acceptable key works -> gpio pin numbers
things = {'house' : 21,
          'alarm' : 21,
          'lexus' : 22,
          'ads' :   None}

# Setup GPIO
GPIO.setmode(g.BOARD)
GPIO.setwarnings(False)
GPIO.setup(list(things.values()),GPIO.OUT)


def button_press(pin, duration):

    GPIO.output(pin, GPIO.HIGH)
    sleep(duration)
    GPIO.output(pin, GPIO.LOW)


def activate(thing, things=things):
    # activate a thing
    # set pin high (button press) for 2 seconds then low (button release)

    if thing not in things:
        my_logger.debug(f"ACTIVATE: invalid {thing}")
        return False

    elif thing == 'ads':
        my_logger.debug(f"ACTIVATE: valid {thing}")
        requests.get('http://192.168.1.103/admin/api.php?disable=900&auth=')
        return True

    else:
        my_logger.debug(f"ACTIVATE: valid {thing}")
        button_press(things[thing], 2)
        return True


if __name__ == '__main__'

    activate('alarm', things)
    activate('lexus', things)
