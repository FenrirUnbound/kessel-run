import json
import unittest

from main import app

class StatusTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_server_status(self):
        endpoint = '/api/v1/status'
        response = self.app.get(endpoint)

        self.assertEqual(response.status_code, 200)

        body = json.loads(response.data)

        self.assertDictEqual(body, {
            'status': 'OK'
        })
