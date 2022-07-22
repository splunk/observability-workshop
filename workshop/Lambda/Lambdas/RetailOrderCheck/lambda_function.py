import os
import json
import boto3


import builtins
from opentelemetry import trace
from opentelemetry.trace.status import StatusCode

def print(*args, **kwargs):
      # grab the current span , then grab the span context for related content
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

def lambda_handler(event,context):
    print ("event: " , event)
    current_span = trace.get_current_span()
   
    Name = event.get('ProductName')
    Quantity    = event.get('Quantity')
    Price   = event.get('UnitPrice')
    
    #setup assumed role and grab credentials
    sts_client = boto3.client('sts')

    assumed_role_object = sts_client.assume_role(
    RoleArn="arn:aws:iam::527477237977:role/PH-remote-role",
    RoleSessionName="RemoteSession")
    sts_connection = boto3.client('sts')
    
    credentials=assumed_role_object['Credentials']
    
    #stsResults =  sts_client.assumeRole(assumed_role_object )
    print("Results: " + str(credentials))   
    ACCESS_KEY = assumed_role_object ['Credentials']['AccessKeyId']
    SECRET_KEY = assumed_role_object ['Credentials']['SecretAccessKey']
    SESSION_TOKEN = assumed_role_object ['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. Lambda
    client = boto3.client(
        'lambda',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    CHECK_LINE = "arn:aws:lambda:eu-west-1:527477237977:function:PH_REMOTE_TEST_2"
    responseCode = 200
    if CHECK_LINE:  # if order line is set we will try to call it other wise use a dummy
        print("Check_Line_ARN: " ,CHECK_LINE)    
      # Define the input parameters that will be passed on to the line item calculation function
        inputParams = {
             "ProductName" : Name ,
             "Quantity"    : Quantity,
             "UnitPrice"   : Price
        }
        
        # SET DECLINE AS DEFAULT
     
        Approval = "Check Declined"
        print ("InputParams :",inputParams)
        # Invoking Lambda directly
    
        response = client.invoke( 
            FunctionName = CHECK_LINE, # This could be set as a Lambda Environment Variable
            InvocationType = 'RequestResponse',
            Payload = json.dumps(inputParams)
            )
        print ("Check returned: " + str( response))
        
        responseFromCheck= json.load(response['Payload'])
        print ("response: "+ str(responseFromCheck))
        responseCode = responseFromCheck.get('statusCode')
        Approval = responseFromCheck.get('approval')
        print ("aproval: "+ str(Approval))
        if responseCode == 418:
            responseCode=500
            current_span.set_status(StatusCode.ERROR) 
    else:
        Approval = "Check Failed"
        responseCode = 400
        current_span.set_status(StatusCode.ERROR) 
 
    retval={ 'statusCode'   : responseCode,
             'phoneType'    : Name,
             'quantity'     : Quantity,
             'price'        : Price,
             'approval'     : Approval
            }
    print ('Sending: ' +  str(retval))   
    return retval
        