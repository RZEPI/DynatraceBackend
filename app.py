import requests
from flask import Flask, request, render_template
from flask_cors import CORS
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

def parse_curr_code(curr_code):
    try:
        curr_code = curr_code.lower()
        if len(curr_code) != 3 or curr_code.isnumeric():
            return None
        return curr_code
    except AttributeError:
        return None


def parse_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime("%Y-%m-%d")
        return date
    except ValueError:
        return None


def parse_quot_num(number):
    try:
        number = int(number)
        if number > 255 or number < 1:
            return None
        return number
    except ValueError:
        return None


def parse_response(response):
    if (response.status_code == 200):
        return True
    else:
        return False


def make_url(expressions, table="a", last_data=False):
    url = f"http://api.nbp.pl/api/exchangerates/rates/{table}/{expressions[0]}/"
    if last_data:
        url += 'last/'
    url += f"{expressions[1]}"
    return url


def avg_exch_result(response_data):
    return response_data['rates'][0]['mid']


def min_max_val_result(response_data):
    rates = response_data['rates']
    max_val = float('-inf')
    min_val = float('inf')
    for rate in rates:
        rate_val = rate['mid']
        if rate_val < min_val:
            min_val = rate_val
        if rate_val > max_val:
            max_val = rate_val
    min_val = "{:.4f}".format(min_val)
    max_val = "{:.4f}".format(max_val)
    return (min_val, max_val)


def major_diff_result(response_data):
    rates = response_data['rates']
    max_diff = -1
    for rate in rates:
        diff = rate['ask'] - rate['bid']
        if diff > max_diff:
            max_diff = diff
    max_diff = "{:.4f}".format(max_diff)
    return max_diff


def check_final_result(response, result_func):
    if parse_response(response):
        response_data = json.loads(response.text)
        result = result_func(response_data)

        return json.dumps({'result': result})
    else:
        return json.dumps({'result': f"Error {response.status_code} occured"})


def get_curr_code():
    curr_code = request.args.get('currency')
    curr_code = parse_curr_code(curr_code)
    return curr_code


def get_date():
    date = request.args.get('date')
    date = parse_date(date)
    return date


def get_quot_num():
    quot_num = request.args.get('quot_num')
    quot_num = parse_quot_num(quot_num)


def get_response(curr_code, quot_number, result_func, table="a"):
    curr_code = parse_curr_code(curr_code)
    quot_num = parse_quot_num(quot_number)

    if curr_code == None:
        return json.dumps({'result': "Invalid currency code format"})
    if quot_num == None:
        return json.dumps({'result': "Invalid number of quotations format"})

    url = make_url((curr_code, quot_num), table, last_data=True)
    response = requests.get(url)

    return check_final_result(response, result_func)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/exchanges/<string:curr_code>/<string:date>', methods=['GET'])
def avg_exch(curr_code, date):
    curr_code = parse_curr_code(curr_code)
    date = parse_date(date)

    if curr_code == None:
        return json.dumps({'result': "Invalid currency code format"})
    if date == None:
        return json.dumps({'result': "Invalid date format"})

    url = make_url((curr_code, date))
    response = requests.get(url)

    return check_final_result(response, avg_exch_result)


@app.route('/minmaxval/<string:curr_code>/<string:quot_number>', methods=['GET'])
def min_max_val(curr_code, quot_number):
    return get_response(curr_code, quot_number, min_max_val_result, "a")


@app.route('/majordiff/<string:curr_code>/<string:quot_number>', methods=['GET'])
def major_diff(curr_code, quot_number):
    return get_response(curr_code, quot_number, major_diff_result, "c")


if __name__ == '__main__':
    app.run(port=8888)

