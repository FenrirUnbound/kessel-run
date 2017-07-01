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

    @mock.patch('controllers.timings.googlemaps.Client')
    def test_mark_route_datapoint(self, mock_gmaps):
        map_payload = {
            'rows': [
                {
                    'elements': [
                        {
                            'distance': { 'text': 'distance' },
                            'duration': { 'value': 1111 }
                        }
                    ]
                }
            ]
        }
        mock_gmaps.return_value.distance_matrix.return_value = map_payload

        endpoint = '/api/v1/timings/1'
        response = self.app.get(endpoint)
        self.assertEqual(response.status_code, 204)

        query_results = Timing.query().fetch(2)
        self.assertEqual(len(query_results), 1)

        test_data = query_results.pop()
        self.assertEqual(test_data.duration, 1111)
        self.assertEqual(test_data.distance, 'distance')
