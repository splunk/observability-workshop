---
title: Distributed Tracing and Bi-Directional Drilldowns
linkTitle: 4. Distributed Tracing
weight: 4
time: 25 minutes
description: Enable supported trace correlation between ThousandEyes and Splunk APM so teams can move between the two products during an investigation.
---

This section turns the ThousandEyes and Splunk integration into a true investigation workflow. In the previous section, ThousandEyes streamed synthetic metrics into Splunk Observability Cloud. In this section, you will enable the supported **ThousandEyes <-> Splunk APM distributed tracing integration** so network, platform, and application teams can pivot between both tools while looking at the same request.

{{% notice title="Why This Matters" style="primary" icon="lightbulb" %}}
This is the piece that gives you **bi-directional access** between the two environments. ThousandEyes can open the related trace in Splunk APM, and Splunk APM can take you back to the originating ThousandEyes test.
{{% /notice %}}

## What You Will Learn

By the end of this section, you will be able to:

- Deploy and use the included Spring PetClinic Kubernetes application as a trace target
- Instrument an internal service so it sends traces to Splunk APM
- Enable distributed tracing on a ThousandEyes **HTTP Server** or **API** test
- Configure the ThousandEyes **Generic Connector** for Splunk APM
- Open the ThousandEyes **Service Map** and jump directly into the corresponding Splunk trace
- Use the ThousandEyes metadata in Splunk APM to jump back to the original ThousandEyes test

## Step 1: Enable Instrumentation and make ThousandEyes changes

We are going to patch every PetClinic Java deployment to two things:
* The Java injection (which instruments the service)
* The OTEL Propagators (to ensure all 3 are set)
* The sampler to `be parentbased_always_on`

```bash
kubectl edit instrumentation splunk-otel-collector 
```

#### THIS SECTION NEEDS TO BE FIXED

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: splunk-otel-collector
spec:
  propagators:
    - baggage
    - b3
    - tracecontext
  sampler:
    type: parentbased_always_on
```

Then deploy it with:
```bash
kubectl apply -f instrumentation.yaml
```

This is the critical part for the ThousandEyes scenario:

- `b3` allows extraction of ThousandEyes B3 headers.
- `tracecontext` preserves traceparent and tracestate.
- `parentbased_always_on` ensures the trace continues once ThousandEyes starts the request.

Then let's inject the java instrumentation:
```bash
kubectl get deployments -l app.kubernetes.io/part-of=spring-petclinic -o name | xargs -I % kubectl patch % -p "{\"spec\": {\"template\":{\"metadata\":{\"annotations\":{\"instrumentation.opentelemetry.io/inject-java\":\"default/splunk-otel-collector\"}}}}}"
```

For other runtimes, use the annotation that matches the language:
- `instrumentation.opentelemetry.io/inject-nodejs`
- `instrumentation.opentelemetry.io/inject-python`
- `instrumentation.opentelemetry.io/inject-dotnet`

We can check that our instrumentation deployed with:
```bash
kubectl exec -n default deploy/api-gateway -- printenv | \
  grep -E 'Image:|OTEL_EXPORTER_OTLP_ENDPOINT|OTEL_PROPAGATORS|OTEL_TRACES_SAMPLER|OTEL_RESOURCE_ATTRIBUTES'
```

You can see that this pod now has the Java instrumentation enabled, and the propagators are including `baggage`, `b3` and `tracecontext`.

Validate the in-cluster API path from the namespace where the ThousandEyes Enterprise Agent runs:

```bash
kubectl run te-petclinic-curl \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl \
  --command -- curl -sS http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

We are going to use this URL for the trace-enabled ThousandEyes **HTTP Server** or **API** tests from the TE agent:

```text
http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

### Validate That Traces Exist

1. Wait for the deployment rollout to finish:

   ```bash
   kubectl rollout status deployment/api-gateway
   ```

2. Generate a few requests against the PetClinic API gateway:

   ```text
   http://api-gateway.default.svc.cluster.local:82/api/customer/owners
   ```

   This request enters through the PetClinic API gateway, routes to `customers-service`, and queries the PetClinic database. It produces a more useful trace than a simple health check.

3. Confirm that traces are arriving in **Splunk APM** before you continue.

{{% notice title="Learning Tip" style="info" %}}
Use a business transaction, not a pure `/health` endpoint, for the tracing exercise. A multi-service request gives you a far better Service Map in ThousandEyes and a more useful trace in Splunk APM.
{{% /notice %}}

## Step 2: Create the Splunk APM Connector in ThousandEyes

{{% notice title="Only need 1 integration" style="warning" %}}
Rather than having each workshop attendee set this up, watch your instructor perform the following steps.

You will continue on Step 3 (Configure Distributed Tracing on the ThousandEyes Test).
{{% /notice %}}

The metric streaming integration from the previous section uses an **Ingest** token. This step is different: ThousandEyes needs to query Splunk APM and build trace links, so it uses a Splunk **API** token instead.

1. In Splunk Observability Cloud, create an access token with the **API** scope.
2. In ThousandEyes, go to **Manage > Integrations > Integrations 2.0**, and change to the **Connectors** tab.
3. Create a **Generic Connector**. You can select the Preset as **Splunk Observability APM**:
  - **Name**: `Splunk APM`
  - **Target URL**: `https://api.<REALM>.signalfx.com`
  - **Header**: `X-SF-Token: <your-api-scope-token>`
