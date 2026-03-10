---
title: 3. Run and Verify in AppD
weight: 3
---

Now run the application with the AppDynamics agent attached. This is the "normal" single-destination instrumentation.

## Run with the AppDynamics Agent

Replace `<YOUR-ACCESS-KEY>`, and `<<YourInitials>>` with the values from the previous step:

{{< tabs >}}
{{% tab title="Command" %}}

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
  -jar app/target/ingest-workshop-1.0.0.jar & 
```

{{% /tab %}}
{{% tab title="Example" %}}

```text
java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=Dual-Ingest-JRH \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey="hj9999999999" \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

{{% /tab %}}
{{< /tabs >}}


Wait for the Spring Boot startup banner to appear (about 10-15 seconds).

## Generate Load

Start a simple load generator in the background:

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## Verify in the AppDynamics Controller

1. Open the [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/)
2. Navigate to **Applications** and find your application (e.g. `Dual-Ingest-YOURINITIALS`)
3. Click into the application to view the **Flow Map**

{{% notice title="Patience" style="info" icon="info-circle" %}}
It may take 2-5 minutes for the application to register and for business transactions to appear in the flow map. Refresh the page if needed.
{{% /notice %}}

You should see:

- The **OrderService** tier in the flow map
- Business transactions for `/order` and `/inventory` endpoints
- Metric data flowing into the controller

At this point, data is flowing **only to AppDynamics**. The application has no connection to Splunk Observability Cloud. In the next phase, you'll change that by enabling dual signal mode.
![AppDynamics Application](../../_images/appd-service.png?width=30vw)

{{% notice title="Keep it running" style="warning" icon="exclamation-triangle" %}}
Leave the application and load generator running. You'll stop them in the next section to add dual mode flags.
{{% /notice %}}
