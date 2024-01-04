---
title: Zero Configuration - Payment Service
linkTitle: 4. Payment Service
weight: 4
---

## 1. Patching the Payment Service

Finally, we will patch the `paymentservice` deployment with an annotation to inject the NodeJS auto instrumentation. This will allow us to see the `paymentservice` service in **APM**.

``` bash
kubectl patch deployment opentelemetry-demo-paymentservice -n otel-demo -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-nodejs":"default/splunk-otel-collector"}}}} }'
```

This will cause the `opentelemetry-demo-paymentservice` pod to restart and after a few minutes, you should see the `paymentservice` service in **APM**.

![Paymentservice](../images/apm-paymentservice.png)
