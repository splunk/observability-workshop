---
title: 1.1 Start and verify the agent
linkTitle: 1.1 Start the agent
weight: 1
---

The Collector runs in the foreground and uses `agent_config.yaml`.

{{% exercise title="Start the agent and check its health" %}}

{{< step "Start the agent" "1" >}}

Reuse the terminal from the prerequisites as the **Agent terminal**. If you are
using a Splunk Show instance and closed that terminal, reconnect with the SSH
command and password supplied by email or by the facilitator.

In the **Agent terminal**, run:

```bash
cd [WORKSHOP]/1-agent
source ../workshop-env.sh
../otelcol --config=agent_config.yaml
```

Leave the Collector running in the foreground. This terminal displays Collector
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

You need only these two terminals: the reused **Agent terminal** and the
**Command terminal**.

{{< /step >}}

{{< step "Check agent health" "3" >}}

In the **Command terminal**, check the agent health endpoint:

```bash
curl -fsS http://127.0.0.1:13133/ && echo "Collector is ready"
```

Wait for `Collector is ready`. In the **Agent terminal**, confirm that the
Collector is still running without configuration errors.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The agent is running from the single agent_config.yaml file." >}}
