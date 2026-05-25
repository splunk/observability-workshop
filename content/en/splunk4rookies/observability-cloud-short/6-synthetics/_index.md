---
title: Digital Experience (Synthetics)
linkTitle: 6. Digital Experience (Synthetics)
archetype: chapter
weight: 6
time: 15 minutes
description: In this section, you will learn how to use Splunk Synthetics to monitor the performance and availability of your applications.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Putting your **SRE** hat back on, you have been asked to set up monitoring for the Online Boutique. You need to ensure that the application is available and performing well 24 hours a day, 7 days a week.

> [!IMPORTANT]Wouldn’t it be great if we could have 24/7 monitoring of our application, and be alerted when there is a problem? This is where Synthetics comes in. We will show you a simple test that runs every 1 minute and checks the performance and availability of a typical user journey through the Online Boutique.

{{% /notice %}}

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="BG" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
Hey, Bill, now that we've resolved the `paymentservice` issue, I think we should set up some monitoring to ensure we catch any future issues before they impact our customers.
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
I suggest we use Synthetics to set up a test that runs every minute and checks the performance and availability of a typical user journey through the Online Boutique. This way, we can be alerted immediately if there are any issues.
{{< /webex-msg >}}
{{< /webex >}}
