---
title: 1.5 Validate Splunk Observability Cloud
linkTitle: 1.5 Cloud Validation
weight: 5
---

This optional step confirms that the trace and metrics exporters can reach the
Splunk Observability Cloud organization configured during setup.

{{% notice title="Skip conditions" style="warning" %}}
Skip this step when setup did not enable cloud export. Local validation from
Steps 1.2 through 1.4 is sufficient.
{{% /notice %}}

{{% exercise title="Find workshop traces and host metrics" %}}

1. On the workshop host, confirm cloud mode was enabled:

   ```bash
   cd [WORKSHOP]/1-agent
   source ../workshop-env.sh
   echo "${CONF2026_CLOUD_ENABLED}"
   ```

   Continue only when the value is `true` and the Agent is running.

2. Generate another small trace sample from `[WORKSHOP]/1-agent`:

   ```bash
   ../loadgen -count 5
   ```

3. Read the detected host name from the local metrics output:

   ```bash
   jq -r '
     .resourceMetrics[].resource.attributes[]
     | select(.key == "host.name")
     | .value.stringValue
   ' agent-metrics.out | sort -u
   ```

4. In Splunk Observability Cloud, select **APM > Traces** (Trace Analyzer),
   choose a recent time range such as the last 15 minutes, and select **All
   traces**.
5. Filter for service `cinema-service` and operation `/movie-validator`.
   Open a returned trace and confirm its span attributes include the synthetic
   `user.*` fields and `otelcol.service.mode=agent`.
6. Select **Infrastructure > Hosts**. Locate the detected workshop host and
   open it.
   Confirm recent CPU data is present. If needed, open **Settings > Metric
   Metadata**, search for `host.name:<detected-host-name>`, and confirm a recent
   `system.cpu.time` data point.

Telemetry can take a short time to become searchable. If nothing appears,
first confirm the same data is present in the Agent console, then inspect the
console for `401`, DNS, TLS, or export errors and recheck the realm, endpoint,
and ingest-token scope in `workshop-env.sh`.

Seeing both the trace and host metrics confirms the `otlp_http` and `signalfx`
connections are working.

{{% /exercise %}}
