# Enable APM for On-prem Spring boot App


## 1. Validate APM Environment
The first activity we are going to do is validate that we have access to  the Splunk APM environment  and  establish our starting point.
To do this please login to Splunk Infrastructure & APM and select APM. 
![APM-MENU](../../images/lambda/springboot-apm/IsAPMAvailable.png){: .zoom}
This will bring you to the APM monitoring page, here you may see zeroe or a large number of services, depending how many services you are actually monitoring with Splunk APM.



Once the Lambda service have been selected you should see a list of available Lambda Functions.  To find the ones that are assigned to you, use the filter 