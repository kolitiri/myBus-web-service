import logging
import sys

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
    """ This endpoint should handle requests for stops
        by instantiating an apis.Api object.

        Currently only TflApi objects are supported.
    """
    data = request.get_json(force=False)

    api = apis.TflApi()

    if data:
        status_code, resp = api.make_stops_request(data)

        if status_code == 200 and resp:
            return jsonify(resp)
        else:
            abort(status_code)
    else:
        # content-type was not application/json
        abort(415)

@app.route('/predictions', methods=['POST'])
def get_predictions():
    """ This endpoint should handle requests for bus
        time predictions by instantiating an API object.

        Currently only TflApi objects are supported.
    """
    data = request.get_json(force=False)

    api = apis.TflApi()

    if data:
        status_code, resp = api.make_predictions_request(data)

        if status_code == 200 and resp is not None:
            return jsonify(resp)
        else:
            abort(status_code)
    else:
        # content-type was not application/json
        abort(415)

def set_up_logging():
    """ Sets up logging for the application """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    )
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


if __name__ == '__main__':
    set_up_logging()
    app.run(debug=False)
