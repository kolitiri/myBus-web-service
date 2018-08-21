import requests

class Api():
	def __init__(self, api_name):
		self.api_name = api_name

	def _make_request(self, type, url, params=None, data=None):
		if type == 'GET':
			resp = requests.get(url, params=params).json()

		return resp


class TflApi(Api):
	def __init__(self, api_name):
		super().__init__(api_name)
		self.stops_domain = 'https://api.tfl.gov.uk/StopPoint'

	def make_stops_request(self, data):

		params = {
			'lat': data['location']['latitude'],
			'lon': data['location']['longtitude'],
			'radius': data['location']['radius'],
			'stopTypes': data['location']['stopTypes'],
			'returnLines': data['location']['returnLines'],
		}

		# https://api.tfl.gov.uk/Stoppoint?lat=51.488998&lon=-0.284000&radius=300&stoptypes=NaptanPublicBusCoachTram&returnLines=False
		resp = self._make_request('GET', self.stops_domain, params=params)

		# Filter the response and return only required fields
		# stopLetter, naptanId, distance

		stopPoints = {'stopPoints': []}
		for sp in resp['stopPoints']:
			try:
				ret = {
					'stopLetter': sp['stopLetter'],
					'naptanId': sp['naptanId'],
					'distance': sp['distance'],
				}
				stopPoints['stopPoints'].append(ret)
			except KeyError:
				continue

		return stopPoints

	def make_predictions_request(self, data):

		params = {
			'mode': 'bus'
		}

		naptanId = data['stop']['naptanId']

		url = '{}/{}/Arrivals'.format(self.stops_domain, naptanId)

		# https://api.tfl.gov.uk/StopPoint/490007705L/Arrivals?mode=bus
		resp = self._make_request('GET', url, params=params)

		# Filter the response and return only required fields
		# lineName, timeToStation

		predictions = []
		for pre in resp:
			ret = {
				'lineName': pre['lineName'],
				'timeToStation': pre['timeToStation'],
			}
			predictions.append(ret)

		return predictions






