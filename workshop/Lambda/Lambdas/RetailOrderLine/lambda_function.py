import json
import uuid
import os

import builtins
from opentelemetry import trace

def print(*args, **kwargs):
      # grab the current span , then grab the span contect for related content
    current_span = trace.get_current_span()
    ctx = current_span.get_span_context()
    #o11yEnv = os.environ['OTEL_RESOURCE_ATTRIBUTES'].partition ('deployment.environment=')[2]
    otelSpanID = format(ctx.span_id, "016x")
    otelTraceID = format(ctx.trace_id, "032x")
    logline = {'trace_id'     :  otelTraceID,
                'span_id'     :  otelSpanID,
                'service.name' : os.environ['OTEL_SERVICE_NAME'],
                'deployment.environment' : 'Otel-Lambda'
            }
    arguments = list(args)        
    arguments.insert(0,json.dumps(logline) + " ") 
    return builtins.print(arguments)

def lambda_handler(event, context):
    print ("event: " , event)
    #1 Read the input parameters
    productName = event.get('ProductName')
    quantity    = event.get('Quantity')
    unitPrice   = event.get('UnitPrice')

    #2 Generate the Order Transaction ID
    transactionId   = str(uuid.uuid1())
    print ("transactionId: "+ transactionId) 
    #3 Implement Business Logic
    if all([quantity, unitPrice]):    
        amount = quantity * unitPrice
    else:
        amount = 0
    print ("Amount: " + str(amount)) 
    
    #4 Format and return the result
    return {
        'TransactionID' :   transactionId,
        'ProductName'   :   productName,
        'Amount'        :   amount
        
        }