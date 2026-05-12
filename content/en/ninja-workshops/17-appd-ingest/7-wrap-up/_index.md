---
title: Wrap Up
linkTitle: 7. Wrap Up
weight: 7
archetype: chapter
time: 5 minutes
description: Summary, cleanup, and next steps.
---

## What You Accomplished

You walked an AppDynamics shop through a four-step progression that gets progressively more capable and progressively closer to an OTel-native footprint:

1. **Phase 1: Built and ran a Java service with normal AppDynamics instrumentation.** A single Java agent sending APM data to the AppDynamics Controller. The starting point most AppDynamics customers run today.

2. **Phase 2: Added infrastructure dual signal with the AppDynamics Combined Machine Agent.** One environment variable (`SPLUNK_OTEL_ENABLED=true`) flipped the launcher into combined mode and the bundled OTel collector forwarded host metrics to Splunk Observability Cloud while the machine agent kept reporting to AppDynamics Server Visibility. The lowest-effort way to put hosts in both platforms.

3. **Phase 3: Customized the bundled collector with the workshop config and enabled dual signal mode on the Java agent.** You proved you can run a real production-ish OTel config inside the AppD machine agent's bundled collector and saw exactly what it costs: eight extra `SPLUNK_*` environment variables, a Smart Agent monitor bundle that is not on disk, and an OTel collector lifecycle glued to the AppDynamics machine agent.

4. **Phase 4: Replaced the bundled collector with the standalone Splunk OpenTelemetry Collector.** Same workshop config, but the install script wires every environment variable into `/etc/otel/collector/splunk-otel-collector.conf`, ships the Smart Agent bundle, and runs the collector as its own `systemd` service. Independent lifecycle, independent upgrade cadence, the configuration we recommend for production observability.

5. **Learned the difference between hybrid and dual signal mode on the Java agent.** Hybrid reuses AppD's own instrumentation to emit OTel spans (lower overhead, narrower coverage). Dual runs the full OTel Java auto-instrumentation alongside AppD (broader coverage, adds the `appd.*` correlation attributes that make the next step possible).

6. **Created a global data link** in Splunk Observability Cloud that uses the `appd.*` span attributes to navigate directly to the corresponding AppDynamics tier view.

## Cleanup

Stop the load generator, the Java app, the machine agent, and the standalone collector:

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app

cd ~/workshop/appd/machine-agent
kill "$(cat machine-agent.pid)" 2>/dev/null || true
rm -f machine-agent.pid

sudo systemctl stop splunk-otel-collector
sudo systemctl disable splunk-otel-collector
```

If you want to leave the bundled config swap in place for later experiments, restore the original AppD-shipped config:

```bash
cd ~/workshop/appd/machine-agent
cp conf/otel/agent_config.yaml.appd-default conf/otel/agent_config.yaml
```

## Key Takeaways

- **Dual mode is a configuration change, not a code change.** You enabled it by adding JVM flags to an already-instrumented application. This makes it practical to roll out across an organization without touching application code.

- **The AppD bundle is not the Splunk OTel Collector, but the binaries are interchangeable.** The OTel binary inside `~/workshop/appd/machine-agent/otel-collector/bin/otelcol_linux_amd64` is the Splunk Distribution. AppD packages and updates it on its own cadence and ships it with a metrics-only default config. You can absolutely point it at a richer config (Phase 3), but everything that the standalone install gives you for free becomes manual work.

- **The standalone Splunk OTel Collector is the configuration we ship to production.** Phase 4 demonstrated why: persistent env vars, the Smart Agent bundle on disk, `systemd`-managed lifecycle, and a release cadence Splunk controls. None of that is impossible to recreate inside the AppD bundle, but the cost piles up quickly.

- **The `appd.*` correlation attributes are what make the integration valuable.** Without them (hybrid mode), you get OTel traces in Splunk O11y but no way to link back to the specific AppDynamics business transaction, tier, or application. Dual mode provides that linkage.

- **Global data links turn correlation into workflow.** Engineers click from a Splunk O11y trace directly into the AppDynamics view instead of cross-referencing two tools by hand.

- **This pattern supports gradual migration toward OTel-native.** Run Phase 4 to validate that Splunk Observability Cloud captures the same signal quality. Then for new services, skip the AppDynamics agent entirely, use the OpenTelemetry Java SDK or auto-instrumentation, and let the standalone collector pick the data up unchanged. AppDynamics stays where it earns its place; everything else moves.

## Further Reading

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode) (AppDynamics docs)
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode) (AppDynamics docs)
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry) (Supported framework list)
- [Combined Agent for Infrastructure Visibility](https://help.splunk.com/en/appdynamics-on-premises/infrastructure-visibility/26.4.0/machine-agent/combined-agent-for-infrastructure-visibility) (AppDynamics docs for the bundled OTel collector)
- [Splunk Distribution of the OpenTelemetry Collector](https://docs.splunk.com/observability/en/gdi/opentelemetry/opentelemetry.html) (Splunk docs)
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html) (Splunk Observability docs)
