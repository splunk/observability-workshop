# Enable APM in the RetailOrder Function

## 1. Edit UID_RetailOrder Lambda in your AWS environment

To add APM to our lambda function, you need to got to the browser tab with your lambda functions selected in  the first exercise, or follow the original [Validate Lambda Functions](../initial_run_env/#1-validate-availability-of-lambda-functions) instructions. Once filtered with your **UID** you should have something like this:

![AWS-Lambda-filtered](../images/lambda/retailorder/functions-lambda-selected.png)

Now select the Lambda Function **UID**_RetailOrder to open the browser based editor environment for Lambda functions.

![AWS-Lambda-editor-1](../images/lambda/retailorder/retailorderedit-1.png)

Now scroll down so you have the full editor visible.

![AWS-Lambda-editor-2](../images/lambda/retailorder/retailorderedit-2.png)

To enable APM, we need to import the Splunk SignalFx Lambda wrapper. We already included this for you, but you can find the details on how to set this up yourself [here](https://github.com/signalfx/lambda-python){: target=_blank}

Secondly we also import the opentracing library, we will use this later to customize the span information we send to Splunk's APM.

Add the follow two lines at the top of the file and add an empty line.

=== "RetailOrder Updates"

    ```text
    import signalfx_lambda
    import opentracing

    ```

Add the following two lines above the line stating ***def lambda_handler(event,context):*** This will enable the wrapper.

=== "RetailOrder Updates"

    ```text
    @signalfx_lambda.emits_metrics()
    @signalfx_lambda.is_traced()
    ```

Verify that the top of the file now looks like this:

=== "RetailOrder Updates"

    ```text
    import signalfx_lambda
    import opentracing

    import os
    import json
    import boto3
    import requests

    # The Environment Tag is used by Splunk APM to filter Environments in UI
    APM_ENVIRONMENT = os.environ['SIGNALFX_APM_ENVIRONMENT']
    PRICE_URL       = os.environ['PRICE_URL']
    ORDER_LINE      = os.environ['ORDER_LINE']

    # Define the client to interact with AWS Lambda
    client = boto3.client('lambda')

    @signalfx_lambda.emits_metrics()
    @signalfx_lambda.is_traced()
    def lambda_handler(event,context):
        print("event received :", event)
    ```
To save your work, you must press on the **Deploy**{: .label-button .label-button.AWS-orange} button above the editor as show here.

![AWS-Lambda-deploy](../images/lambda/retailorder/lambdadeploy.png)

---

## 3. Run a case and find both the Service Dashboard for your lambda function & your trace

Go back to the browser tab with your Phone App running that you opened earlier, if you have closed it you can open a new one by navigating to *http://**[ec2_ip]**:8080/order* (where **[ec2_ip]** is the public ip address of your EC2 instance)

![ec2-shop1](../images/lambda/initial_run/Shop.png)

Generate your first trace in your environment by typing a phone name, selecting a number greater then 0 and  choosing a customer type:

- Name of a phone: For example *Geoff's big pictures phone*
- Quantity:  *2*
- Select a customer type: *Silver*

Click submit to run the application with the newly enabled FrameWork and Tracing settings, which will result in the generation of your first APM Trace.

The result should be similar to this:

![ec2-shop2](../images/lambda/initial_run/Shop-result.png)

### 3.1 Find your Service Dashboard for the RetailOrder Lambda Function in Splunk APM

Right now your trace is being processed by the splunk APM back end, and since this is the first time this service is seen by Splunk APM, the corresponding service dashboard for the Lambda Function will be generated.

Return to the APM Tab you opened in Step 1 of this section which should be displaying the Splunk APM Monitoring Dashboard.

Hover over **Dashboards** in the top menu, and then click on **All Dashboards**. A number of pre-built dashboards are provided for you in your default view.

![apm-dashboard](../images/lambda/springboot-apm/gotoAPMServices.png)

Here you should have a Dashboard Group called **APM Services** (If it is not present, wait for a minute or two and refresh the screen, If it has not appeared after a couple of minutes, reach out the the workshop leader)

Select the **Services** Dashboard.

![apm-dashboard-1](../images/lambda/springboot-apm/Dashboard-Service 1.png)

From the Environment Drop down box select ***UID_*Retail_Demo**, from the Service drop down box select ***uid*-mobile-web-shop-base** (where [UID] is your unique UID allocated to you for this Workshop.  The following examples have a UID of ACME).

![apm-dashboard-2](../images/lambda/springboot-apm/Dashboard-Service 2.png)

This wil give you the automatically generated service dashboard for ***uid*-mobile-web-shop-base**.

If you set the time to -5 minutes you can see the single invocation, the averages over time on the left side will become active after a few minutes.

![apm-dashboard-3](../images/lambda/springboot-apm/Dashboard-Service 3.png)

## 3.1 Look at trace info in splunk APM

Now navigate back to the APM Tab:

![APM-MENU](../images/lambda/springboot-apm/IsAPMAvailable.png)

At the APM monitoring page, you should now have a single circle in the centre of the dashboard, this represents the UID_Retail_Demo Service.  Over the next modules you will enable APM on additional services which will then also appear in this view.

If you see more services please filter it down by selecting your environment ***UID_*Retail_Demo** from the drop down list.

![APM-First_service](../images/lambda/springboot-apm/our_first_service.png)
You can also see the two endpoints used by the service.

Now click on **Troubleshooting** to go to the Troubleshooting view.

You should see your single service with on the right, two dashboards with a spike indicating the single invocation.

Select the top of the spike of the top dashboard as shown.
![APM-troubleshoot](../images/lambda/springboot-apm/Troubleshootingourfirsttrace.png)

This will expand and show a list of traces matching the time frame selected. (In our case it should be our single trace.)

Click on the blue **Trace-id** to see the waterfall view of the trace. (Clicking on the Span name ***uid*-mobile-web-shop-base**  will expand it as shown.)

![APM-waterfall](../images/lambda/springboot-apm/waterfallview.png)

In the expanded view you can see the default tags send by the application.
