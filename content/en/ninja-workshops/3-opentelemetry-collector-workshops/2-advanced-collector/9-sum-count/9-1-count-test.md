---
title: 9.1 Testing the Count Connector
linkTitle: 9.1 Test Count Connector
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory and run:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory and run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Start the Loadgen**: In the **Spans terminal** window navigate to the `[WORKSHOP]/9-sum-count` directory. Send 20 log line with the `loadgen`:

```bash { title="Loadgen" }
../loadgen -logs -json -count 20
```


```bash
jq '.resourceMetrics[].scopeMetrics[].metrics[]
    | select(.name == "logs.full.count" or .name == "logs.sw.count" or .name == "logs.lotr.count" or .name == "logs.error.count")
    | {name: .name, value: (.sum.dataPoints[0].asInt // "-")}' gateway-metrics.out
```

{{% /notice %}}
**Send a Regular Span**:

1. Locate the **Spans terminal** and navigate to the `[WORKSHOP]/8-routing-data` directory.
2. Start the `loadgen`.

Both the `agent` and `gateway` will display debug information. The gateway will also generate a new `gateway-traces-standard.out` file, as this is now the designated destination for regular spans.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you check `gateway-traces-standard.out`, it will contain the `span` sent by `loadgen`. You will also see an empty `gateway-traces-security.out` file, as the routing configuration creates output files immediately, even if no matching spans have been processed yet.
{{% /notice %}}