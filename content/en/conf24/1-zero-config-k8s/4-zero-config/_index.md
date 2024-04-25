---
title: Setting up Zero configuration Auto instrumentation for APM
linkTitle: 4. Auto-instrumentation & Metrics
weight: 5
---

In the previous section, we enabled the OpenTelemetry Collector for Kubernetes on our cluster and configured it to send metrics both Kubernetes and Mysql metrics to **Splunk Observability Cloud**. This next section will enable Zero-Config Auto-Instrumentation for our Java services running on the cluster.

{{% notice title="Zero Config Auto Instrumentation" style="info" %}}

It is important to understand that Zero-Config Auto-instrumentation is designed to get Trace/Span & Profiling data out of your existing application, without requiring you to change your code or requiring to rebuild.

{{% /notice %}}

For this workshop, we will be using the Zero config option of the Opentelemetry Collector in Kubernetes.
This means that the Collector monitors your pods running in Kubernetes, and if they match certain criteria, they will enable auto-instrumentation on the pod.

For Java, it is looking for the Kubernetes tag `instrumentation.opentelemetry.io/inject-java` set to `true` or to the location of the Otel collector, like `default/splunk-otel-collector`. The last one will work across namespaces, so this is what we will use in our examples.

{{% notice title="Using the deployment.yaml" style="info" %}}

If you want your pods to send traces automatically, you can add the annotation to the `deployment.yaml` as shown below. This will add the instrumentation library during the initial deployment. To speed things up we have done that for the management pods: **admin-server**, **config-server** and **discovery-server**.

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: admin-server
  labels: 
    app.kubernetes.io/part-of: spring-petclinic
spec:
  selector:
    matchLabels:
      app: admin-server
  template:
    metadata:
      labels:
        app: admin-server
      annotations:
        instrumentation.opentelemetry.io/inject-java: "default/splunk-otel-collector"
```

{{% /notice %}}
