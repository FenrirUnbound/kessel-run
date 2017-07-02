import json
import unittest

from datetime import datetime, timedelta
from google.appengine.ext import ndb, testbed
from main import app
from models.timing import Timing

class RoutesTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.app = app.test_client()

    def tearDown(self):
        self.app = None
        self.testbed.deactivate()

    def helper_populate_datastore(self, num_of_elements, route_id):
        parent_key = ndb.Key('Route', route_id)
        now = datetime.now()
        time_interval = timedelta(minutes=10)

        elements = []
        for i in range(num_of_elements):
            timestamp = now - (time_interval * i)

            current = Timing(parent=parent_key, create_time=timestamp, distance='10.0 mi', duration=1234+i)
            elements.append(current)

        return ndb.put_multi(elements)

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
                    'name': 'Santa Clara',
                    'origin': '701 1st Avenue, Sunnyvale, CA 94089',
                    'destination': '2855 Stevens Creek Blvd, Santa Clara, CA 95050'
                },
                {
                    'id': 2,
                    'name': 'S. San Jose',
                    'origin': '701 1st Avenue, Sunnyvale, CA 94089',
                    'destination': '1 Curtner Avenue, San Jose, CA 95125'
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
                'name': 'Santa Clara',
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
        time_interval = timedelta(minutes=10)
        self.helper_populate_datastore(num_of_elements=3, route_id=11)

        # unreleated data in the set
        Timing(parent=ndb.Key('Route', 2), create_time=now, distance='9.9 mi', duration=5555).put()

        endpoint = '/api/v1/routes/11/day'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        body = json.loads(response.data)

        self.assertEqual(len(body['data']), 3)
        self.assertDictEqual(body, {
            'data': [
                {
                    'distance': '10.0 mi',
                    'duration': 1236,
                    'timestamp': (now - (time_interval * 2)).strftime('%s')
                },
                {
                    'distance': '10.0 mi',
                    'duration': 1235,
                    'timestamp': (now - (time_interval * 1)).strftime('%s')
                },
                {
                    'distance': '10.0 mi',
                    'duration': 1234,
                    'timestamp': now.strftime('%s')
                }
            ]
        })

    def test_fetch_timings_amount_for_past_day(self):
        now = datetime.now()
        parent_key = ndb.Key('Route', 5)
        # dummy data
        Timing(parent=ndb.Key('Route', 7), create_time=now, distance='9.9 mi', duration=5555).put()

        # target test data
        for i in range(150):
            diff = timedelta(minutes=10)
            timestamp = now - (diff * i)

            Timing(parent=parent_key, create_time=timestamp, distance='10.0 mi', duration=1234+i).put()

        endpoint = '/api/v1/routes/5/day'
        response = self.app.get(endpoint)
        self.assertEqual(response.status_code, 200)

        body = json.loads(response.data)
        self.assertEqual(len(body['data']), 144)
        for element in body['data']:
            self.assertEqual(element['distance'], '10.0 mi')

    def test_fetch_cache(self):
        test_keys = self.helper_populate_datastore(num_of_elements=3, route_id=1)

        Timing(parent=ndb.Key('Route', 2), create_time=datetime.now(), distance='9.9 mi', duration=5555).put()

        endpoint = '/api/v1/routes/1/day'
        response = self.app.get(endpoint)
        body = json.loads(response.data)

        self.assertEqual(len(body['data']), 3)

        ndb.delete_multi(test_keys)

        response = self.app.get(endpoint)
        self.assertEqual(response.status_code, 200)

        body = json.loads(response.data)
        self.assertEqual(len(body['data']), 3)
