---
title: OpenTelemetry Collector Receivers
linkTitle: 3. Receivers
weight: 3
---

A receiver, which can be push or pull based, is how data gets into the Collector. Receivers may support one or more data sources.

### Host Metrics Receiver

```yaml
  hostmetrics:
    collection_interval: 10s
    scrapers:
      cpu:
      disk:
      filesystem:
      memory:
      network:
      # System load average metrics https://en.wikipedia.org/wiki/Load_(computing)
      load:
      # Paging/Swap space utilization and I/O metrics
      paging:
      # Aggregated system process count metrics
      processes:
      # System processes metrics, disabled by default
      # process:
```
