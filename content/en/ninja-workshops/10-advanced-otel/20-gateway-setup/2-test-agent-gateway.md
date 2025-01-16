---
title: Testing the Route from agent via gateway
linkTitle: 2.2 Agent -> Gateway
weight: 2
---

## Validate Agent and Gateway routing

Verify the gateway is running in its own shell and is ready to receive data, then in the agent Shell, restart the agent with:

```bash
[LOCATION_OF_OTELCOLLECTOR]/otelcol --config=agent.yaml
```

The agent should start to send *cpu* metrics again and both the agent and the gateway should reflect that in their output:

```text
<snip>
NumberDataPoints #37
Data point attributes:
     -> cpu: Str(cpu9)
     -> state: Str(system)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 9637.660000
NumberDataPoints #38
Data point attributes:
     -> cpu: Str(cpu9)
     -> state: Str(idle)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 2064591.290000
NumberDataPoints #39
Data point attributes:
     -> cpu: Str(cpu9)
     -> state: Str(interrupt)
StartTimestamp: 2024-12-09 14:18:28 +0000 UTC
Timestamp: 2025-01-15 15:27:51.319526 +0000 UTC
Value: 0.000000
	{"kind": "exporter", "data_type": "metrics", "name": "debug"}
  ```

Check if a **gateway-metrics.out** is created.

Now run the curl command to send a trace:

```text
curl -X POST -i http://localhost:4318/v1/traces \
-H "Content-Type: application/json" \
 -d @trace.json 
```

Check for the gateway-traces.out
