---
title: 2. Enable Dual Mode on the Java Agent
weight: 2
---

The bundled collector is now running the workshop config and listening for OTLP on `localhost:4318`. Restart the Java app from Phase 1 in dual signal mode so its traces flow into that collector and onward to Splunk APM.

## Stop the Running Application

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If `kill %1` does not work, find the PID with `ps aux | grep ingest-workshop` and kill it directly.
{{% /notice %}}

## Restart with Dual Mode

Same AppD flags as Phase 1, with four additional lines that turn on dual signal mode and point the OTel side at the bundled collector. We reuse the `${APPD_ACCESS_KEY}` and `${APPD_APP_NAME}` variables from Phase 1.

```bash
cd ~/workshop/appd

java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=${APPD_APP_NAME} \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey=${APPD_ACCESS_KEY} \
  -Dagent.deployment.mode=dual \
  -Dotel.traces.exporter=otlp \
  -Dotel.exporter.otlp.endpoint=http://localhost:4318 \
  -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-${INSTANCE},deployment.environment=${INSTANCE}-appd-dual \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

Wait for the Spring Boot startup banner. Press return to get back to your prompt.

### What the new flags do

| Flag | Purpose |
|---|---|
| `-Dagent.deployment.mode=dual` | Enables dual signal mode. The full OTel Java auto-instrumentation runs alongside the AppD agent. |
| `-Dotel.traces.exporter=otlp` | Exports spans via OTLP. |
| `-Dotel.exporter.otlp.endpoint` | Points to the bundled collector on `localhost:4318` (OTLP HTTP). |
| `-Dotel.resource.attributes` | Stamps `service.name`, `service.namespace`, and `deployment.environment` on every span. `deployment.environment` here matches the value the workshop config's `resource/workshop` processor stamps, so spans, host metrics, and traces all land in the same Splunk APM environment. |

## Restart the Load Generator

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## Confirm Dual Mode is Active

{{< tabs >}}
{{% tab title="Command" %}}

```bash
ps aux | grep "deployment.mode=dual" | grep -v grep
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk    181598  172  2.1 14402900 717736 pts/0 SNl  21:31   1:02 java -javaagent:agent/javaagent.jar ... -Dagent.deployment.mode=dual -Dotel.traces.exporter=otlp -Dotel.exporter.otlp.endpoint=http://localhost:4318 -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-shw-a79e,deployment.environment=shw-a79e-appd-dual -jar app/target/ingest-workshop-1.0.0.jar
```

{{% /tab %}}
{{< /tabs >}}

The Java process now sends:

- **AppD APM data** to the AppDynamics Controller, unchanged.
- **OTLP traces** to the bundled collector on `localhost:4318`, which the workshop config forwards to Splunk APM via the `otlp_http` and `signalfx` exporters.

Move on to verify both destinations and then take a look at what the bundled-collector path actually cost.