4. **Save and Assign Operation**

![Splunk APM Generic Connector in ThousandEyes](../images/splunk-apm-generic-connector.png)

5. Create a **New Operation** and select **Splunk Observability APM**.
6. Name it `Splunk APM`.
7. **Save & Assign Connector** to enable the operation and save the integration.
8. Select the connector and click **Save**.

![Splunk APM Operation in ThousandEyes](../images/splunk-apm-operation.png)

## Step 3: Configure Distributed Tracing on the ThousandEyes Test

Create or edit an **API** test that targets the instrumented backend endpoint from Step 1.

1. In ThousandEyes, go to create an **Network&App Synthetics > Test Settings**.
2. Click **Add New Test** and then select **API**
3. Enter the URL (i.e. `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`)
4. Where test runs from: `Select your agent` and **close**
5. Set the name to `Your name - API`
6. Under **API Performance (Optional)**, enable **Distributed Tracing**
7. Click **Next**
8. Name the step **Test Kubernetes** and set the URL to `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
9. Click **Deploy**, and then check the test results. You can run a test without changes.

![Enable Distributed Tracing in ThousandEyes](../images/distributed-tracing-enable.png)

After the test runs, ThousandEyes injects the trace headers and captures the trace context for that request.

It may take some time for the trace to show up. You can go to the service map (in ThousandEyes) and copy the trace id to find in Observability Cloud. You will see the trace is likely still in progress.

## Step 4: Validate the Bi-Directional Investigation Loop

Once the test is running and the connector is enabled, validate the workflow in both directions.

### Start in ThousandEyes

1. Open the test in ThousandEyes.
2. Navigate to the **Service Map** tab.
3. Confirm that you can see the trace path, service latency, and any downstream errors.
4. Use the ThousandEyes link into **Splunk APM** to inspect the full trace.

![ThousandEyes Service Map with Splunk APM correlation](../images/thousandeyes-service-map.png)

### Continue in Splunk APM

Inside Splunk APM, verify that the trace contains ThousandEyes metadata such as:

- `thousandeyes.account.id`
- `thousandeyes.test.id`
- `thousandeyes.permalink`
- `thousandeyes.source.agent.id`

Use either the `thousandeyes.permalink` field or the **Go to ThousandEyes test** button in the trace waterfall view to navigate back to the originating ThousandEyes test.

![Splunk APM trace linked back to ThousandEyes](../images/splunk-apm-trace.png)

## Suggested Learning Scenario

Try now creating a web test, using a cloud agent and your url (for example `http://i-0cedf3429f9192aaa.splunk.show:81/#!/owners`, replace with your own instance).


## Need to recheck this section

Use the following flow during a workshop:

1. Create a ThousandEyes test against an internal API route that calls multiple services.
2. Let ThousandEyes surface the issue first, so the class starts from the network and synthetic-monitoring perspective.
3. Open the **Service Map** in ThousandEyes and identify where latency or errors begin.
4. Jump into **Splunk APM** for span-level analysis.
5. Jump back to **ThousandEyes** to inspect the test, agent, and network path again.

This is a strong teaching loop because it mirrors how different teams actually work:

- Network and edge teams often start in ThousandEyes.
- SRE and platform teams often start in Splunk dashboards or alerts.
- Application teams usually want the trace in Splunk APM.

With this integration in place, everyone can pivot without losing context.

## Common Pitfalls

- A test might be visible in Splunk dashboards but still have no trace correlation. That usually means only the **metrics** stream is configured, not the **Splunk APM Generic Connector**.
- A trace might exist in Splunk APM but not show up in ThousandEyes if the monitored endpoint does not propagate the trace headers downstream.
- A shallow endpoint such as `/health` often produces limited trace value even when the configuration is correct.

## References

- [ThousandEyes Distributed Tracing](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)
- [ThousandEyes Distributed Tracing with Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)
- [Splunk APM: View traces with Cisco ThousandEyes integration](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace)
- [Splunk OTel Collector zero-code instrumentation for Kubernetes language runtimes](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/automatic-discovery-of-apps-and-services/kubernetes/language-runtimes)
