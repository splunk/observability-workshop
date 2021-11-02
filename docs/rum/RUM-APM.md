# Correlate between Splunk RUM and APM backend services

* Continue with the RUM Session information in the RUM UI
* See correlated APM traces and logs in the APM & Log Observer UI

---
## 1. Find the Backend service with an issue.

Click on the ![RUM-JS](../images/rum/RUM-JS-Error.png) to close the Span view. </br>
Now continue to scroll down and find the **POST /cart/checkout** line.

![RUM-APM-Click](../images/rum//RUM-APM-Click.png)

Click on the blue ![RUM-APM-BLUE](../images/rum/RUM-APM.png) link, this should pop a dialog showing information</br> on the backend services that where part of the checkout action taken by the end user.

![RUM-APM-Trace](../images/rum//RUM-Trace.png)

In this popup, there are multiple sections available, providing you with a quick insight in the behavior of your backend services. For example the Performance Summary section will tell you where the time was spend during the backend call. 

![RUM-APM-Trace-perf](../images/rum/RUM-Trace-Performance.png)

In the above example you can see that more then 77,9% was spend in external services.

If you scroll down to the bottom of the dialog, so you can see the complete Trace and Services section like shown below:

![RUM-APM-Trace-services](../images/rum/RUM-Trace-Services.png)

in the Services map, you can see two services flagged red, the **Checkout** Service and the **Payment** Service in both in dark red. light red mean it received an error and dark red means an error originated from that service.

![RUM-APM-Trace-services-detail](../images/rum/RUM-Trace-Services-Detail.png)
So already it is obvious there is a problem in the back end services.</br>

Let's investigate!

---
## 2.  Follow the Trace to the Backend service.
You can now click on the Trace Id link: </br>
![RUM-APM-Trace-link](../images/rum/RUM-Trace-url.png)

This will bring you to Waterfall APM view that will show you what occurred in detail in call to the backend services.</br>
On the right you see the Trace Id: and again the Performance Summary, as we saw before.</br>
in the waterfall, you can identify the various backend services that where part of this call from the frontend.

As you can see there are red error indicators ![RUM-APM-error-flag](../images/rum/APM_Error_Flag.png) </br>
before the **Checkout** Service and the **Payment** Service.

![RUM-APM-waterfall](../images/rum/RUM-APM-Waterfall.png)

Click on the ![RUM-APM-error-flag](../images/rum/APM_Error_Flag.png) after the **paymentservice: grpc.hipstershop.PaymentService/Charge** line.

![RUM-payment-click](../images/rum/payment-click.png)

This will open the span detail page to show you the detail info about this service call.
You wil see that the call returned a **401** error code or *Invalid Request*. 

---
## 3.  Use the Related Content - Logs 
As the Splunk Observability cloud suite correlates traces metrics and logs automatically, teh system will show you in the related content bar at the bottom of the page, the corresponding logs for this trace.

![RUM-payment-related-content](../images/rum/log-corelation.png)

Click on the Log link to see the logs.

When the log s are show, notice that the filter at the top of the page contains the logs for the trace.</br>
Next select one of the  lines indicating an error for the payment service.</br>
This should open the log message on the right.

It clearly shows the reason why the payment service fails: we are using an invalid token towards the service:  </br>
***Failed payment processing through ButtercupPayments: Invalid API Token (test-20e26e90-356b-432e-a2c6-956fc03f5609)**

![RUM-logs](../images/rum/RUM-LogObserver.png)

---
## 4.  Conclusion.

In the workshop, you have seen how to add RUM functionality to you website. </br>
We investigate the performance of your Website using RUM Metrics.</br>
Using the Tag profile, you have searched for your own session, and with the session waterfall, you identified two problems:</br>
* A Java script error that caused you price calculation to be zero.</br>
* An issue in the payment backend service that caused payments to fail.</br>

Using the ability to correlate RUM traces with the Backend APM trace and Logs you have found te reason for the payment failure.

This concludes the RUM workshop.
