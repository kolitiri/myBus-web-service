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

	api_name = data['application']['apiName']

	api = None
	if api_name == 'TflApi':
		api = apis.TflApi(api_name)

	if api is not None:
		resp = api.make_stops_request(data)
		return jsonify(resp)
	else:
		abort(400)


@app.route('/predictions', methods=['POST'])
def get_predictions():

	data = request.get_json()

	api_name = data['application']['apiName']

	api = None
	if api_name == 'TflApi':
		api = apis.TflApi(api_name)	

	if api is not None:
		resp = api.make_predictions_request(data)
		return jsonify(resp)
	else:
		abort(400)


if __name__ == '__main__':
	app.run()
