# Correlate Between Splunk RUM and APM

* Continue with the RUM Session information in the RUM UI
* See correlated APM traces and logs in the APM & Log Observer UI

---
## 1.  Validating the 

Click on the ![RUM-JS](../images/rum/RUM-JS-Error.png) to close the Span view. </br>
Now continue to scroll down and find the **POST /cart/checkout** line.

![RUM-APM-Click](../images/rum//RUM-APM-Click.png)

Click on the blue ![RUM-APM-BLUE](../images/rum/RUM-APM.png) link, this should pop a dialog showing information</br> on the backend services that where part of the checkout action taken by the end user.

![RUM-APM-Trace](../images/rum//RUM-Trace.png)

In this popup, there are multiple sections available, providing you with a quick insight in the behavior of your backend services. For example the Performance Summary section will tell you where the time was spend during the backend call. 

![RUM-APM-Trace-perf](../images/rum/RUM-Trace-Performance.png)

In the above example you can see that more then 44% was spend in external services.

If you scroll down to the bottom of the dialog, so you can see the complete Trace and Services section like shown below:

![RUM-APM-Trace-services](../images/rum/RUM-Trace-Services.png)


