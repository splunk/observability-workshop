---
title: Adding resilience to the agent
linkTitle: 4. Resilience
time: 10 minutes
weight: 4
---

In this section, you will learn how to you can add basic resilience to the OpenTelemetry Collector. This will have the collector create a local queue, and will use that to restart sending data when the connection is back.

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
Note, this will only be useful if the connections fails for a short period like a couple of minutes.  
If the connection is down for longer periods, the backend will drop the data anyways because the timing's are to far out of synch.

Secondly, this will works for logs, but we wil introduce a more robust solution in one of the upcoming collector builds  

{{% /notice %}}

### Setup

Create a new sub directory called `4-resilience` and copy the contents from `3-filelog` across. Create the appropriate log generation script script for your operating system in the new directory (`log-gen.sh` on Mac or Linux or `log-gen.ps1` for Windows).
