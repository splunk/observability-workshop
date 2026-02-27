---
title: 4. How This Scales
weight: 4
---

## The Pattern Across Environments

In Phase 0 you ran a binary. In Phase 2 (Docker), you added one container. In Phase 3 (K8s), you added one DaemonSet. The pattern is the same:

| Environment | OBI Deployment | What Changes |
|---|---|---|
| Bare host | Binary via `sudo` | Nothing -- OBI watches processes from the kernel |
| Docker Compose | One container | Add a service to `docker-compose.yaml` |
| Kubernetes | One DaemonSet | `kubectl apply` a DaemonSet manifest |

For production, you would also consider the [OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) which can inject OBI as a sidecar automatically using annotations -- no DaemonSet needed.

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
- **One container** -- add it to your compose/K8s manifest and you're done
