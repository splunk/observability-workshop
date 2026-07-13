---
title: Zero-Code APM with OBI and eBPF
linkTitle: Zero-Code APM with OBI
weight: 4
time: 90 minutes
authors: ["Jeremy Hicks"]
description: Add full distributed tracing to apps with zero code changes using OpenTelemetry eBPF Instrumentation, streaming telemetry to Splunk Observability Cloud.
aliases:
  - /ninja-workshops/16-obi-ebpf/
---

In this workshop, you'll experience the power of **OpenTelemetry eBPF Instrumentation (OBI)** -- a zero-code approach to application performance monitoring that instruments your services directly from the Linux kernel.

You'll progress through three phases, each building on the last:

- **Phase 0 -- Python Warm-up**: Run a bare Python app on the host. Use the OBI binary to add APM tracing from the kernel -- no SDK, no code changes.
- **Phase 1 -- Docker (Before OBI)**: Deploy three polyglot microservices (Node.js + Go + Go) with Docker Compose. Confirm APM is empty.
- **Phase 2 -- Docker (The Magic)**: Add one OBI container. Full distributed traces appear in Splunk APM across all three services. Zero code changes.
- **Phase 3 -- Kubernetes**: Deploy the same services to K8s with the Splunk OTel Collector Helm chart. Enable OBI with one flag. Same zero-code tracing, enterprise-grade orchestration.

```text
Phase 0:  Python (:5150) ──── instrumented by OBI binary on host

Phase 1:  Frontend (Node.js :3000) → Order-Processor (Go :8080) → Payment-Service (Go :8081)
          ↑ infrastructure metrics only, APM is empty

Phase 2:  Same three services + one OBI container
          ↑ full distributed traces, zero code changes

Phase 3:  Same services on Kubernetes + Splunk OTel Collector Helm chart + obi.enabled=true
          ↑ same tracing, scales to any cluster
```
