---
title: "Phase 4: Standalone Splunk OpenTelemetry Collector"
linkTitle: 5. Standalone OTel Collector
weight: 5
archetype: chapter
time: 15 minutes
description: Take the same workshop collector config you used in Phase 3 and run it under the standalone Splunk OpenTelemetry Collector install. Get every environment variable, the Smart Agent monitor bundle, and `systemd`-managed lifecycle for free, and move one step closer to an OTel-native footprint.
---

In the previous phase you proved you can run the workshop collector config inside the AppDynamics machine agent. You also tallied the cost: eight environment variables in your shell, a Smart Agent receiver that does nothing because the bundle is not on disk, and an OTel collector lifecycle glued to the AppD machine agent's process.

This phase swaps the runtime substrate underneath. The same workshop `collector-config.yaml` runs under the **standalone Splunk Distribution of the OpenTelemetry Collector**, installed via the official install script. The config is unchanged. The Java app stays in dual mode. The transitions are all operational.

Here is what changes:

| Aspect | Phase 3 (bundled collector path) | Phase 4 (standalone install) |
|---|---|---|
| Where the OTel binary lives | `~/workshop/appd/machine-agent/otel-collector/bin/otelcol_linux_amd64` | `/usr/lib/splunk-otel-collector/bin/otelcol` |
| Who starts it | The AppDynamics machine agent launcher | `systemd` |
| Config location | `~/workshop/appd/machine-agent/conf/otel/agent_config.yaml` (inside the AppD install tree, can be overwritten on AppD upgrade) | `/etc/otel/collector/agent_config.yaml` (independent of AppD) |
| Env vars | Manually exported in your shell | Written once into `/etc/otel/collector/splunk-otel-collector.conf` by the install script |
| Smart Agent monitor bundle | Not present, `smartagent/processlist` silently does nothing | Shipped at `/usr/lib/splunk-otel-collector/agent-bundle`, `smartagent/processlist` works |
| Lifecycle | Stops when the machine agent stops | `systemctl restart splunk-otel-collector` independent of AppD |
| Update cadence | Tracks AppD machine agent releases | Tracks the Splunk OTel Collector release cadence |
| Diagnosis | `tail -f machine-agent/logs/otel/otel-collector.log` | `journalctl -u splunk-otel-collector -f` |
| AlwaysOn Profiling and call graphs | Bundled config has no logs pipeline; would need additional manual setup | Workshop config already includes the `splunk_hec/profiling` exporter |

In this phase you will:

1. Disable the bundled OTel side of the AppDynamics machine agent (set `SPLUNK_OTEL_ENABLED=false`) so the bundled collector stops, while the machine agent keeps reporting infrastructure to AppDynamics Server Visibility.
2. Install the standalone Splunk OTel Collector with the official script and apply the same workshop `collector-config.yaml` you used in Phase 3.
3. Verify that APM traces, host metrics, and the Smart Agent process list all flow under the new substrate, and check what was painful in Phase 3 is now handled by the install.

{{% notice title="Why would we keep the AppDynamics machine agent running?" style="info" icon="info-circle" %}}
When you still require **AppDynamics Server Visibility** to receive host metrics for the AppD side of dual signal. The machine agent process is what feeds Server Visibility. We just turn off its bundled OTel side so the standalone collector owns the OTel pipeline cleanly. But in the future the agent could be fully removed from the system.
{{% /notice %}}

{{% notice title="Skipped Phase 3" style="info" icon="info-circle" %}}
If you came here directly from Phase 2 without doing Phase 3 (not using the AppD Machine Agent), the Java app is still in single signal mode and only sending to AppDynamics. After you finish the install steps below, restart the Java app with the dual mode flags shown in [Phase 3 Step 2](../4-customize-bundled-collector/2-enable-dual-mode/) so it begins emitting OTLP into the new collector.
{{% /notice %}}

This is the configuration we recommend for production observability and the natural next step on the path toward dropping the AppDynamics agent entirely and running an OTel-native footprint when you are ready.
