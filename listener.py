from flask import Flask, request, abort
import logging
import graypy

from runner import activate


# Setup logging
my_logger = logging.getLogger('Keyfob Manager')
my_logger.setLevel(logging.DEBUG)
handler = graypy.GELFUDPHandler('192.168.10.101', 12201)
my_logger.addHandler(handler)


# setup flask app
app = Flask(__name__)

# route to lisen for post requests (i.e. http://IP:PORT/json_webhook )
@app.route('/json_webhook', methods=['POST'])
def json_example():

    # set up some variables we need
    header = request.headers
    data = request.get_json()
    thing = data['thing'].strip().lower()

    # check if "Auth" included in header
    # this is *not* good security, but helps cut down on bots
    if "Auth" not in header or header['Auth'] != "AAAAC3NzaC1lZDI1NTE5AAAAIFCU8Ss0/oYc91EmrOJTZrqE0C1uAlHDZoYYIA0+zL+7":
        my_logger.debug(f"Invalid auth token: {header}")
        return ("Invalid Token", abort(401))

    # if the request header includes our super duper special auth token:
    elif header['Auth'] == "AAAAC3NzaC1lZDI1NTE5AAAAIFCU8Ss0/oYc91EmrOJTZrqE0C1uAlHDZoYYIA0+zL+7":

        my_logger.debug(f"Request: {data}")
        # if the requested "thing" is valid (in runner.py), then the request is "good"
        # you need to check runner.py to make sure the "thing" was activated correctly though
        if activate(thing):
            response = {"type":"webhook_response","object":thing,"status":"valid"}
            my_logger.debug(response)
            return (response, 200)

        # else if the "thing" is not in the approved list:
        else:
            reponse = {"type":"webhook_response","object":thing,"status":"invalid"}
            my_logger.debug(response)
            return (response, abort(400))

    # all other outcomes:
    else:
        return ("Unknown error - impressive", abort(500))


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=False)
