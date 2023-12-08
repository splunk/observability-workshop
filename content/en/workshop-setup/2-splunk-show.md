---
title: 2. Using Splunk Show
weight: 2
---

## Provision the EC2 Instances Using Splunk Show

![Splunk Show](../images/splunk-show.png)

Please visit [**Splunk Show**](https://show.splunk.com/template/262/?type=workshop) to provision your workshop instance(s).

Select the desired **Content Type** as follows:

- _Default (for interactive workshop)_ - select this if your audience is technical and wants hands-on experience installing OpenTelemetry and deploying applications.
  - Select either Normal Workshop, Private Event or Public Event. Change **Estimated Participants** to the number of attendees you expect and set the same value in **O11y Shop Quantity**. This will provision the correct number of EC2 instances. It is recommended that you over-provision by 10% - 20% to allow for any last-minute attendees.
- _Pre-configured Instances_ - select this if you need the OpenTelemetry Collector and the application pre-deployed for a less technical audience. Attendees will only require a browser to complete the workshop.
  - Select Normal Workshop only! Ensure that **Estimated Participants** is set to **1** and **O11y Shop Quantity** is set to **1** also as only a single instance is required by the workshop instructor.

{{% notice info %}}

- Ensure you set **Operating hours** to **Run always (24/7)** as this will prevent the instance from being suspended and obtaining a new IP address which breaks RUM and Synthetics.
- Ensure you set a **DNS name** for the instance(s) as this makes it easier to find environments in Splunk Observability Cloud.

{{% /notice %}}

Select your Splunk Observability Cloud Realm and enter the INGEST, API, RUM tokens and the HEC URL and HEC Token that **SWiPE** generated for you.

For further guidance on using Splunk Show please see the [**Splunk Show User Guide**](http://go/show/user-guide).
