---
title: 2. Configure and Run
weight: 2
---

You will:

1. Set the environment variables that flip the launcher into combined mode.
2. Start the combined machine agent.

The Java app from Phase 1 keeps running unchanged.

## Set Combined Mode Environment Variables

Per the [Combined Agent docs](https://help.splunk.com/en/appdynamics-on-premises/infrastructure-visibility/26.4.0/machine-agent/combined-agent-for-infrastructure-visibility), environment variables have the highest precedence. Map your existing `${ACCESS_TOKEN}` and `${REALM}` to the names the bundled collector expects, and tag the host so it is easy to find in Splunk:

```bash
export SPLUNK_OTEL_ENABLED=true
export SPLUNK_ACCESS_TOKEN=${ACCESS_TOKEN}
export SPLUNK_REALM=${REALM}
export DEPLOYMENT_ENVIRONMENT=${INSTANCE}-appd-machine
```

`SPLUNK_OTEL_ENABLED=true` is what flips the launcher into combined mode. With it set, the launcher starts the bundled OTel collector at `otel-collector/bin/otelcol_linux_amd64` alongside the Java machine agent process and configures it from the bundled `conf/otel/agent_config.yaml`.

## Start the Combined Machine Agent

The launcher accepts the same `-D` system properties you used for the Java agent in Phase 1, plus `-d` for daemon mode. The launcher requires a pidfile when running detached, so we write one alongside the install:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
cd ~/workshop/appd/machine-agent

./bin/machine-agent -p ./machine-agent.pid -d \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=${APPD_APP_NAME} \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Machine-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey=${APPD_ACCESS_KEY} \
  -Dappdynamics.agent.uniqueHostId=${INSTANCE} \
  -Dappdynamics.sim.enabled=true
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
Using java executable at /home/splunk/workshop/appd/machine-agent/jre/bin/java
Starting OTel Collector: /home/splunk/workshop/appd/machine-agent/otel-collector/bin/otelcol_linux_amd64
OTel config: /home/splunk/workshop/appd/machine-agent/conf/otel/agent_config.yaml
OTel Collector started (PID=151396)
```

{{% /tab %}}
{{< /tabs >}}

The flags worth calling out:

| Flag | Purpose |
|---|---|
| `-p ./machine-agent.pid` | **Required by the launcher whenever `-d` is set.** Write the launcher PID to this file. |
| `-d` | Run the launcher detached as a background daemon. |
| `-Dappdynamics.agent.uniqueHostId=${INSTANCE}` | Pin the host identity so it matches `host.name` in Splunk and the AppDynamics machine identity. |
| `-Dappdynamics.sim.enabled=true` | Enable Server Visibility (SIM) so AppDynamics surfaces host metrics, not just JVM-side data. |

The launcher writes its own startup log to `machine-agent/logs/startup.out` and the bundled collector's log to `machine-agent/logs/otel/otel-collector.log`.

## Verify the Bundled Collector is Listening

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -s http://localhost:13133/ | jq
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
  "status": "Server available",
  "upSince": "2026-05-04T19:46:26.711526053Z",
  "uptime": "11.697620361s"
}
```

{{% /tab %}}
{{< /tabs >}}

This means the bundled collector is now scraping host metrics every 10 seconds and exporting them to Splunk Observability Cloud through the SignalFx exporter! The machine agent process also reports the same hardware data to the AppDynamics Controller over the AppD protocol.

The Java app from Phase 1 is still running and still sending APM data to AppDynamics only. Move on to verify both halves of the dual signal.
