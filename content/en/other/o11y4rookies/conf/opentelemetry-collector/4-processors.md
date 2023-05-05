---
title: OpenTelemetry Collector Processors
linkTitle: 4. Processors
weight: 4
---

Processors are run on data between being received and being exported. Processors are optional though some are recommended.

``` yaml
processors:
  batch:
  resourcedetection:
    detectors: [system]
    override: true
```
