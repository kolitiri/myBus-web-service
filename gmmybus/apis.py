import requests
import logging


class Api():
    def __init__(self):
        self.log = logging.getLogger('flask.app.apis')


class TflApi(Api):
    def __init__(self):
        super().__init__()
        self.stops_domain = 'https://api.tfl.gov.uk/StopPoint'

    def make_stops_request(self, data):
        """ Make a stops request TFL Unified API

            https://api.tfl.gov.uk/Stoppoint?
            lat=51.488998&lon=-0.284000&radius=300&
            stoptypes=NaptanPublicBusCoachTram&returnLines=False
        """
        params = {
            'lat': data['location']['latitude'],
            'lon': data['location']['longtitude'],
            'radius': data['location']['radius'],
            'stopTypes': data['location']['stopTypes'],
            'returnLines': data['location']['returnLines'],
        }

        try:
            r = requests.get(self.stops_domain, params=params)
        except requests.exceptions.RequestException as e:
            self.log.error(e)
            return

        if r.status_code != 200:
            self.log.info(
                'TFL Api request failed with status:{}'.format(r.status_code)
            )
            return

        # TODO: Need to catch JSONDecodeError
        tfl_resp = r.json()

        # Filter the response and return only required fields
        # stopLetter, naptanId, distance
        stopPoints = {'stopPoints': []}
        for sp in tfl_resp['stopPoints']:
            try:
                ret = {
                    'stopLetter': sp['stopLetter'],
                    'naptanId': sp['naptanId'],
                    'distance': sp['distance'],
                }
                stopPoints['stopPoints'].append(ret)
            except KeyError:
                # Unfortunately some stopPoints are
                # inconsistent. Ignore them for now 
                continue

        return stopPoints

    def make_predictions_request(self, data):
        """ Make a predictions requests to TFL Unified API

            https://api.tfl.gov.uk/StopPoint/490007705L/Arrivals?mode=bus
        """

        params = {
            'mode': 'bus'
        }

        naptanId = data['stop']['naptanId']

        url = '{}/{}/Arrivals'.format(self.stops_domain, naptanId)

        try:
            r = requests.get(url, params=params)
        except requests.exceptions.RequestException as e:
            self.log.error(e)
            return

        if r.status_code != 200:
            self.log.info(
                'TFL Api request failed with status:{}'.format(r.status_code)
            )
            return

        # TODO: Need to catch JSONDecodeError
        tfl_resp = r.json()

        # Filter the response and return only required fields
        # lineName, timeToStation
        predictions = []
        for pre in tfl_resp:
            ret = {
                'lineName': pre['lineName'],
                'timeToStation': pre['timeToStation'],
            }
            predictions.append(ret)

        return predictions
