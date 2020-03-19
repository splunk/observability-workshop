#!/usr/bin/env python

from flask import Flask, make_response, request
from signalfx_tracing import trace
import opentracing

app = Flask(__name__)

@trace
def convert_response(message):

  # In this example we want to force this trace to be retained

    opentracing.tracer.active_span.set_tag('sampling.priority', 1)
    opentracing.tracer.active_span.set_tag('message', message)
    print (opentracing.tracer.active_span)
    return 'You said: {}'.format(message)


@app.route('/echo', methods=['POST'])
def echo():
    message = request.data.decode('utf-8')
    return make_response(convert_response(message))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
