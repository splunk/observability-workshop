---
title: 8. APM to Logs
weight: 8
---

{{% notice title="Exercise" style="green" icon="running" %}}

Now that we have identified the version of the **paymentservice** that is causing the issue, let's see if we can find out more information about the error. This is where **Related Logs** come in.

Related Content relies on specific metadata that allows APM, Infrastructure Monitoring, and Log Observer to pass filters around Observability Cloud. For related logs to work, you need to have the following metadata in your logs:

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

* At the very bottom of the **Trace Waterfall** click on **Logs**. This highlights that there are **Related Logs** for this trace.
* Click on the **Logs for trace xxx** entry in the pop-up, this will open the logs for the complete trace in **Logs**.

![Related Logs](../images/apm-related-logs.png)

* Next, let's find out more about the error in the logs.

{{% /notice %}}
