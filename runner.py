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
# pin 3 (ads) is a pin that I *personaly* won't be using
things = {'house' : 29,
          'alarm' : 29,
          'lexus' : 31,
          'ads'   : 3}

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pin_list = [int(i) for i in things.values()]
GPIO.setup(pin_list,GPIO.LOW)


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


if __name__ == '__main__':

    activate('alarm', things)
    activate('lexus', things)
