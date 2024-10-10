---
title: Capture Prometheus metrics
weight: 11
---
Add a [prometheus receiver][prom-recv] to the OpenTelemetry Collector configuration so that it captures the metrics introduced in Task 2 from the application.

Hint: The hostname `host.docker.internal` allows you to access the host from within a docker container. Add

```bash
--add-host=host.docker.internal:host-gateway
```

to the docker run command for the OpenTelemetry collector.
TODO test instructions

Validate that you are getting data for the custom metric `characters_recv_total` introduced in Task 2.

The milestone for this task is `04service-metrics-prom`.

[prom-recv]: https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/simpleprometheusreceiver

