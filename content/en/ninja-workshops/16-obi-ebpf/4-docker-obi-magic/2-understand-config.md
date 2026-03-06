---
title: 2. Understand the OBI Config
weight: 2
---

## The OBI Configuration File

Open `obi-config.yaml` (already in the repo) to understand how OBI discovers and instruments your services:

``` bash
cat ~/workshop/obi/02-obi-docker/obi-config.yaml
```

``` yaml
discovery:
  instrument:
    - name: "frontend"
      open_ports: 3000
    - name: "order-processor"
      open_ports: 8080
    - name: "payment-service"
      open_ports: 8081

ebpf:
  context_propagation: all

otel_traces_export:
  endpoint: http://localhost:4318
```

### How Each Section Works

**`discovery.instrument`** tells OBI how to find your services and what to name them. It matches processes by the ports they listen on, then assigns the `name` as the `service.name` attribute in the generated traces. Without this, OBI would use the executable path as the service name (e.g. `/usr/local/bin/order-processor`).

**`context_propagation: all`** is the key to distributed tracing. OBI injects `Traceparent` headers into outgoing HTTP requests at the kernel level. This is how a trace started in `frontend` connects through `order-processor` to `payment-service` -- even though none of these services know anything about tracing.

**`otel_traces_export.endpoint`** tells OBI where to send traces. Because OBI uses `network_mode: host`, `localhost:4318` reaches the collector's port that is mapped to the host in the compose file.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
For deeper configuration options, see the OBI documentation:

* [Service discovery](https://opentelemetry.io/docs/zero-code/obi/configure/service-discovery)
* [Context propagation](https://opentelemetry.io/docs/zero-code/obi/configure/metrics-traces-attributes/#context-propagation)
* [Config example](https://opentelemetry.io/docs/zero-code/obi/configure/example/)
{{% /notice %}}
