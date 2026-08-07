---
title: 1.1 Start and Verify the Agent
linkTitle: 1.1 Start the Agent
weight: 1
---

The Collector runs as a foreground process using `agent_config.yaml`. This
portable-binary approach works on the supported Linux systems and Apple
Silicon Macs.

{{% exercise title="Start the Agent and check its health" %}}

{{< step "Start the Agent" "1" >}}

Reuse the terminal from the prerequisites as the **Agent Console**. If you are
using a Splunk Show instance and closed that terminal, reconnect with the SSH
command and password supplied by email or by the facilitator.

In the **Agent Console**, run:

```bash
cd [WORKSHOP]/1-agent
source ../workshop-env.sh
../otelcol --config=agent_config.yaml
```

Leave the Agent running in the foreground. This terminal displays Collector
startup messages and debug exporter output.

{{< /step >}}

{{< step "Open one command terminal" "2" >}}

Open one additional terminal for load generation, health checks, and `jq`
validation. This is the **Command terminal** used throughout the workshop.

If you are using a Splunk Show instance, connect again with the same SSH
command and password. Then run:

```bash
cd [WORKSHOP]/1-agent
```

You need only these two terminals: the reused **Agent Console** and the
**Command terminal**.

{{< /step >}}

{{< step "Check Agent health" "3" >}}

In the **Command terminal**, check the Agent health
extension:

```bash
curl -fsS http://127.0.0.1:13133/ && \
echo "Collector is ready"
```

Treat the successful health response as the readiness checkpoint. In the
**Agent Console**, confirm only that the Collector remains running without
configuration errors.

{{< /step >}}

The normal `metrics` pipeline sends full host metrics to SignalFx when cloud
export is enabled. The throttled `metrics/workshop` pipeline always provides
bounded local debug and file output. `metrics/internal` retains Collector
self-monitoring, `logs/signalfx` retains the default process-list path, and
`logs/entities` remains available for discovery mode. The retained `logs`
pipeline stays on `nop` during the live lab, while `logs/workshop` provides
local debug and file output for the exercises.

{{% /exercise %}}

{{< checkpoint "The Agent is running from the single agent_config.yaml file." >}}
