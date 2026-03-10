---
title: 2. Enable Dual Mode
weight: 2
---

Now restart the application with dual signal mode flags added to the JVM command line.

## Stop the Running Application

Stop the app and load generator from Phase 1:

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If `kill %1` doesn't work, find the PID with `ps aux | grep ingest-workshop` and kill it directly.
{{% /notice %}}

## Restart with Dual Mode

Run the app again with the same AppD flags, plus the dual mode and OTel exporter flags. Replace `<YOUR-ACCESS-KEY>` and `<YourInitials>` with the same values you used in Phase 1:

We are adding 4 lines just before we invoke the application `-jar app/target/ingest-workshop-1.0.0.jar &`

```bash
cd ~/workshop/appd

java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=Dual-Ingest-<YourInitials> \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey=<YOUR-ACCESS-KEY> \
  -Dagent.deployment.mode=dual \
  -Dotel.traces.exporter=otlp \
  -Dotel.exporter.otlp.endpoint=http://localhost:4318 \
  -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-${INSTANCE},deployment.environment=${INSTANCE}-appd-dual \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

Wait for the Spring Boot startup banner to appear.

### What the new flags do

| Flag | Purpose |
|---|---|
| `-Dagent.deployment.mode=dual` | Enables dual signal mode -- the full OTel Java auto-instrumentation runs alongside the AppD agent |
| `-Dotel.traces.exporter=otlp` | Tells the OTel instrumentation to export spans via OTLP |
| `-Dotel.exporter.otlp.endpoint` | Points to the local OTel Collector on port 4318 (HTTP/protobuf) |
| `-Dotel.resource.attributes` | Sets OTel resource attributes: `service.name` maps to the AppD tier, `service.namespace` maps to the AppD application, `deployment.environment` tags data for your workshop instance |

## Restart the Load Generator

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## Verify Dual Mode is Active

Check the application logs for confirmation that dual mode started:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
ps aux | grep "deployment.mode=dual" | grep -v grep
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-77-108 ~/workshop/appd $ ps aux | grep "deployment.mode=dual" | grep -v grep
splunk    181598  172  2.1 14402900 717736 pts/0 SNl  21:31   1:02 java -javaagent:agent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Dual-Ingest-JRH -Dappdynamics.agent.tierName=OrderService -Dappdynamics.agent.nodeName=OrderService-Node -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj9999999999 -Dagent.deployment.mode=dual -Dotel.traces.exporter=otlp -Dotel.exporter.otlp.endpoint=http://localhost:4318 -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-shw-a79e,deployment.environment=shw-a79e-appd-dual -jar app/target/ingest-workshop-1.0.0.jar
```

{{% /tab %}}
{{< /tabs >}}

You should see the java process with the `deployment.mode=dual` flag.

The AppDynamics agent is now sending:

- **AppD APM data** to the AppDynamics Controller (unchanged)
- **OTLP traces** to the local OTel Collector on `localhost:4318`, which forwards to Splunk Observability Cloud
    - use `env` in your instance to see the `{INSTANCE}` value used for your environment `deployment.environment=${INSTANCE}-appd-dual`
