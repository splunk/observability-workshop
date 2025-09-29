---
title: 7.3 Testing the Count Connector
linkTitle: 7.3 Test Sum Connector
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**:  
In the **Gateway terminal** window run:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**:  
In the **Agent terminal** window run:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**Start the Loadgen**:  
In the **Spans terminal** window send 8 spans with the following `loadgen` command:

```bash { title="Loadgen" }
../loadgen -count 8
```

Both the **Agent** and **Gateway** will display debug information, showing they are processing data. Wait until the loadgen completes.

**Verify the metrics**:  
While processing the span, the **Agent**, has generated metrics and passed them on to the **Gateway**. The **Gateway** has written them into `gateway-metrics.out`.

To confirm the presence of `user.card-charge`and verify each one has an attribute `user.name` in the metrics output, run the following jq query:

{{% tabs %}}
{{% tab title="jq query command" %}}

```bash

jq -r '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "user.card-charge") | .sum.dataPoints[] | "\(.attributes[] | select(.key == "user.name").value.stringValue)\t\(.asDouble)"' gateway-metrics.out | while IFS=$'\t' read -r name charge; do
    printf "%-20s %s\n" "$name" "$charge"
done    
```

{{% /tab %}}
{{% tab title="jq example output" %}}

```text
George Lucas         67.49
Frodo Baggins        87.14
Thorin Oakenshield   90.98
Luke Skywalker       51.37
Luke Skywalker       65.56
Thorin Oakenshield   67.5
Thorin Oakenshield   66.66
Peter Jackson        94.39
```

{{% /tab %}}
{{% /tabs %}} 

> [!IMPORTANT]
> Stop the **Agent** and the **Gateway** processes by pressing `Ctrl-C` in their respective terminals.

{{% /notice %}}
