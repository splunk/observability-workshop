import requests
from flask import Flask, request
from waitress import serve
from opentelemetry import trace  # <--- ADDED BY WORKSHOP

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/test')
def test_it():
    return 'OK'

@app.route('/check')
def credit_check():
    current_span = trace.get_current_span()  # <--- ADDED BY WORKSHOP
    customerNum = request.args.get('customernum')
    current_span.set_attribute("customer.num", customerNum)  # <--- ADDED BY WORKSHOP

    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore?customernum=" + customerNum)
    creditScoreReq.raise_for_status()
    creditScore = int(creditScoreReq.text)
    current_span.set_attribute("credit.score", creditScore)  # <--- ADDED BY WORKSHOP

    creditScoreCategory = getCreditCategoryFromScore(creditScore)
    current_span.set_attribute("credit.score.category", creditScoreCategory)  # <--- ADDED BY WORKSHOP

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck?customernum=" + str(customerNum) + "&score=" + str(creditScore))
    creditCheckReq.raise_for_status()
    checkResult = str(creditCheckReq.text)
    current_span.set_attribute("credit.check.result", checkResult)  # <--- ADDED BY WORKSHOP

    return checkResult

def getCreditCategoryFromScore(score):
    creditScoreCategory = ''
    match score:
        case num if num > 850:
            creditScoreCategory = 'impossible'
        case num if 800 <= num <= 850 :
            creditScoreCategory = 'exceptional'
        case num if 740 <= num < 800 :
            creditScoreCategory = 'very good'
        case num if 670 <= num < 740 :
            creditScoreCategory = 'good'
        case num if 580 <= num < 670 :
            creditScoreCategory = 'fair'
        case num if 300 <= num < 580 :
            creditScoreCategory = 'poor'
        case _:
            creditScoreCategory = 'impossible'
    return creditScoreCategory

if __name__ == '__main__':
    serve(app, port=8888)