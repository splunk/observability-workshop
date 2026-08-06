---
title: 1. Verify Agent Configuration
linkTitle: 1. Agent Configuration
time: 20 minutes
weight: 3
---

Start one Collector in Agent mode, send sample telemetry, and upload its
configuration to OTel Collector Config Builder.

{{% exercise title="Start the Agent" %}}

1. Open a terminal named **Agent Console** and run:

   ```bash
   cd [WORKSHOP]/1-agent
   source ../workshop-env.sh
   ../otelcol --config=agent_config.yaml
   ```

2. Leave the Agent running. Use `Ctrl-C` when a later step asks you to stop it.

3. Open a second terminal named **Loadgen** and run:

   ```bash
   cd [WORKSHOP]/1-agent
   ```

The same `agent_config.yaml` always writes local debug and file output. If you
enabled cloud export during setup, its traces and metrics pipelines also send
to Splunk Observability Cloud.

{{% expand title="Optional: terminal layout" %}}

Use three terminals during the workshop:

- **Agent Console** — the running Collector and debug output
- **Loadgen** — sample metrics, traces, and logs
- **Tests** — health checks and `jq` validation

{{% /expand %}}

{{% /exercise %}}

{{< checkpoint "The Agent is running from the single agent_config.yaml file." >}}
