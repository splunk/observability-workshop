# Splunk RUM, an introduction

Splunk RUM is the industry’s only end to end, full fidelity Real User Monitoring solution. It is built to optimize performance and aid in faster troubleshooting, giving you full visibility into end-user experiences.

Splunk RUM allows you to identify performance problems in your web applications that impact the customer experience. We support benchmarking and measuring page performance with core web vitals. This includes but not limited to: W3C timings, the ability to identify long running tasks, along with everything that can impact your page load. 

With Splunk’s end to end monitoring capabilities you are able to view the latency between all of the services that make up your application, through to infrastructure metrics such as database calls and everything in between. 

Our full fidelity end to end monitoring solution is made up of 100% of your span data. We do not sample, we are framework agnostic and Open Telemetry standardized. 

More often than not we find that the frontend and backend applications performance are interdependent. So understanding and being able to visualize the link between your backend services and your user experience is increasingly important.
To see the full picture, Splunk RUM provides seamless correlation between our front end and back end microservices. If your users are experiencing a bad user experience on your web based application due to an issue related to your microservice or infrastructure, Splunk will be able to detect this issue and alert you. 

To complete the picture and offer full visibility, Splunk is also able to show in-context logs and events to enable deeper troubleshooting and root-cause analysis.


![Architecture Overview](../images/rum/rum-architecture.png)

## Overview of the Rum Workshop

In this RUM workshop you are  going to see what is needed to add RUM to your website and then examine performance of your website with RUM metrics, followed by investigating issues with your website.

To show you the difference between a RUM and a Non RUM Website we will be using a separate RUM Host. Another reason for using a separate RUM Website is that we can increase the amount of traffic to this website, making the data we will be looking at more realistic.

The Workshop Host will provide you the URL for the RUM Host and the URL of the Non RUM Host if this is standalone session. If you are running this session as part of an IMT/APM/RUM Workshop, you will use your current ec2 instance as the NON-RUM website during the workshop.
