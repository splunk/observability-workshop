import os
import json
import boto3
from botocore.exceptions import ClientError
import requests

import builtins
from opentelemetry import trace

from opentelemetry.trace.status import StatusCode

def print(*args, **kwargs):
      # grab the current span , then grab the span contect for related content
    current_span = trace.get_current_span()
    ctx = current_span.get_span_context()
    otelSpanID = format(ctx.span_id, "016x")
    otelTraceID = format(ctx.trace_id, "032x")
    logline = {'trace_id'     :  otelTraceID,
                'span_id'     :  otelSpanID,
                'service.name' : os.environ['OTEL_SERVICE_NAME'],
                'deployment.environment' : os.environ['OTEL_ENVIRONMENT']
            }
    arguments = list(args)        
    arguments.append(json.dumps(logline)) 
    return builtins.print(arguments)

#Try and fetch the urls/arns for the other functions to be called 
PRICE_URL       = os.environ.get('PRICE_URL')
ORDER_LINE      = os.environ.get('ORDER_LINE')
ADMIN_CHECK     = os.environ.get('ADMIN_CHECK')

# Define the client to interact with AWS Lambda
client = boto3.client('lambda')

def lambda_handler(event,context):
    current_span = trace.get_current_span()
    print ("event: " , event)
    #Define / read input parameters from the event trigger
    Name         =  json.loads(event ['body']).get("ProductName")  # Value passed in from test case
    Quantity     =  json.loads(event ['body']).get("Quantity")     # Value passed in from test case
    CustomerType =  json.loads(event ['body']).get("CustomerType") # Value passed in from test case
    OrderNumber  =  json.loads(event ['body']).get("orderNumber")
    
    current_span.set_attribute("request.ProductName", Name)
    current_span.set_attribute("request.OrderNumber", OrderNumber)
    current_span.set_attribute("request.CustomerType", CustomerType)
    
    # Call Node-JS lambda via Api Gateway to get the Price
    if PRICE_URL:   # if there is a value we try to call the service otherwise use a dummy value
       print ("Price_url: " , PRICE_URL)
       payload = {'CustomerType': CustomerType}
       r = requests.get(PRICE_URL,  params=payload)

       #Get Price from response   
       Price =  json.loads(r.text).get('Price') # Get Value from the Price calculator  

    else:
        Price = 600. # for testing 
    
    print ("Price: " ,Price)
    if ORDER_LINE:  # if order line is set we will try to call it other wise use a dummy
        print("Order_Line_ARN: " ,ORDER_LINE)    
      # Define the input parameters that will be passed on to the line item calculation function
        inputParams = {
            "ProductName" : Name ,
            "Quantity"    : Quantity,
            "UnitPrice"   : Price
        }
        print ("inputparams :",inputParams)
        # Invoking Lambda directly
     
        response = client.invoke(
            FunctionName = ORDER_LINE, # This could be set as a Lambda Environment Variable
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
        responseFromOrderLine = json.load(response['Payload'])
        print ("Response: ",responseFromOrderLine)
        newPrice = responseFromOrderLine.get('Amount')
        
        transactionID =  responseFromOrderLine.get('TransactionID')
    else:
        newPrice =  Price
        transactionID = "1-800-transaction-id"
        
    print("New Price: " + str(newPrice) + " transactionID: "+ transactionID)   
    
    inputParams = {
        "ProductName"   : Name,
        "Quantity"      : Quantity,
        "UnitPrice"     : newPrice
    }
    Approval = "Admin Check not Available"
    responseCode = 200 
    if ADMIN_CHECK:
        print("Invoking: " + ADMIN_CHECK)
        response = client.invoke(
            FunctionName = ADMIN_CHECK,
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
        )
        responseCode = 200 #assume all is well here (need better handling for other branches)
        responseFromCheck = json.load(response['Payload'])
        print ("Received: "+  str(responseFromCheck))
        #responseCode = json.load(responseFromCheck['statusCode'])
        responseCode = responseFromCheck.get('statusCode')
        print('R: '+ str(responseCode))
        Approval = responseFromCheck.get('approval')
        print('A: '+ str(Approval))
        if responseCode != 200:
            responseCode=500
            current_span.set_status(StatusCode.ERROR) 
        
    # sqs_client = boto3.client('sqs')
    # sqs_queue_url = sqs_client.get_queue_url(QueueName="RetailOrder")['QueueUrl']
    # msg_body = message = {"key": "value"}
    # try:
    #     msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
    #                                   MessageBody=json.dumps(msg_body)) 
    # except ClientError as e:
    #     print("error: ",e) 
    #     return {
    #         'statusCode': 418,
    #         'body': json.dumps(e)
    #         }
    # else:       
    #     print (msg)
    
    current_span.set_attribute("reply.ProductName" , Name )
    current_span.set_attribute("reply.quantity" , Quantity )
    current_span.set_attribute("reply.customerType" , CustomerType )
    current_span.set_attribute("reply.price" , newPrice )
    current_span.set_attribute("reply.transaction" , transactionID )
    current_span.set_attribute("reply.approval" , Approval )
    
    

    retval={'phoneType'     : Name,
            'quantity'      : Quantity,
            'customerType'  : CustomerType,
            'price'         : newPrice,
            'transaction'   : transactionID,
            'approval'      : Approval
            }
    return {
            'statusCode': responseCode,
            'body': json.dumps(retval)
        }