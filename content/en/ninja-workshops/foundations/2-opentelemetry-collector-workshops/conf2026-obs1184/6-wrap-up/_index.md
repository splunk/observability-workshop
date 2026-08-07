---
title: 6. Wrap-up and take-home exercises
linkTitle: 6. Take-home exercises
weight: 9
time: 3 minutes
---

![Well done](../images/welldone.png)

You used Config Builder to filter noisy spans, protect sensitive attributes,
and transform logs. You then applied the completed configuration and verified
the results. If you enabled cloud export, you also found traces and metrics in
Splunk Observability Cloud.

## Take-home exercises

{{% expand title="Send logs to Splunk Platform" %}}

A Splunk Observability Cloud free organization does not include a Splunk
Platform HEC endpoint. Use a separate non-production Splunk Enterprise or
Splunk Cloud Platform environment.

1. Set `SPLUNK_HEC_URL` and `SPLUNK_HEC_TOKEN` for your non-production Splunk
   Platform instance. The configuration already defines the
   [`splunk_hec` exporter](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/collector-components/exporters/splunk-hec-exporter).
2. The default `logs` pipeline already uses `splunk_hec` and
   `splunk_hec/profiling`. After setting the HEC environment variables, send an
   OTLP or Fluent Forward log. To reuse the quote exercise, add the existing
   `file_log/quotes` receiver and `transform` processor to that pipeline.
3. If your environments meet the requirements, configure
   [Splunk Log Observer Connect](https://help.splunk.com/splunk-observability-cloud/manage-data/view-splunk-platform-logs/introduction-to-splunk-log-observer-connect)
   to investigate logs alongside metrics and traces.

Use only non-production credentials and data for this exercise.

{{% /expand %}}

{{% expand title="Add AlwaysOn Profiling" %}}

Instrument a supported application and follow
[Get data into Splunk APM AlwaysOn Profiling](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/alwayson-profiling/get-data-into-splunk-apm-alwayson-profiling).

{{% /expand %}}

{{% expand title="Strengthen the trace policy" %}}

- Add an Amex pattern and repeat the redaction test. See the
  [Redaction Processor documentation](https://help.splunk.com/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/collector-components/processors/redaction-processor).
- Add another precise noisy-span condition. See the
  [Filter Processor documentation](https://help.splunk.com/en/splunk-observability-cloud/manage-data/manage-sensitive-data/sanitize-data-with-opentelemetry-collector-processors/filter-processor).

{{% /expand %}}

{{% notice title="Keep your Config Builder result" style="note" %}}
Save the final `agent_config.yaml` without secrets. Before you use it outside
the workshop, review component support, credentials, network access, processor
order, and data volume.
{{% /notice %}}
