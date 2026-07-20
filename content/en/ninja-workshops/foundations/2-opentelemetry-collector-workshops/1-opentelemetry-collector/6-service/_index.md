---
title: OpenTelemetry Collector Service
linkTitle: 6. Service
weight: 6
---

The **Service** section is used to configure what components are enabled in the Collector based on the configuration found in the receivers, processors, exporters, and extensions sections.

{{% notice style="info" %}}
If a component is configured, but not defined within the **Service** section then it is **not** enabled.
{{% /notice %}}

The service section consists of three sub-sections:

- extensions
- pipelines
- telemetry

In the default configuration, the extension section has been configured to enable `health_check`, `pprof` and `zpages`, which we configured in the Extensions module earlier.

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

So lets configure our Metric Pipeline!
