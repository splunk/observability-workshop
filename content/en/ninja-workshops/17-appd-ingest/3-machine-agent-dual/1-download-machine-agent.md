---
title: 1. Download the Machine Agent
weight: 1
---

The same `download-appd-agent.sh` script you used to fetch the Java agent in Phase 1 takes an optional argument. Pass `machine` to fetch the latest 64-bit Linux machine agent bundle (with a bundled JRE and a bundled OTel collector binary).

## Run the Download Script

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cd ~/workshop/appd
./download-appd-agent.sh machine
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
Downloading agent from: https://download-files.appdynamics.com/download-file/machine-bundle/26.x.y.zzzz/machineagent-bundle-64bit-linux-26.x.y.zzzz.zip
Archive:  ./MachineAgent.zip
  inflating: machine-agent/machineagent.jar
  inflating: machine-agent/conf/controller-info.xml
  ...
```

{{% /tab %}}
{{< /tabs >}}

The bundle unpacks into `~/workshop/appd/machine-agent/`. The pieces you will touch in the next page:

| Path | What it is |
|---|---|
| `bin/machine-agent` | Launcher script. Knows how to start both the Java machine agent and the bundled OTel collector. |
| `conf/controller-info.xml` | AppDynamics Controller settings (we will pass these via `-D` flags instead, so we do not need to edit it). |
| `conf/otel/agent_config.yaml` | Default OTel Collector config. Hostmetrics + signalfx exporter, which is exactly what we need for this phase. We use it as-is. |
| `otel-collector/bin/otelcol_linux_amd64` | The bundled OTel Collector binary. |
| `jre/bin/java` | Bundled JRE so you do not need a system JDK. |

{{% notice title="Why a bundled JRE" style="info" icon="info-circle" %}}
The machine agent runs as a Java process. Using `jre/bin/java` from the bundle keeps the workshop independent of whatever JDK happens to be on the instance and matches the version AppDynamics qualifies the agent against.
{{% /notice %}}
