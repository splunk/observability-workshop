---
title: 1.2 Send Metrics
linkTitle: 1.2 Send Metrics
weight: 3
---
Now that the **gateway** is running, it’s time to test the full telemetry flow.

We’ll start the **agent**, which will begin by sending **metrics**. Then we’ll send **traces** and generate **logs** to verify that all signals are properly routed through the agent to the gateway.

You should see the resulting output appear in the following files:

* `gateway-traces.out`
* `gateway-metrics.out`
* `gateway-logs.out`

This will confirm that communication between the agent and gateway is working as expected.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Agent**: In the **Agent terminal** window start the agent with the agent configuration:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Verify CPU Metrics**:

1. Check that when the **Agent** starts, it immediately starts sending **CPU** metrics.
2. Both the **Agent** and the **Gateway** will display this activity in their debug output. The output should resemble the following snippet:

```text
<snip>
NumberDataPoints #37
Data point attributes:
    -> cpu: Str(cpu0)
    -> state: Str(system)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 9637.660000
```

At this stage, the **Agent** continues to collect **CPU** metrics once per hour or upon each restart and sends them to the gateway.

The **Gateway** processes these metrics and exports them to a file named `./gateway-metrics.out`. This file stores the exported metrics as part of the pipeline service.  

**Verify Data arrived at Gateway**: To confirm that CPU metrics, specifically for `cpu0`, have successfully reached the gateway, we’ll inspect the `gateway-metrics.out` file using the `jq` command.

The following command filters and extracts the `system.cpu.time` metric, focusing on `cpu0`. It displays the metric’s state (e.g., `user`, `system`, `idle`, `interrupt`) along with the corresponding values.

Run the command below in the **Tests terminal** to check the `system.cpu.time` metric:

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
