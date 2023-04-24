import unittest
import app


class TestParseCurrCode(unittest.TestCase):

    def test_valid_curr_code(self):
        result = app.parse_curr_code('eur')
        self.assertEqual(result, 'eur')

    def test_valid_curr_code_upper(self):
        result = app.parse_curr_code('EUR')
        self.assertEqual(result, 'eur')

    def test_invalid_curr_code_num(self):
        result = app.parse_curr_code('123')
        self.assertEqual(result, None)

    def test_invalid_curr_code_len(self):
        result = app.parse_curr_code('euro')
        self.assertEqual(result, None)


class TestParseDate(unittest.TestCase):

    def test_valid_date(self):
        result = app.parse_date('2023-01-01')
        self.assertEqual(result, '2023-01-01')

    def test_invalid_date(self):
        result = app.parse_date('-1200 12 21')
        self.assertEqual(result, None)

    def test_invalid_date_format(self):
        result = app.parse_date('21-12-2001')
        self.assertEqual(result, None)


class TestParseQuotNum(unittest.TestCase):
    def test_valid_quot_num(self):
        result = app.parse_quot_num(20)
        self.assertEqual(result, 20)

    def test_invalid_quot_num_str(self):
        reslut = app.parse_quot_num("hi")
        self.assertEqual(reslut, None)

    def test_invalid_quot_num_zero(self):
        reslut = app.parse_quot_num(0)
        self.assertEqual(reslut, None)

    def test_invalid_quot_num_minus(self):
        reslut = app.parse_quot_num(-10)
        self.assertEqual(reslut, None)

    def test_invalid_quot_num_too_much(self):
        reslut = app.parse_quot_num(260)
        self.assertEqual(reslut, None)


class TestMakeUrl(unittest.TestCase):
    def test_avg_exch(self):
        result = app.make_url(("ebp", "2023-01-02"))
        self.assertEqual(
            result, "http://api.nbp.pl/api/exchangerates/rates/a/ebp/2023-01-02")

    def test_min_max_val(self):
        result = app.make_url(("ebp", 2), last_data=True)
        self.assertEqual(
            result, "http://api.nbp.pl/api/exchangerates/rates/a/ebp/last/2")

    def test_major_diff(self):
        result = app.make_url(("ebp", 2), table="c", last_data=True)
        self.assertEqual(
            result, "http://api.nbp.pl/api/exchangerates/rates/c/ebp/last/2")


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


class TestMinMaxValResult(unittest.TestCase):
    def test_majordiff_result(self):
        test_list = []
        test_case = {}
        test_case['mid'] = 5.1123132
        test_list.append(test_case.copy())
        test_case['mid'] = 5.2123132
        test_max_val = test_case['mid']
        test_max_val = "{:.4f}".format(test_max_val)
        test_list.append(test_case.copy())
        test_case['mid'] = 5.0323132
        test_min_val = test_case['mid']
        test_min_val = "{:.4f}".format(test_min_val)
        test_list.append(test_case.copy())
        test_data = {'rates': test_list}
        min_max_val = app.min_max_val_result(test_data)
        self.assertEqual(min_max_val, (test_min_val, test_max_val))


class TestMajordiffResult(unittest.TestCase):
    def test_majordiff_result(self):
        test_list = []
        test_case = {}
        test_case['ask'] = 5.1123132
        test_case['bid'] = 4.9212132
        test_max_diff = test_case['ask'] - test_case['bid']
        test_max_diff = "{:.4f}".format(test_max_diff)
        test_list.append(test_case.copy())
        test_case['ask'] = 3.0123132
        test_case['bid'] = 2.9212132
        test_list.append(test_case.copy())
        test_case['ask'] = 2.9323132
        test_case['bid'] = 2.9212132
        test_list.append(test_case.copy())
        test_data = {'rates': test_list}
        max_diff = app.major_diff_result(test_data)
        self.assertEqual(max_diff, test_max_diff)


if __name__ == '__main__':
    unittest.main()
