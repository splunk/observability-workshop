---
title: NodeJS Workshop
weight: 2
description: A workshop using Zero Configuration Auto-Instrumentation for NodeJS.
hidden: true
---

The goal is to walk through the basic steps to configure the following components of the **Splunk Observability Cloud** platform:

* Splunk Infrastructure Monitoring (IM)
* Splunk Zero Configuration Auto Instrumentation for NodeJS (APM)
  * Database Query Performance
  * AlwaysOn Profiling

We will deploy the OpenTelemetry Astronomy Shop application, which has a NodeJS service. Once the application is up and running, we will instantly start seeing metrics and traces via the **Zero Configuration Auto Instrumentation** for NodeJS that will be used by the **Splunk APM** product.

{{% notice title="Prerequisites" style="primary" icon="info" %}}

* Outbound SSH access to port `2222`.
* Outbound HTTP access to port `8083`.
* Familiarity with the `bash` shell and `vi/vim` editor.

{{% /notice %}}
