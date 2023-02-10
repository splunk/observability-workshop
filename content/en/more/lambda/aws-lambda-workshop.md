# AWS Lambda --> Splunk APM Workshop
In this workshop, you will create a microservices app (written in Python) out of AWS Lambda functions, using the CloudFormation template provided. You will then instrument the functions to get visibility through Splunk APM. **No coding experience necessary!**

## Table of Contents
- [Requirements](#requirements)
- [Steps](#steps)
  - [Create the microservices environment](#create-the-microservices-environment)
  - [Instrument the Lambda functions](#instrument-the-lambda-functions)
  - [Run the app to generate APM data](#run-the-app-to-generate-apm-data)
  - [[Optional] Add custom span tags for additional info](#optional-add-custom-span-tags-for-additional-info)
- [Conclusion](#conclusion)
- [Troubleshooting](#troubleshooting)

## Requirements
- Access to a Splunk Observability Cloud organization with APM enabled
- Permissions to view APM access tokens in Splunk Observability Cloud
- AWS account
- Permissions to create Lambda functions and S3 buckets in the 'us-east-1' (N. Virginia) region on AWS

## Steps
### Create the microservices environment
1. Download [this CloudFormation template](https://github.com/smathur-splunk/lambda-apm-workshop/blob/main/AlpacaTraderWorkshopIncomplete.template). This template contains all the objects (and code) that are needed for the microservices app that you will instrument.
2. Navigate to [CloudFormation in the AWS console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1). **Make sure you are in the 'us-east-1' (N. Virginia) region!!! The CloudFormation template is written for that region ONLY.**
3. At the top-right, click `Create stack` > `With new resources (standard)`.
4. On the 'Create stack' page, select `Upload a template file`, and then `Choose file` to select the CloudFormation template you downloaded in Step 1. Click `Next`. <img src="images/step04.png"/>
5. To complete the CloudFormation stack creation, give the stack a name (e.g. `lambda-stack`), and under 'Parameters', enter a name for the S3 bucket to be used by the microservices app. Click `Next`. Note that this name **must be unique across all of AWS**.
6. On the next page titled 'Configure stack options', scroll all the way down and click `Next`. Finally, on the 'Review' page, scroll to the bottom, and select the checkbox that says 'I acknowledge that AWS CloudFormation might create IAM resources with custom names.' Then click `Create stack`.
7. You should now see that your stack has a status of 'CREATE_IN_PROGRESS'. Wait until it says 'CREATE_COMPLETE' (or spam the refresh button, your choice). You now have a microservices app running on AWS Lambda!

### Instrument the Lambda functions
8. Navigate to [AWS Lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions) and take a moment to understand the functions in this app. There are 4 of them: 'watchlistUpdater', 'stockRanker', 'getFinancials', and 'buyStocks'. The architecture of these functions will become clear once you instrument them for APM.
9. Navigate to the Splunk O11y 'Data Setup' page, and search for `lambda` (you may have to click `Extend search across all integrations`). Select `AWS Lambda (Serverless instrumentation)`, and click `Add Integration`.
10. For 'Function name', enter the name of the first Lambda function you will instrument (e.g. `watchlistUpdater`). Select your Splunk access token (make sure it has the right permissions for APM), and enter a name for this app's environment (e.g. `lambda-app`). Click 'Next'. **Make sure the environment name is the same for all your functions in this app.**
11. On the 'Install Integration' page, select `Python`. Follow the steps on this page to add the Splunk OTel layer and set the environment variables. For the ARN, use `arn:aws:lambda:us-east-1:254067382080:layer:splunk-apm:51`. <img src="images/step11-1.png"/> <img src="images/step11-2.png"/> <img src="images/step11-3.png"/> <img src="images/step11-4.png" height="350"/> <img src="images/step11-5.png"/> <img src="images/step11-6.png" height="600"/>
12. Phew! That was a lot. Now repeat Step 11 for all 4 Lambda functions. (You do not need to go through the Splunk O11y GDI wizard again; simply make the changes necessary in AWS.)

### Run the app to generate APM data
13. Time to finally run the code and see some data! Manually run these 3 functions in order: 'watchlistUpdater', 'stockRanker', and 'buyStocks'. To run them, open up each function, and under the 'Function overview' section, click on the `Test` tab. Enter an event name (e.g. `test`), and at the top right, click the orange `Test` button. <img src="images/step13.png" height="350"/>
14. If 'watchlistUpdater' and 'stockRanker' run as expected, you should see 'Execution result: succeeded'.
15. When running the 'buyStocks' function, you will get an error--**this is expected!** If you go into the service map in Splunk APM, you will now see that all 4 of our functions are there, as well as the S3 bucket that some of them are talking to. There will be a red circle for 'buyStocks', indicating that an error occurred! This is especially useful if Lambda functions are scheduled to run automatically, in which case errors won't be immediately apparent without APM. <img src="images/step18.png"/>
16. In the APM service map, click on `buyStocks` and select `Traces` on the right. Find the trace with the error we just saw, and see if you can find the issue. If not, go to the next step.
17. Go back to the AWS Lambda page for 'buyStocks' and in 'index.py', uncomment line 13. Click `Deploy` to save your changes.
```python
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    alpaca_id = "PK6MU6XGW0KY0SSI402E"
    alpaca_secret = "ZBvSlwEB8mk1DnbFZHCm18mkmeYdxVLu5nw6c8cR"
    headers = {'APCA-API-KEY-ID':alpaca_id, 'APCA-API-SECRET-KEY':alpaca_secret}
  
    rankings_file = s3.get_object(Bucket=os.environ['BUCKET_NAME'], Key='rankings.txt')
    #stock_ranking = rankings_file['Body'].read().decode('utf-8').split(' ')
    # ^^^ UNCOMMENT THE LINE ABOVE
```
18. Go to the `Test` tab and run this function again. You should now see 'Execution result: succeeded', and another trace should pop up in Splunk APM as well (this time without any errors).

### [Optional] Add custom span tags for additional info
19. Custom span tags are already added for 3 of the functions. Let's take a look at how to add custom span tags in the 4th one, 'getFinancials'. Open up the 'getFinancials' Lambda function.
20. Under line 2, add a new line and write `from opentelemetry import trace`.  Under line 6, add **with proper indentation** 
```python
customizedSpan = trace.get_current_span()
customizedSpan.set_attribute("symbol", ticker);
customizedSpan.set_attribute("finnhub.token", "brqivm7rh5rc4v2pmq8g");
```
The final result should look like this:
```python
import json
import requests
from opentelemetry import trace

def lambda_handler(event, context):
    ticker = event['symbol']
    
    customizedSpan = trace.get_current_span()
    customizedSpan.set_attribute("symbol", ticker);
    customizedSpan.set_attribute("finnhub.token", "brqivm7rh5rc4v2pmq8g");
```
Source: [Instrument your application code to add tags to spans](https://docs.splunk.com/Observability/apm/span-tags/add-context-trace-span.html#instrument-your-application-code-to-add-tags-to-spans)

21. Click `Deploy` to save your changes. Now if you run 'stockRanker' and look at the traces for 'getFinancials' in Splunk APM, you'll see that each span has tags for the stock symbol being analyzed and the API token being used. This can help with troubleshooting, in case of any errors. <img src="images/step21.png"/>

## Conclusion
At this point, you've created a microservices app in AWS using a CloudFormation template, and instrumented it for Splunk APM. As you probably noticed, the process of instrumenting Lambda functions for APM is simple, but tedious. This is where CloudFormation can help. For this workshop, the process of creating the app was automated, but the instrumentation can be automated too.

To see what the final result *should* look like if you did everything correctly (and how the instrumentation process can be automated), create a stack with [this CloudFormation template](https://github.com/smathur-splunk/lambda-apm-workshop/blob/main/AlpacaTraderWorkshop.template) and run the 3 functions in the same order: 'watchlistUpdater', 'stockRanker', and 'buyStocks'.


## Troubleshooting
### CloudFormation stack creation failed. Check the S3 bucket name.
S3 bucket names must be unique across the entirety of AWS, so make sure that when you create your CloudFormation stack, you enter a unique name in the 'bucketName' parameters field.

### Data is not being sent into Splunk Observability. Check your Splunk access token.
Ensure that the Splunk access token you have used has the right permissions for APM data.

### Lambda functions won't run. Check for indentation issues.
Don't forget to indent your code the proper amount when adding custom span tags, or the Python code won't be able to run.

### In the APM service map, services aren't connected to each other. Check the environment name.
Make sure the environment name (`OTEL_RESOURCE_ATTRIBUTES` environment variable in Lambda configuration) is the same for all your functions in this app.
