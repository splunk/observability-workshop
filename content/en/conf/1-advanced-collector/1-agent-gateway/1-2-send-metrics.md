---
title: 1.2 Validate & Test Configuration
linkTitle: 1.2 Validate & Test Configuration
weight: 3
---

Now, we can start the **Gateway** and the **Agent**, which is configured to automatically send **Host Metrics** at startup. We do this to verify that data is properly routed from the **Agent** to the **Gateway**.

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway**: In the **Gateway terminal** window, run the following command to start the **Gateway**:

```bash {title="Start the Gateway"}
../otelcol --config=gateway.yaml
```

If everything is configured correctly, the collector will start and state `Everything is ready. Begin running and processing data.` in the output, similar to the following:

```text
2025-06-09T09:22:11.944+0100    info    service@v0.126.0/service.go:289 Everything is ready. Begin running and processing data. {"resource": {}}
```

Once the **Gateway** is running, it will listen for incoming data on port `5318` and export the received data to the following files:

* `gateway-traces.out`
* `gateway-metrics.out`
* `gateway-logs.out`

**Start the Agent**: In the **Agent terminal** window start the agent with the agent configuration:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Verify CPU Metrics**:

1. Check that when the **Agent** starts, it immediately starts sending **CPU** metrics.
2. Both the **Agent** and the **Gateway** will display this activity in their debug output. The output should resemble the following snippet:

```text
<snip>
NumberDataPoints #31
Data point attributes:
     -> cpu: Str(cpu3)
     -> state: Str(wait)
StartTimestamp: 2025-07-07 16:49:42 +0000 UTC
Timestamp: 2025-07-09 09:36:21.190226459 +0000 UTC
Value: 77.380000
        {"resource": {}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "metrics"}
```

At this stage, the **Agent** continues to collect **CPU** metrics once per hour or upon each restart and sends them to the gateway. The **Gateway** processes these metrics and exports them to a file named `gateway-metrics.out`. This file stores the exported metrics as part of the pipeline service.  

**Verify Data arrived at Gateway**: To confirm that CPU metrics, specifically for `cpu0`, have successfully reached the gateway, we’ll inspect the `gateway-metrics.out` file using the `jq` command.

The following command filters and extracts the `system.cpu.time` metric, focusing on `cpu0`. It displays the metric’s state (e.g., `user`, `system`, `idle`, `interrupt`) along with the corresponding values.

Open or create your third terminal window and name it **Tests**. Run the command below in the **Tests terminal** to check the `system.cpu.time` metric:

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

> [!IMPORTANT]
> Stop the **Agent** and the **Gateway** processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
