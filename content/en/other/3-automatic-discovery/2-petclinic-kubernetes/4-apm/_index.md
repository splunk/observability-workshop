---
title: Setting up automatic discovery and configuration for APM
linkTitle: 4. Automatic discovery and configuration
weight: 5
time: 10 minutes
---

In this section we will enable **automatic discovery and configuration** for the Java services running in Kubernetes. This means that the OpenTelemetry Collector will look for Pod annotations that indicate that the Java application should be instrumented with the Splunk OpenTelemetry Java agent. This will allow us to get traces, spans, and profiling data from the Java services running on the cluster.

{{% notice title="automatic discovery and configuration" style="note" %}}

It is important to understand that automatic discovery and configuration is designed to get **trace, span & profiling** data out of your application, without requiring code changes or recompilation.

This is a great way to get started with APM, but it is **not** a replacement for manual instrumentation. Manual instrumentation allows you to add custom spans, tags, and logs to your application, which can provide more context and detail to your traces.

{{% /notice %}}

For Java applications the OpenTelemetry Collector will look for the annotation `instrumentation.opentelemetry.io/inject-java`.

The annotation can have the value set `true` or to the `namespace/daemonset` of the OpenTelemetry Collector e.g. `default/splunk-otel-collector`. This allows working across namespaces and what we will use in this workshop.

{{% notice title="Using the deployment.yaml" style="info" %}}

If you want your Pods to send traces automatically, you can add the annotation to the `deployment.yaml` as shown below. This will add the instrumentation library during the initial deployment. To speed things up we have done that for the following Pods:

- **admin-server**
- **config-server**
- **discovery-server**

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
