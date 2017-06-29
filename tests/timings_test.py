import json
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

    def test_list_routes(self):
        endpoint = '/api/v1/timings/1'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 204)

        query_results = Timing.query().order(-Timing.create_time).fetch(2)

        self.assertEqual(len(query_results), 1)
        test_data = query_results[0]

        self.assertGreaterEqual(test_data.duration, 1227)
        self.assertEqual(test_data.distance, '13.2 mi')
