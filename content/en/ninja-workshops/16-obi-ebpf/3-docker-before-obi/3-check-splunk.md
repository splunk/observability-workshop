---
title: 3. Check Splunk
weight: 3
---

## Verify Infrastructure Metrics

{{% notice title="Exercise" style="green" icon="running" %}}

1. Open [Metric Finder](https://app.signalfx.com/#/metrics) and search for `workshop.heartbeat`
2. You should see the metric with `host.name` matching your `WORKSHOP_HOST_NAME` value.
3. Search for that `host.name` to see what other metrics the collector is sending (CPU, memory, disk, etc.).

{{% /notice %}}

## Confirm APM is Empty

{{% notice title="Exercise" style="green" icon="running" %}}

1. Navigate to **APM** in Splunk Observability Cloud.
2. Filter by the environment you defined (`WORKSHOP_ENVIRONMENT`).
3. It should be **empty** (or not exist). No services, no traces, no service map.

{{% /notice %}}

The collector is sending infrastructure metrics because that's what it does by default, but it has no traces to export because nothing is generating them.

{{% notice title="Note" style="info" %}}
This is the "before" state. You have three running services processing real requests, but Splunk APM has zero visibility into those requests. In the next section, you'll fix that -- **without touching the application code**.
{{% /notice %}}
