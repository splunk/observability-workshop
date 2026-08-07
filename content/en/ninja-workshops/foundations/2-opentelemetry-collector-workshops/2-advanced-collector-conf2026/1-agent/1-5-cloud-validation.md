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

Steps 1.2 and 1.3 already generated the telemetry for this validation. When
cloud export is enabled, the Agent continuously sends host metrics and sends
the `/movie-validator` spans generated in Step 1.3. You do not need to run
`loadgen` again. The workshop logs generated in Step 1.4 are validated locally
and are not part of this cloud check.

1. In the **Command terminal**, confirm cloud mode was enabled:

   ```bash
   cd [WORKSHOP]/1-agent
   source ../workshop-env.sh
   echo "${CONF2026_CLOUD_ENABLED}"
   ```

   Continue only when the value is `true` and the Agent is running.

2. Print a ready-to-use Infrastructure Monitoring filter containing the exact
   host name detected by the Agent:

   ```bash
   jq -r '
     .resourceMetrics[].resource.attributes[]
     | select(.key == "host.name")
     | "host.name:\(.value.stringValue)"
   ' agent-metrics.out | sort -u
   ```

   Copy the resulting `host.name:<detected-host-name>` value. This is more
   reliable than assuming that the name shown by your shell matches the name
   selected by resource detection.

3. In Splunk Observability Cloud, select **APM > Traces** (Trace Analyzer),
   choose a recent time range such as the last 15 minutes, and select **All
   traces**.
4. Filter for service `cinema-service` and operation `/movie-validator`.
   Open a returned trace and confirm its span attributes include the synthetic
   `user.*` fields and `otelcol.service.mode=agent`.
5. Select **Infrastructure > Hosts**, choose a recent time range, and paste the
   `host.name:<detected-host-name>` value into the filter bar. Open the matching
   host and confirm recent CPU, memory, load, or network data is present.

Telemetry can take a short time to become searchable. If nothing appears,
confirm the trace and workshop CPU metrics are present locally. Then inspect
the Agent console for `401`, DNS, TLS, or export errors and recheck the realm,
endpoint, and access token's ingest authorization in `workshop-env.sh`.

Seeing both the trace and host metrics confirms the `otlp_http` and `signalfx`
connections are working.

{{% /exercise %}}
