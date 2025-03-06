---
title: 2.3 Send metrics from the Agent to the Gateway
linkTitle: 2.3 Send Metrics
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Agent**: In the **Agent terminal** window start the agent with the updated configuration:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Verify CPU Metrics**:

1. Check that when the `agent` starts, it immediately starts sending **CPU** metrics.
2. Both the `agent` and the `gateway` will display this activity in their debug output. The output should resemble the following snippet:

```text
<snip>
NumberDataPoints #37
Data point attributes:
    -> cpu: Str(cpu9)
    -> state: Str(system)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 9637.660000
```

At this stage, the `agent` continues to collect **CPU** metrics once per hour or upon each restart and sends them to the gateway. The **OpenTelemetry Collector**, running in `gateway` mode, processes these metrics and exports them to a file named `./gateway-metrics.out`. This file stores the exported metrics as part of the pipeline service.  

**Verify Data arrived at Gateway**:

In order to verify that CPU metrics, specifically for `cpu0`, have successfully arrived at the gateway by checking the `gateway-metrics.out` we will use the `jq` command.

This command below filters and extracts the `system.cpu.time` metric, focusing on `cpu0`, and displays its state (e.g., `user`, `system`, `idle`, `interrupt`) along with the corresponding values.

Run the following command in the **Tests terminal** to check the `system.cpu.time` metric:

{{% tabs %}}
{{% tab title="Check CPU Metrics" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "system.cpu.time") | .sum.dataPoints[] | select(.attributes[0].value.stringValue == "cpu0") | {cpu: .attributes[0].value.stringValue, state: .attributes[1].value.stringValue, value: .asDouble}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
  "cpu": "cpu0",
  "state": "user",
  "value": 123407.02
}
{
  "cpu": "cpu0",
  "state": "system",
  "value": 64866.6
}
{
  "cpu": "cpu0",
  "state": "idle",
  "value": 216427.87
}
{
  "cpu": "cpu0",
  "state": "interrupt",
  "value": 0
}
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
