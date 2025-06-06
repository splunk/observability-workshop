---
title: 9.1 Testing the Count Connector
linkTitle: 9.1 Test Count Connector
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**:  
In the **Gateway terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory and run:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**:  
In the **Agent terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory and run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Send 12 Logs lines with the Loadgen**:  
In the **Spans terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory.  
Send 12 log lines, they should be read in two intervals. Do this with the following `loadgen` command:

```bash { title="Loadgen" }
../loadgen -logs -json -count 12
```

Both the `agent` and `gateway` will display debug information, showing they are processing data. Wait until the loadgen completes.

**Verify metrics have been generated**  
As the logs are processed, the **Agent** generates metrics and forwards them to the **Gateway**, which then writes them to `gateway-metrics.out`.

To check if the metrics `logs.full.count`, `logs.sw.count`, `logs.lotr.count`, and `logs.error.count` are present in the output, run the following **jq** query:

{{% tabs %}}
{{% tab title="jq query command" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[]
    | select(.name == "logs.full.count" or .name == "logs.sw.count" or .name == "logs.lotr.count" or .name == "logs.error.count")
    | {name: .name, value: (.sum.dataPoints[0].asInt // "-")}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="jq example output" %}}

```json
{
  "name": "logs.sw.count",
  "value": "2"
}
{
  "name": "logs.lotr.count",
  "value": "2"
}
{
  "name": "logs.full.count",
  "value": "4"
}
{
  "name": "logs.error.count",
  "value": "2"
}
{
  "name": "logs.error.count",
  "value": "1"
}
{
  "name": "logs.sw.count",
  "value": "2"
}
{
  "name": "logs.lotr.count",
  "value": "6"
}
{
  "name": "logs.full.count",
  "value": "8"
}
```

{{% /tab %}}
{{% /tabs %}}
{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Note: the `logs.full.count` normally is equal to `logs.sw.count` + `logs.lotr.count`, while the `logs.error.count` will be a random number.
{{% /notice %}}

> [!IMPORTANT]
> Stop the `agent` and the `gateway` processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
