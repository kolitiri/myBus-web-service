import json
import logging
import requests


class Api():
    """ API class. """
    def __init__(self):
        self.log = logging.getLogger('flask.app.apis')


class TflApi(Api):
    """ TFL API class """
    def __init__(self):
        super().__init__()
        self.stops_domain = 'https://api.tfl.gov.uk/StopPoint'

    def make_stops_request(self, data):
        """ Make a stops request to TFL Unified API

            Example request:
                https://api.tfl.gov.uk/Stoppoint?
                lat=51.488998&lon=-0.284000&radius=300&
                stoptypes=NaptanPublicBusCoachTram&returnLines=False

            Args:
                data (dict): The request data

            Returns:
                (status, stopPoints) (tuple): The status of the request to TFL,
                                                along with the response data if
                                                the request was successful
        """
        try:
            params = {
                'lat': data['location']['latitude'],
                'lon': data['location']['longtitude'],
                'radius': data['location']['radius'],
                'stopTypes': data['location']['stopTypes'],
                'returnLines': data['location']['returnLines'],
            }
        except KeyError:
            return 400, None

        try:
            r = requests.get(self.stops_domain, params=params)
        except requests.exceptions.RequestException as e:
            self.log.error('TFL Api request failed:{}'.format(e))
            return 500, None

        if r.status_code != 200:
            self.log.info(
                'TFL Api request failed with status:{}'.format(r.status_code)
            )
            return r.status_code, None

        try:
            tfl_resp = r.json()
        except json.decoder.JSONDecodeError as e:
            # TFL endpoint might be wrong
            self.log.error('JSONDecodeError:{}'.format(e))
            return 500, None

        # Filter the response and return only required fields
        # stopLetter, naptanId, distance
        stopPoints = {'stopPoints': []}
        for stoppoint in tfl_resp['stopPoints']:
            try:
                node = {
                    'stopLetter': stoppoint['stopLetter'],
                    'naptanId': stoppoint['naptanId'],
                    'distance': stoppoint['distance'],
                }
                stopPoints['stopPoints'].append(node)
            except KeyError:
                # Unfortunately some stopPoints are
                # inconsistent. Ignore them for now 
                continue

        return r.status_code, stopPoints

    def make_predictions_request(self, data):
        """ Make a predictions requests to TFL Unified API

            Example request:
                https://api.tfl.gov.uk/StopPoint/490007705L/Arrivals?mode=bus

            Args:
                data (dict): The request data

            Returns:
                (status, predictions) (tuple): The status of the request to TFL,
                                                along with the response data if
                                                the request was successful
        """
        params = {
            'mode': 'bus'
        }

        try:
            naptanId = data['stop']['naptanId']
        except KeyError:
            return 400, None

        url = '{}/{}/Arrivals'.format(self.stops_domain, naptanId)

        try:
            r = requests.get(url, params=params)
        except requests.exceptions.RequestException as e:
            self.log.error('TFL Api request failed:{}'.format(e))
            return 500, None

        if r.status_code != 200:
            self.log.info(
                'TFL Api request failed with status:{}'.format(r.status_code)
            )
            return r.status_code, None

        try:
            tfl_resp = r.json()
        except json.decoder.JSONDecodeError as e:
            # TFL endpoint might be wrong
            self.log.error('JSONDecodeError:{}'.format(e))
            return 500, None

        # Filter the response and return only required fields
        # lineName, timeToStation
        predictions = []
        for prediction in tfl_resp:
            node = {
                'lineName': prediction['lineName'],
                'timeToStation': prediction['timeToStation'],
            }
            predictions.append(node)

        return r.status_code, predictions
