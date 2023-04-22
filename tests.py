import unittest
from app import app, json


class TestAvgExch(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_valid_input(self):
        response = self.app.get('/exchanges/gbp/2023-01-02')
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'], 5.2768)

    def test_invalid_curr_code(self):
        response = self.app.get('/exchanges/21/2023-01-02')
        response_data = json.loads(response.text)
        # print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'], "Invalid currency code format")

    def test_invalid_date(self):
        response = self.app.get('/exchanges/GBP/sdasa')
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'], "Invalid date format")
