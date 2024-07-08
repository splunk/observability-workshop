import logging
import random
import time
import requests
from flask import Flask, request
from waitress import serve

app = Flask(__name__)

# Last number =
# 0-5 = Normal
# 6, 7, 8 = Feature Flags
# 9 = HipsterCard txns
# Issues/Processes:
# - Errors on credit scores not between 300-850
# - Delays on transactions where credit score is 300-580 (poor)


@app.route("/test")
def test_it():
    return "OK"


@app.route("/getScore")
def get_credit_score():
    customernum = request.args.get("customernum")

    score = random.randrange(250, 850, 1)

    if score >= 300 and score < 580:
        addDelays()

    return str(score)


def addDelays():
    length = random.randrange(2, 4)
    time.sleep(length)


@app.route("/runCreditCheck")
def run_credit_check():
    customernum = request.args.get("customernum")
    creditscore = request.args.get("score")

    iLastDigit = int(str(customernum)[-1])
    iScore = int(creditscore)

    if iLastDigit == 7 and iScore >= 800:
        time.sleep(5)

    if iScore < 300:
        requests.get("http://otherservice:777/extra?customernum=" + customernum)

    return "OK"


if __name__ == "__main__":
    serve(app, port=8899)
