---
title: 1.1 Start and Verify the Agent
linkTitle: 1.1 Start the Agent
weight: 1
---

The Collector runs as a foreground process using `agent_config.yaml`. This
portable-binary approach works on both supported platforms.

{{% exercise title="Check Agent health" %}}

If you have not already started the Agent in the **Agent Console**, run:

```bash
cd [WORKSHOP]/1-agent
source ../workshop-env.sh
../otelcol --config=agent_config.yaml
```

Confirm that the startup output contains:

```text
Everything is ready. Begin running and processing data.
```

Leave that process running. In the **Tests** terminal, check the Agent health
extension:

```bash
curl -fsS http://127.0.0.1:13133/
```

The command succeeds when the foreground Agent is healthy. In the **Agent
Console**, also confirm that the Collector starts without configuration
errors and reports that it is ready to process data.

{{% /exercise %}}
