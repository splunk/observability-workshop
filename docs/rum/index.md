# Splunk RUM, an introduction

Splunk RUM is the industry’s only end to end, full fidelity Real User Monitoring solution, built to optimize performance and troubleshoot faster,giving you full visibility into end-user experiences.</br></br>What this means is that you can view the latency for all interactions from your app running in clients web browsers, through your database calls and everything in between. Identify performance problems in your page loads, and measure how slow backend service performance impacts your customer experience.
</br></br>
We support benchmarking and improving page performance with core web vitals, W3C timings,the ability to identifying long running tasks, and everything that impacts your page load </br></br>
And for data, we don’t sample, we’re framework agnostic, we’re OpenTelemetry standardized, and we capture full user sessions.</br>
All of this means you can measure all user interactions and dynamic components of your modern applications.
</br></br>
Similar to Splunk APM, the frontend and back end application performance are interdependent.</br>To see the full picture, Splunk RUM provides seamless correlation between your front end and the back end microservices.</br> If your web based application acts out because of an issue related to the microservices, or the infra structure they are running on, Splunk will let you know.</br></br> To complete the picture, in-context access to Splunk logs and events enable deeper troubleshooting and root-cause analysis.
</br>
</br>
![Architecture Overview](../images/rum/rum-architecture.png)

## Overview of the Rum Workshop

In this RUM workshop you are  going to see what is needed to add RUM to your website.</br>
and then examine performance of your website with  RUM metrics, followed by investigating issues with your website.</br?>

To show you the difference between a RUM and a Non RUM Website we are using a separate RUM Host</br>
An other reason for using a separate RUM Website is that we can increase the amount of traffic to this website,</br> 
making the data we  will be looking at, more realistic.</br>

The Workshop Host will provide you the URL for the RUM Host and the URL of the Non RUM Host if this is standalone session</br>
If you are running this session as part of an IMT/APM/RUM Workshop, you will use your current ec2 instance as the NON-RUM website during the workshop. 
