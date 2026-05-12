---
title: "Phase 2: Combined Machine Agent"
linkTitle: 3. Machine Agent Dual
weight: 3
archetype: chapter
time: 10 minutes
description: Add infrastructure dual signal to your AppDynamics-only setup using the AppDynamics Combined Machine Agent, which ships with a bundled OTel collector and reports host metrics to both AppDynamics and Splunk Observability Cloud.
---

In Phase 1 your Java application reports APM data to the AppDynamics Controller and nothing else. The simplest first step toward Splunk Observability Cloud is **infrastructure dual signal**: report host metrics (CPU, memory, disk, network) to both platforms from a single agent.

The **AppDynamics Machine Agent** ships with a minimal OpenTelemetry Collector binary bundled inside the install. 
- One environment variable (`SPLUNK_OTEL_ENABLED=true`) starts both processes and the bundled collector forwards host metrics to Splunk while the machine agent process continues reporting to the AppDynamics Controller.

What you **do not** get from the AppD bundle is a fully-configured Splunk OTel Collector deployment with all of the correlation and log goodness.  
The bundled config is intentionally narrow: a `hostmetrics` receiver and the `signalfx` exporter, no traces, logs, or profiling pipelines. That is fine for infrastructure dual signal, but it is not a substitute for the workshop config we apply in Phase 3 or the standalone Splunk OTel Collector install in Phase 4.

In this phase you will:

1. Download the machine agent bundle using the same `download-appd-agent.sh` script you used for the Java agent in Phase 1, with a `machine` argument.
2. Start the combined machine agent.
3. Verify host metrics in **AppDynamics Server Visibility** and in **Splunk O11y Infrastructure**.

APM data still flows only to AppDynamics at the end of this phase. **Phase 3** broadens that by dropping the workshop's full `collector-config.yaml` into the same bundled collector and turning on dual signal mode on the Java agent. **Phase 4** then takes the same workshop config and runs it under the standalone Splunk OTel Collector install, the configuration we recommend for production observability.

{{% notice title="Why infra first" style="info" icon="info-circle" %}}
The combined machine agent is the lowest-effort dual signal step for an AppDynamics shop: it is one extra environment variable on an agent you already deploy. It is a great way to see your hosts side-by-side in both platforms before you take on the broader APM migration.
{{% /notice %}}
