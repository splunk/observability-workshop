---
title: Wrap Up
linkTitle: 5. Wrap Up
weight: 5
archetype: chapter
time: 5 minutes
description: Summary, cleanup, and next steps.
---

## What You Accomplished

In this workshop you:

1. **Built and ran a Java service with normal AppDynamics instrumentation**: a single agent sending APM data to the AppDynamics Controller only.

2. **Learned the difference between hybrid and dual signal mode**: hybrid reuses AppD's own instrumentation to generate OTel spans (lower overhead, narrower coverage), while dual runs the full OTel Java auto-instrumentation alongside AppD (broader coverage, adds correlation attributes).

3. **Enabled dual signal mode**: by adding four JVM flags to the same process. No code changes, no second agent, no recompilation. The same AppDynamics agent now sends data to both AppDynamics and Splunk Observability Cloud simultaneously.

4. **Created a global data link**: in Splunk Observability Cloud that uses the `appd.*` span attributes to navigate directly to the corresponding AppDynamics tier view.

## Cleanup

Stop the application and load generator:

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app
```

Optionally stop the collector:

```bash
sudo systemctl stop splunk-otel-collector
```

## Key Takeaways

- **Dual mode is a configuration change, not a code change.** You enabled it by adding JVM flags to an already-instrumented application. This makes it practical to roll out across an organization without touching application code.

- **The `appd.*` correlation attributes are what make the integration valuable.** Without them (hybrid mode), you get OTel traces in Splunk O11y but no way to link back to the specific AppDynamics business transaction, tier, or application. Dual mode provides that linkage.

- **Global data links turn correlation into workflow.** Instead of manually cross-referencing two tools, engineers can click from a Splunk O11y trace directly into the AppDynamics view 

- **This pattern supports gradual migration.** Organizations can run dual mode for a period to validate that Splunk Observability Cloud captures the same signal quality, then decide per-service whether to continue dual, switch to Splunk-only instrumentation, or stay with AppDynamics.

## Further Reading

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode) -- AppDynamics docs
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode) -- AppDynamics docs
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry) -- Supported framework list
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html) -- Splunk Observability docs
