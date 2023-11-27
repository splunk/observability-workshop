---
title: 8. Correlate between Splunk RUM and APM backend services
linkTitle: 8. APM & RUM Correlation
weight: 8
---
* Continue with the RUM Session information in the RUM UI
* See correlated APM traces and logs in the APM & Log Observer UI

---

## 1. Finding backend service issues

Click on the ![RUM-JS](../images/RUM-JS-Error.png?classes=inline&height=25px) to close the Span view.
Now continue to scroll down and find the **POST /cart/checkout** line.

![RUM-APM-Click](../images/RUM-APM-Click.png)

Click on the blue ![RUM-APM-BLUE](../images/RUM-APM.png?classes=inline&height=25px) link, this should pop up a dialog showing information on the backend services that were part of the checkout action taken by the end user.

![RUM-APM-Trace](../images/RUM-Trace.png)

In this popup, there are multiple sections available, providing you with a quick insight in the behavior of your backend services. For example the Performance Summary section will tell you where the time was spent during the backend call.

![RUM-APM-Trace-perf](../images/RUM-Trace-Performance.png)

In the above example you can see that more than 77,9% was spent in external services.

If you scroll down to the bottom of the dialog, you can see the complete Trace and Services section like shown below:

![RUM-APM-Trace-services](../images/RUM-Trace-Services.png)

in the Services map, you can see two services flagged red, the **Checkout** Service and the **Payment** Service in both in dark red. Light red means it received an error and dark red means an error originated from that service.

![RUM-APM-Trace-services-detail](../images/RUM-Trace-Services-Detail.png)
So already it is obvious there is a problem in the back end services.

Let's investigate!

## 2.  Follow the Trace to the Backend service

You can now click on the Trace Id link:

![RUM-APM-Trace-link](../images/RUM-Trace-url.png)

This will bring you to the Waterfall APM view that will show you what occurred in detail in a call to the backend services.
On the right you see the Trace Id: and again the Performance Summary, as we saw before.
In the waterfall, you can identify the various backend services that were part of this call from the frontend.

As you can see there are red error indicators ![RUM-APM-error-flag](../images/APM_Error_Flag.png?classes=inline&height=25px) before the **Checkout** Service and the **Payment** Service.

![RUM-APM-waterfall](../images/RUM-APM-Waterfall.png)

Click on the ![RUM-APM-error-flag](../images/APM_Error_Flag.png?classes=inline&height=25px) after the **paymentservice: grpc.hipstershop.PaymentService/Charge** line.

![RUM-payment-click](../images/payment-click.png)

This will open the span detail page to show you the detailed information about this service call.
You wil see that the call returned a **401** error code or *Invalid Request*.

## 3.  Use the Related Content - Logs

As the Splunk Observability cloud suite correlates trace metrics and logs automatically, the system will show you in the related content bar at the bottom of the page, the corresponding logs for this trace.

![RUM-payment-related-content](../images/log-corelation.png)

Click on the Log link to see the logs.

When the logs are shown, notice that the filter at the top of the page contains the logs for the trace.
Next select one of the  lines indicating an error for the payment service.
This should open the log message on the right.

It clearly shows the reason why the payment service fails: we are using an invalid token towards the service:  
***Failed payment processing through ButtercupPayments: Invalid API Token (test-20e26e90-356b-432e-a2c6-956fc03f5609)**

![RUM-logs](../images/RUM-LogObserver.png)

## 4.  Conclusion

In the workshop, you have seen how to add RUM functionality to you website.
We investigate the performance of your Website using RUM Metrics.
Using the Tag profile, you have searched for your own session, and with the session waterfall, you identified two problems:

* A Java script error that caused your price calculation to be zero.
* An issue in the payment backend service that caused payments to fail.

Using the ability to correlate RUM traces with the Backend APM trace and Logs, you have found the reason for the payment failure.

This concludes the RUM workshop.
