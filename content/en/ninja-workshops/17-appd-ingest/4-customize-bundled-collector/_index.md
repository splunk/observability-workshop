---
title: "Phase 3: Customize the Bundled Collector"
linkTitle: 4. Customize Bundled Collector
weight: 4
archetype: chapter
time: 15 minutes
description: Reuse the OTel binary already inside the AppDynamics machine agent by overwriting its config with the full workshop collector config. Get APM, traces, and host metrics in Splunk Observability Cloud through the same process the AppD launcher manages, and see exactly what that costs in environment variables and missing pieces.
---

Phase 2 turned on the bundled OTel collector with the default `agent_config.yaml` AppDynamics ships. That gave you host metrics in Splunk Observability Cloud through one environment variable, but you stopped short of APM, profiling, and the rest of the pipeline set you would normally run in production.

You do not need to install anything else to get those. The OTel binary AppD ships at `otel-collector/bin/otelcol_linux_amd64` is the **Splunk Distribution of the OpenTelemetry Collector** the same binary you would install standalone in Phase 4. It will run any config you point it at. So in this phase you point it at the workshop's full `collector-config.yaml`.
- **NOTE:** The packaged version of the collector in the AppD Machine Agent does not follow the Splunk release cadence for new Collector binaries

So why don't we just run the Machine Agent all the time? The AppDynamics launcher only knows about the env vars the bundled config needs (`SPLUNK_OTEL_ENABLED`, `SPLUNK_ACCESS_TOKEN`, `SPLUNK_REALM`) and only contains a configuration for infrastructure metrics.  
To get the rest of our data into Splunk our config needs to reference a great deal more OpenTelemetry configuration. We will wire all of that up  and you will see exactly how much "by hand" work is required.

In this phase you will:

1. Stop the bundled collector, drop the workshop `collector-config.yaml` into the AppD install in place of `agent_config.yaml`, and export the additional environment variables the workshop config needs.
2. Restart the machine agent so the bundled collector comes back up running the workshop config.
3. Enable dual signal mode on the Java agent so APM traces flow into the bundled collector on `localhost:4318`.
4. Verify that APM, host metrics, and the AppDynamics correlation attributes all reach Splunk Observability Cloud.
5. Tally the friction the env vars you had to remember, the smart agent components that silently do nothing, and the lifecycle coupling between the AppD machine agent and the OTel collector.

Phase 4 then takes the same workshop config, runs it through the official Splunk OTel Collector install script, and you watch the friction disappear. That is the natural next step on the path toward an OTel-native instrumentation footprint.

{{% notice title="Why bother showing this path at all" style="info" icon="info-circle" %}}
Some teams genuinely run this way. They do not want a second OTel process on the host, or they want to keep all telemetry plumbing inside something the AppDynamics admin already operates. The path works for metrics and traces. Walking it once makes it obvious why we recommend the standalone install for everything else.
{{% /notice %}}
