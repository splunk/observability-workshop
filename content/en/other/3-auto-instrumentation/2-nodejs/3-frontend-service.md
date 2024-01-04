---
title: Zero Configuration - Frontend Service
linkTitle: 3. Frontend Service
weight: 3
---

## 1. Patching the Frontend service

First, confirm that you can see your environment in **APM**. There should be a service called `loadgenerator` displayed in the Service map.

![APM Service Map](../images/apm-servicemap.png)

Next, we will patch the `frontend` deployment with an annotation to inject the NodeJS auto instrumentation. This will allow us to see the `frontend` service in **APM**. Note, that at this point we have not edited any code.

``` bash
kubectl patch deployment opentelemetry-demo-frontend -n otel-demo -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-nodejs":"default/splunk-otel-collector"}}}} }'
```

* This will cause the `opentelemetry-demo-frontend` pod to restart.
* The annotation value `default/splunk-otel-collector` refers to the instrumentation configuration named `splunk-otel-collector` in the `default` namespace.
* If the chart is not installed in the `default` namespace, modify the annotation value to be `{chart_namespace}/splunk-otel-collector`.

After a few minutes, you should see the `frontend` service in **APM**.

![Frontend](../images/apm-frontend.png)

With the `frontend` service highlighted, click on the **Traces** tab to see the traces for the service. Select one of the traces and confirm that the trace contains metadata confirming that the Splunk Zero-Configuration Auto-Instrumentation for NodeJS is being used.

![Zero Configuration](../images/apm-frontend-trace.png)
