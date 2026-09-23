---
title: 8. APM to Logs
weight: 8
---

{{% exercise title="Open the Related Logs" %}}

You have identified the failing span, its error message, and the affected version of the **payment** service. The trace shows where the request failed; related *logs* may provide additional diagnostic details about why it failed.

**Related Content** connects telemetry from different parts of Splunk Observability Cloud. It uses shared metadata to preserve the context of your investigation as you move between traces, infrastructure, metrics, and logs.

For *trace-to-log* correlation, useful metadata can include:
* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

The exact metadata and available *Related Content* links depend on how your environment and log integration are configured.

{{< notice >}}
If the related logs option is not available, the logs might not contain the required correlation metadata, or the log integration might not be configured. Ask your instructor for guidance.
{{< /notice >}}

To open the logs associated with the trace:
* Scroll to the bottom of the *Trace Waterfall*.
* Select **Logs** in the Related Content bar. The number beside it indicates how many related log destinations are available.
* In the pop-up, select **Logs** for trace **<trace ID>**. This opens **Logs** with the trace context and relevant time range already applied.

![Related Logs](../images/apm-related-logs.png)

You have now moved from a user-visible failure in *RUM*, through its backend trace in *APM*, to the logs associated with that trace. On the next page, you’ll examine those log records for more information about the payment failure.

{{% /exercise %}}
