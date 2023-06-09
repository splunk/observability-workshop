---
title: OpenTelemetry Collector Exporters
linkTitle: 5. Exporters
weight: 5
---

An exporter, which can be push or pull based, is how you send data to one or more backends/destinations. Exporters may support one or more data sources.

For this workshop we will be using the **otlphttp** exporter. The OpenTelemetry Protocol (OTLP) is a vendor-neutral, standardised protocol for transmitting telemetry data. The OTLP exporter sends data to a server that implements the OTLP protocol. The OTLP exporter supports both gRPC and HTTP/JSON protocols.

In order to send metrics over HTTP to Splunk Observability Cloud we will need to configure the **otlphttp** exporter.

Let's edit our `/etc/otelcontribcol/config.yaml` file and configure the **otlphttp** exporter. Insert the following YAML under the **exporters** section, taking care to indent by two spaces e.g.

We will also change the verbosity of the logging exporter to prevent the disk filling up. The default of `detailed` is very noisy.

```yaml {hl_lines=["3-4"]}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
```

Next we need to define the `metrics_endpoint` and configure the target URL. For Splunk Observerability Cloud the URL is `https://ingest.eu0.signalfx.com/v2/datapoint/otlp`.

The **otlphttp** exporter can also be configured to also send traces and logs by defining target URL for `traces_endpoint` and `logs_endpoint` respectively.

```yaml {hl_lines=["5"]}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.eu0.signalfx.com/v2/datapoint/otlp
```

By default `gzip` compression is enabled for all endpoints, this can be disabled by setting `compression: none` in the exporter configuration. We will leave compression enabled for this workshop and accept the default as this is the most efficient way to send data.

In order to send metrics to Splunk Observability Cloud we need to define a token. This can be done by creating a new token in the Splunk Observability Cloud UI. For more information on how to create a token, see [Create a token](https://docs.splunk.com/Observability/admin/authentication-tokens/org-tokens.html). The token needs to be of type **INGEST**.

The token can then be added to the configuration file by defining a _key_ named `X-SF-TOKEN` and a _value_ of the token created above under `headers` section:

```yaml {hl_lines=["6-8"]}
exporters:
  logging:
    verbosity: normal
  otlphttp/splunk:
    metrics_endpoint: https://ingest.eu0.signalfx.com/v2/datapoint/otlp
    headers:
      X-SF-TOKEN: <redacted>
```

Of course, you could easily configure the `metrics_endpoint` to point to any other solution that supports the **OTLP** protocol.
