import json
from requests import Response
import unittest
from unittest.mock import (
    Mock,
    patch
)

import gmmybus


GET_STOPS_TESTING_SCENARIOS = [
    {
        'description': 'Testing status 200',
        # Incoming request data to /stops
        'request_data': {
            "location": {
                "latitude": "51.492628",
                "longtitude": "-0.223060",
                "radius": "200",
                "stopTypes": "NaptanPublicBusCoachTram",
                "returnLines": "False"
            }
        },
        # Expected response from a request to /stops
        'exp_response': {
            "stopPoints": [
                {
                    "distance": 32.65928570759986,
                    "naptanId": "490008688P",
                    "stopLetter": "H"
                },
            ]
        },
        # Expected status of a request to /stops
        'exp_status': 200,
        # Response from a request to the TFL Api
        'tfl_resp': {
            "stopPoints": [
                {
                    "naptanId": "490008688P",
                    "distance": 32.65928570759986,
                    "indicator": "Stop H",
                    "stopLetter": "H",
                    "icsCode": "1008688",
                    "stopType": "NaptanPublicBusCoachTram",
                    "stationNaptan": "490G000617",
                    "lat": 51.488231,
                    "lon": -0.287386
                },
            ]
        },
        # Status of a request to /stops
        'tfl_status': 200,
    },
    {
        'description': 'Testing status 400 Bad Request',
        'request_data': {
            "loca": {
                "latitude": "51.492628",
                "longtitude": "-0.223060",
                "radius": "200",
                "stopTypes": "NaptanPublicBusCoachTram",
                "returnLines": "False"
            }
        },
        'exp_response': None,
        'exp_status': 400,
        'tfl_resp': None,
        'tfl_status': None,
    },
]

GET_PREDICTIONS_TESTING_SCENARIOS = [
    {
        'description': 'Testing status 200',
        'request_data': {
            'stop': {
                'naptanId': '490004290L'
            }
        },
        'exp_response': [
            {
                "lineName": '237',
                "timeToStation": 794
            }
        ],
        'exp_status': 200,
        'tfl_resp': [
            {
                "vehicleId": "LK10BXV",
                "naptanId": "490004290L",
                "stationName": "Brentford Fountain Leisure Centre",
                "lineId": "237",
                "lineName": "237",
                "platformName": "K",
                "timeToStation": 794
            }
        ],
        'tfl_status': 200,
    },
    {
        'description': 'Testing status 400 Bad Request',
        'request_data': {
            'st': {
                'nanId': '490004290L'
            }
        },
        'exp_response': None,
        'exp_status': 400,
        'tfl_resp': None,
        'tfl_status': None,
    },
]

class GmmybusTestCase(unittest.TestCase):

    def setUp(self):
        gmmybus.app.testing = True
        self.app = gmmybus.app.test_client()

    def test_get_stops(self):

        for data in GET_STOPS_TESTING_SCENARIOS:
            with patch('apis.requests.get') as get_request:
                # Create a fake Response object
                mock_tfl_resp = Mock(spec=Response)
                mock_tfl_resp.json.return_value = data['tfl_resp']
                mock_tfl_resp.status_code = data['tfl_status']

                get_request.return_value = mock_tfl_resp

                response = self.app.post(
                        '/stops',
                        data=json.dumps(data['request_data']),
                        content_type='application/json'
                )

                self.assertEqual(response.status_code, data['exp_status'])

                # Compare content only if there is an actual json response
                if response.get_json(force=False):
                    self.assertDictEqual(response.get_json(force=False), data['exp_response'])

    def test_get_predictions(self):

        for data in GET_PREDICTIONS_TESTING_SCENARIOS:
            with patch('apis.requests.get') as get_request:
                # Create a fake Response object
                mock_tfl_resp = Mock(spec=Response)
                mock_tfl_resp.json.return_value = data['tfl_resp']
                mock_tfl_resp.status_code = data['tfl_status']

                get_request.return_value = mock_tfl_resp

                response = self.app.post(
                        '/predictions',
                        data=json.dumps(data['request_data']),
                        content_type='application/json'
                )

                self.assertEqual(response.status_code, data['exp_status'])

                # Compare content only if there is an actual json response
                if response.get_json(force=False):
                    self.assertEqual(response.get_json(force=False), data['exp_response'])


if __name__ == '__main__':
    unittest.main()