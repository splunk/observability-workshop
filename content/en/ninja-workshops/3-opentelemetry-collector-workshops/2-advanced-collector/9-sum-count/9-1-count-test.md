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

**Start the Loadgen**:  
In the **Spans terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory. Send 20 log lines with the following `loadgen` command:

```bash { title="Loadgen" }
../loadgen -logs -json -count 20
```

Both the `agent` and `gateway` will display debug information, showing they are processing data. Wait until the loadgen completes.

**Verify that metrics**  
While processing the logs, the **Agent**, has generated metrics and passed them on to the **Gateway**. The **Gateway** has written them into `gateway-metrics.out`.

To confirm the presence of `logs.full.count`, `logs.sw.count`, `logs.lotr.count` & `logs.error.count` in your metrics output, run the following jq query:

{{% tabs %}}
{{% tab title="jq query command" %}}

```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[]
    | select(.name == "logs.full.count" or .name == "logs.sw.count" or .name == "logs.lotr.count" or .name == "logs.error.count")
    | {name: .name, value: (.sum.dataPoints[0].asInt // "-")}' gateway-metrics.out
```

{{% /tab %}}
{{% tab title="jq example output" %}}

```text
{
  "name": "logs.sw.count",
  "value": "1"
}
{
  "name": "logs.error.count",
  "value": "1"
}
{
  "name": "logs.lotr.count",
  "value": "5"
}
{
  "name": "logs.full.count",
  "value": "6"
}
{
  "name": "logs.error.count",
  "value": "1"
}
{
  "name": "logs.lotr.count",
  "value": "7"
}
{
  "name": "logs.full.count",
  "value": "10"
}
{
  "name": "logs.sw.count",
  "value": "3"
}
{
  "name": "logs.lotr.count",
  "value": "3"
}
{
  "name": "logs.full.count",
  "value": "4"
}
{
  "name": "logs.sw.count",
  "value": "1"
}
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
