---
title: Splunk Synthetics
linkTitle: 8. Splunk Synthetics*
archetype: chapter
weight: 8
time: 15 minutes
description: In this section, you will learn how to use Splunk Synthetics to monitor the performance and availability of your applications.
---

{{% notice icon="user" style="orange" title="Persona" %}}

Putting your **SRE** hat back on, you have been asked to set up monitoring for the Online Boutique. You need to ensure that the application is available and performing well 24 hours a day, 7 days a week.

{{% /notice %}}

Wouldn’t it be great if we could have 24/7 monitoring of our application, and be alerted when there is a problem? This is where Synthetics comes in. We will show you a simple test that runs every 1 minute and checks the performance and availability of a typical user journey through the Online Boutique.
