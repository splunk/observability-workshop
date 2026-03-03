---
title: 4. How This Scales
weight: 4
---

## The Pattern Across Environments

In Phase 0 you ran a binary. In Phase 2 (Docker), you added one container. In Phase 3 (K8s), you ran one `helm upgrade`. The pattern is the same:

| Environment | OBI Deployment | What Changes |
|---|---|---|
| Bare host | Binary via `sudo` | Nothing -- OBI watches processes from the kernel |
| Docker Compose | One container | Add a service to `docker-compose.yaml` |
| Kubernetes | Helm chart flag | `helm upgrade` with `--set="obi.enabled=true"` |

The [Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md) is the production way to deploy both the collector and OBI. For even more automation, the [OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) can inject OBI as a sidecar automatically using annotations.

## The Value Proposition

Many organizations have applications they **cannot** or **will not** instrument with OpenTelemetry SDKs:

- **Legacy systems**: COBOL-to-Java migrations, decade-old .NET Framework apps, vendor-provided binaries with no source access
- **Compiled languages**: Go, Rust, C++ services where recompilation isn't an option or the team has moved on
- **Developer resistance**: "We don't have time", "It's not in the sprint", "We're not changing working code"
- **Regulatory constraints**: Any code change triggers a full audit/certification cycle

OBI gives you **full distributed tracing without any code changes**:

- **Zero SDK integration** -- no imports, no dependencies, no compile-time changes
- **Zero application restarts** -- OBI attaches to already-running processes via eBPF
- **Language agnostic** -- works with Go, Node.js, Python, Java, Rust, C++ -- anything that speaks HTTP or gRPC
- **One container or one Helm flag** -- add it to your compose or enable `obi.enabled=true` in your Helm chart and you're done
