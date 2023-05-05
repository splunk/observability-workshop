---
title: OpenTelemetry Collector Processors
linkTitle: 4. Processors
weight: 4
---

[Processors](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/README.md) are run on data between being received and being exported. Processors are optional though some are recommended.

There is [a large number of processors](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor) included in the OpenTelemetry contrib Collector.


Robert, thoughts on metrics transform processor example here? 

https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor


``` yaml
processors:
  batch:
  resourcedetection:
    detectors: [system]
    override: true
```
