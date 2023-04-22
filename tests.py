import unittest
import app


class TestAvgExch(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_valid_input(self):
        response = self.app.get('/exchanges/gbp/2023-01-02')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'], 5.2768)

    def test_invalid_curr_code(self):
        response = self.app.get('/exchanges/21/2023-01-02')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid currency code format")

    def test_invalid_date(self):
        response = self.app.get('/exchanges/GBP/sdasa')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'], "Invalid date format")


class TestMinMaxVal(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_invalid_curr_code(self):
        response = self.app.get('/minmaxval/21/2')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid currency code format")

    def test_invalid_quot_num_zero(self):
        response = self.app.get('/minmaxval/eur/0')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid number of quotations format")

    def test_invalid_quot_num_too_high(self):
        response = self.app.get('/minmaxval/eur/300')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid number of quotations format")

    def test_invalid_quot_num_nan(self):
        response = self.app.get('/minmaxval/eur/hi')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid number of quotations format")


class TestMajorDiff(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_invalid_curr_code(self):
        response = self.app.get('/majordiff/21/2')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid currency code format")

    def test_invalid_quot_num_zero(self):
        response = self.app.get('/majordiff/eur/0')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid number of quotations format")

    def test_invalid_quot_num_too_high(self):
        response = self.app.get('/majordiff/eur/300')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid number of quotations format")

    def test_invalid_quot_num_nan(self):
        response = self.app.get('/majordiff/eur/hi')
        response_data = app.json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['result'],
                         "Invalid number of quotations format")
