---
title: 2. Install the Splunk OTel Collector
weight: 2
---

The Java app from Phase 3 is still emitting OpenTelemetry traces over OTLP to `localhost:4318`. This step puts a real collector behind that endpoint, on its own `systemd` service, and applies the same workshop `collector-config.yaml` you used in Phase 3.

## Install the Splunk OpenTelemetry Collector

Run the Splunk OTel Collector install script. This installs the collector as a `systemd` service and ships the Smart Agent monitor bundle that was missing in Phase 3:

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

The default collector config the install script writes is general-purpose. Replace it with the same `~/workshop/appd/collector-config.yaml` you used in Phase 3. The processors below are why the workshop ships its own config in the first place:

We will copy the custom config we used previously in the workshop over the `agent_config.yaml` to verify we are comparing apples to apples with our previous agent:

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

Lets check out an important element in the custom config we used in both phases of our workshop. The processors below help us maintain telemetry cleanliness when ingesting into the backend:

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

## Set the Collector Environment Variables

In Phase 3 you exported these variables in your shell every time you started the machine agent. The standalone install reads them from `/etc/otel/collector/splunk-otel-collector.conf` instead. Write them once and `systemd` carries them across reboots and restarts:

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
