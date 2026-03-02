---
title: 3. Verify in Splunk APM
weight: 3
---

## Check Splunk APM

{{% notice title="Exercise" style="green" icon="running" %}}

1. Navigate to **APM** in Splunk Observability Cloud.
2. Filter by service name `warmup-app`.
3. You should see traces for the `/hello` endpoint.
**NOTE: This may take a number of minutes to ingest the first traces**

{{% /notice %}}

## What Just Happened?

1. The Flask app is "naked" -- it has zero observability code. It only knows how to say hello and send a heartbeat metric.
2. OBI attached eBPF probes to the kernel's networking stack and observed HTTP traffic flowing through your app's process.
3. OBI generated OpenTelemetry-compatible trace spans and sent them directly to Splunk.

**You just added distributed tracing to a running process from the kernel. No SDK, no code changes, no restart.**

This is the same technology you'll use in Phase 1 & 2, but inside Docker containers instead of bare processes.

## Clean Up Phase 0

Before moving on, stop the Python app and OBI:

``` bash
kill %1 2>/dev/null
sudo pkill -f ./obi 2>/dev/null
deactivate
```
