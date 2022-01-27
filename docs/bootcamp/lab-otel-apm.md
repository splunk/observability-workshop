# Lab: Application Performance Monitoring

## Goals

1. Understand GDI path for APM for common tech stacks (Docker, K8s).
1. Be able to instrument an app from scratch (traces, custom metadata).
1. Understand how distributed tracing works across tech stacks (header propagation, …)

## Future Tasks

TODO YOUR Idea here? Let us know!

TODO metrics method being traced - how to disable?

```python
from opentelemetry.context import attach, detach, set_value
token = attach(set_value("suppress_instrumentation", True))
```

TODO autodetect metrics with k8s labels: `prometheus.io/scrape: true` - run prometheus on separate port `9090`.

TODO [tracing examples][py-trace-ex]

[py-trace-ex]: https://github.com/open-telemetry/opentelemetry-python/blob/main/docs/examples/

