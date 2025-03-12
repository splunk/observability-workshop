---
title: 9.3 Testing the Count Connector
linkTitle: 9.3 Test Sum Connector
weight: 3
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
printf "\033[1m%-20s %s\033[0m\n" "Name" "Credit Card Charge"
jq -r '.resourceMetrics[].scopeMetrics[].metrics[] | select(.name == "user-card-total") | .sum.dataPoints[] | "\(.attributes[] | select(.key == "user.name").value.stringValue)\t\(.asDouble)"' gateway-metrics.out | while IFS=$'\t' read -r name charge; do
    printf "%-20s %s\n" "$name" "$charge"
done    
```

{{% /tab %}}
{{% tab title="jq example output" %}}

```text
George Lucas        68.02
Frodo Baggins       57.58
Frodo Baggins       79.95
Thorin Oakenshield  85.55
Thorin Oakenshield  81.27
Frodo Baggins       61.28
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
