import sys
import logging

from flask import (
    abort,
    Flask,
    jsonify,
    request,
)

import apis


app = Flask(__name__)

@app.route('/stops', methods=['POST'])
def get_stops():
    data = request.get_json()

    api = apis.TflApi()

    resp = api.make_stops_request(data)

    if resp:
        return jsonify(resp)
    else:
        # Request either failed of was not 200
        abort(500)

@app.route('/predictions', methods=['POST'])
def get_predictions():

    data = request.get_json()

    api = apis.TflApi()

    resp = api.make_predictions_request(data)

    if resp:
        return jsonify(resp)
    else:
        # Request either failed of was not 200
        abort(500)

def set_up_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    )
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


if __name__ == '__main__':
    set_up_logging()
    app.run()
