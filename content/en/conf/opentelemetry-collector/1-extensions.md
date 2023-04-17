---
title: OpenTelemetry Collector Extensions
linkTitle: 1. Extensions
weight: 1
---

Extensions are available primarily for tasks that do not involve processing telemetry data. Examples of extensions include health monitoring, service discovery, and data forwarding. Extensions are optional.

```yaml
extensions:
  health_check:
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679
```

## Health Check

## Performance Profiler

## zPages
