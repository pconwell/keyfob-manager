from flask import Flask, request, abort
import logging
import graypy

from runner import activate


# Setup logging
my_logger = logging.getLogger('Keyfob Manager')
my_logger.setLevel(logging.DEBUG)
handler = graypy.GELFUDPHandler('192.168.10.101', 12201)
my_logger.addHandler(handler)


app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def webhook():

    thing = request.args['thing'].strip().lower()
    my_logger.debug(f'{{"TYPE":"WEBHOOK_REQUEST","object":"{thing}"}}')

    if activate(thing):
        return f'{{"TYPE":"WEBHOOK_REQUEST","object":"{thing}"}}'

    else:
        return abort(400)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=False)
