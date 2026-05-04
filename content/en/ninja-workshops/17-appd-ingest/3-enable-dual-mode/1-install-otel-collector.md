---
title: 1. Install the OTel Collector
weight: 1
---

The AppDynamics agent in dual mode emits OpenTelemetry data over OTLP. You need a collector on the same host to receive that data and forward it to Splunk Observability Cloud.

## Verify Environment Variables

Your instance should have these variables pre-set. Confirm they are available with `env` or:

```bash
echo "REALM=$REALM"
echo "ACCESS_TOKEN=$ACCESS_TOKEN"
echo "INSTANCE=$INSTANCE"
```

All three should have values. If any are empty, check with your instructor.

## Install the Splunk OpenTelemetry Collector

Run the Splunk OTel Collector install script. This installs the collector as a `systemd` service:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh && \
  sudo sh /tmp/splunk-otel-collector.sh --realm $REALM -- $ACCESS_TOKEN
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
Splunk OpenTelemetry Collector has been successfully installed.
```

{{% /tab %}}
{{< /tabs >}}

## Apply the Workshop Collector Configuration

The default collector config is general-purpose. We will replace it with the workshop-specific config that receives OTLP from the AppDynamics agent and exports to Splunk Observability Cloud. But first lets take a look at what we're adding:

```bash
vim ~/workshop/appd/collector-config.yaml
```

look for this section under `processors:`:
{{< tabs >}}
{{% tab title="collector-config.yaml" %}}

```yaml
  resource/workshop:
    attributes:
      - key: host.name
        value: "${INSTANCE}"
        action: upsert
      - key: deployment.environment
        value: "${INSTANCE}-appd-dual"
        action: upsert 
      - key: deployment.environment.name
        value: "${INSTANCE}-appd-dual"
        action: upsert

  transform/drop_dims_high_cardinality:
      error_mode: ignore
      metric_statements:
        - context: resource
          conditions:
            - Len(resource.attributes) + Len(attributes) > 34
          statements:
            # Delete from datapoint attributes (where the Java agent puts them)
            - delete_key(attributes, "process.command_args") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.executable.path") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.runtime.description") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.runtime.name") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.runtime.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "process.pid") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "os.description") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "os.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "host.arch") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "host.image.id") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.distro.name") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.distro.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.sdk.version") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.sdk.name") where Len(resource.attributes) + Len(attributes) >= 34
            - delete_key(attributes, "telemetry.sdk.language") where Len(resource.attributes) + Len(attributes) >= 34

            # Add marker
            - set(resource.attributes["cardinality.trimmed"], "true")
```

{{% /tab %}}
{{% /tabs %}}

These processors make sure we correctly reference our variables for the `host.name` and `deployment.enviroment`/`deployment.environment.name`(preferred) attributes.

The `transform/drop_dims_high_cardinality` processor uses [OpenTelemetry Transformation Language (OTTL)](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/LANGUAGE.md) to check our metrics for any that have more than 34 attributes (the actual value attached to the metric counts as a point also).

- **IMPORTANT: Currently we will drop metrics that have too many attributes (>36) in the backend.** This can happen with AppDynamics telemetry due to additional attributes.

In our `transform` config we are checking if a metric is over 34 combined attributes and if so we progressively delete some attributes that may be of lesser value.  
Finally we do a check for available space afterwards to add a dimension for `cardinality.trimmed` so we can easily identify metrics that had dropped attributes.

Each of these processors is included at the end of the `pipeline:` for metrics in our configuration.

We will then copy that custom config over the `agent_config.yaml`:

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## Set the Collector Environment Variables

The collector service reads environment variables from a config file. The Splunk OTel Collector binary requires `SPLUNK_REALM` and `SPLUNK_ACCESS_TOKEN` (with the `SPLUNK_` prefix). Your instance has `REALM` and `ACCESS_TOKEN`, so we map them:

```bash
sudo bash -c "cat > /etc/otel/collector/splunk-otel-collector.conf << EOF
INSTANCE=${INSTANCE}
SPLUNK_INGEST_URL=https://ingest.${REALM}.signalfx.com
SPLUNK_CONFIG=/etc/otel/collector/agent_config.yaml
SPLUNK_ACCESS_TOKEN=${ACCESS_TOKEN}
SPLUNK_REALM=${REALM}
SPLUNK_API_URL=https://api.${REALM}.signalfx.com
SPLUNK_HEC_TOKEN=${HEC_TOKEN}
SPLUNK_HEC_URL=${HEC_URL}
SPLUNK_MEMORY_TOTAL_MIB=512
SPLUNK_BUNDLE_DIR=/usr/lib/splunk-otel-collector/agent-bundle
SPLUNK_COLLECTD_DIR=/usr/lib/splunk-otel-collector/agent-bundle/run/collectd
EOF"
```

## Restart the Collector

Restart to pick up the new configuration:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
sudo systemctl restart splunk-otel-collector
```

{{% /tab %}}
{{< /tabs >}}

## Verify the Collector is Running

{{< tabs >}}
{{% tab title="Command" %}}

```bash
sudo systemctl status splunk-otel-collector --no-pager
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
● splunk-otel-collector.service - Splunk OpenTelemetry Collector
     Loaded: loaded (/lib/systemd/system/splunk-otel-collector.service; enabled)
     Active: active (running) since ...
```

{{% /tab %}}
{{< /tabs >}}

Verify the health endpoint:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -s http://localhost:13133/ | jq
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-47-33 ~/workshop/appd $ curl -s http://localhost:13133/ | jq
{
  "status": "Server available",
  "upSince": "2026-05-04T16:02:29.509202038Z",
  "uptime": "30.174963775s"
}
```

{{% /tab %}}
{{< /tabs >}}

The collector is now listening for OTLP on ports **4317** (gRPC) and **4318** (HTTP).
