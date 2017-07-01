import json
import unittest

from datetime import datetime, timedelta
from google.appengine.ext import testbed
from main import app
from models.timing import Timing

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
        self.assertEqual(response.headers['Content-Type'], 'application/json')

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
        self.assertEqual(response.headers['Content-Type'], 'application/json')

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

    def test_fetch_day_timings(self):
        now = datetime.now()
        for i in range(3):
            diff = timedelta(minutes=10)
            timestamp = now - (diff * i)

            Timing(create_time=timestamp, distance='10.0 mi', duration=1234+i).put()

        endpoint = '/api/v1/routes/1/day'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        body = json.loads(response.data)

        self.assertDictEqual(body, {
            'data': [
                {
                    'distance': '10.0 mi',
                    'duration': 1236
                },
                {
                    'distance': '10.0 mi',
                    'duration': 1235
                },
                {
                    'distance': '10.0 mi',
                    'duration': 1234
                }
            ]
        })

    def test_fetch_timings_amount_for_past_day(self):
        now = datetime.now()
        for i in range(150):
            diff = timedelta(minutes=10)
            timestamp = now - (diff * i)

            Timing(create_time=timestamp, distance='10.0 mi', duration=1234+i).put()

        endpoint = '/api/v1/routes/1/day'
        response = self.app.get(endpoint)
        self.assertEqual(response.status_code, 200)

        body = json.loads(response.data)
        self.assertEqual(len(body['data']), 144)
