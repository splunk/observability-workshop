---
title: 1.1 Start and verify the Collector
linkTitle: 1.1 Start the Collector
weight: 1
time: 3 minutes
---

The Collector runs in the foreground and uses `agent_config.yaml`.

{{% exercise title="Start the Collector and check its health" %}}

{{< step "Start the Collector" "1" >}}

Reuse the terminal from the prerequisites as the **Collector terminal**. If you are
using a Splunk Show instance and closed that terminal, reconnect with the SSH
command and password supplied by email or by the facilitator.

In the **Collector terminal**, run:

```bash
cd 1-agent
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
cd 1-agent
```

You need only these two terminals: the reused **Collector terminal** and the
**Command terminal**.

{{< /step >}}

{{< step "Check Collector health" "3" >}}

In the **Command terminal**, check the Collector health endpoint:

```bash
curl -fsS http://127.0.0.1:13133/ && echo "Collector is ready"
```

Wait for `Collector is ready`. In the **Collector terminal**, confirm that the
Collector is still running without configuration errors.

{{< /step >}}

{{% /exercise %}}

{{< checkpoint "The Collector is running from the single agent_config.yaml file." >}}
