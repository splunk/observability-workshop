---
title: Splunk RUM, an introduction
linkTitle:  Splunk RUM
weight: 1
cascade:
  - _target:
    type: docs
---
Splunk RUM is the industry’s only end to end, full fidelity Real User Monitoring solution. It is built to optimize performance and aid in faster troubleshooting, giving you full visibility into end-user experiences.

Splunk RUM allows you to identify performance problems in your web applications that impact the customer experience. We support benchmarking and measuring page performance with core web vitals. This includes but not limited to: W3C timings, the ability to identify long running tasks, along with everything that can impact your page load.

With Splunk’s end to end monitoring capabilities you are able to view the latency between all of the services that make up your application, from the service itself through to infrastructure metrics such as database calls and everything in between.

Our full fidelity end to end monitoring solution captures 100% of your span data. We do not sample, we are framework agnostic and Open Telemetry standardized.

More often than not we find that the frontend and backend application's performance are interdependent. Fully understanding and being able to visualize the link between your backend services and your user experience is increasingly important.
To see the full picture, Splunk RUM provides seamless correlation between our front end and back end microservices. If your users are experiencing less than optimal conditions on your web based application due to an issue related to your microservice or infrastructure, Splunk will be able to detect this issue and alert you.

To complete the picture and offer full visibility, Splunk is also able to show in-context logs and events to enable deeper troubleshooting and root-cause analysis.

![Architecture Overview](/images/rum/rum-architecture.png)

---

## Overview of the RUM Workshop

The aim of this Splunk Real User Monitoring (RUM) workshop is to:

* See how to add RUM to your website.

* Examine the performance of your website with RUM metrics.

* Investigate issues with your website.

 In order to reach this goal, we will use an online boutique to order various products. Whilst shopping on the online boutique you may encounter some issues with this web site, and you will use Splunk RUM to identify the issues, so they can be resolved by the developers.

The workshop host will provide you with the URL for an online boutique store that has RUM enabled. This will allow us to generate live data to be analysed later.

If you are running this session as part of the IMT/APM workshop you will be able to compare your current online boutique store which is not RUM enabled to the RUM enabled URL that your workshop host will provide.  If this an standalone RUM workshop, you will be provided with two URL, one for a shop that no RUM, and one that is RUM enabled.
