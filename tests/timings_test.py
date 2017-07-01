import json
import mock
import unittest

from google.appengine.ext import testbed
from main import app
from models.timing import Timing

class TimingsTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.app = app.test_client()

    @mock.patch('services.gmaps.googlemaps.Client')
    def test_mark_route_datapoint(self, mock_gmaps):
        map_payload = [
            {
                'summary': 'US-101 S',
                'legs': [
                    {
                        'distance': { 'text': 'distance' },
                        'duration_in_traffic': { 'value': 1111 }
                    }
                ],
                'duration': { 'value': 9999 }   # default duration
            }
        ]
        # todo: assert parameters
        mock_gmaps.return_value.directions.return_value = map_payload

        endpoint = '/api/v1/timings/1'
        response = self.app.get(endpoint)
        self.assertEqual(response.status_code, 204)

        query_results = Timing.query().fetch(2)
        self.assertEqual(len(query_results), 1)

        test_data = query_results.pop()
        self.assertEqual(test_data.duration, 1111)
        self.assertEqual(test_data.distance, 'distance')
