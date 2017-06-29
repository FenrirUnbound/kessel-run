import json
import unittest

from google.appengine.ext import testbed
from main import app

class RoutesTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.app = app.test_client()

    def test_list_routes(self):
        endpoint = '/api/v1/routes'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.data)

        self.assertDictEqual(body, {
            'data': [
                {
                    'id': 1,
                    'name': 'Valley Fair',
                    'origin': '701 1st Avenue, Sunnyvale, CA 94089',
                    'destination': '2855 Stevens Creek Blvd, Santa Clara, CA 95050'
                }
            ]
        })

    def test_fetch_specific_route(self):
        endpoint = '/api/v1/routes/1'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.data)

        self.assertDictEqual(body, {
            'data': {
                'id': 1,
                'name': 'Valley Fair',
                'origin': '701 1st Avenue, Sunnyvale, CA 94089',
                'destination': '2855 Stevens Creek Blvd, Santa Clara, CA 95050'
            }
        })

    def test_fail_missing_route(self):
        endpoint = '/api/v1/routes/89'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 404)
