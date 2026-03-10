---
title: 1. Install the OTel Collector
weight: 1
---

The AppDynamics agent in dual mode emits OpenTelemetry data over OTLP. You need a collector on the same host to receive that data and forward it to Splunk Observability Cloud.

## Verify Environment Variables

Your instance should have these variables pre-set. Confirm they are available:

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

The default collector config is general-purpose. Replace it with the workshop-specific config that receives OTLP from the AppDynamics agent and exports to Splunk Observability Cloud:

```bash
sudo cp ~/workshop/appd/collector-config.yaml /etc/otel/collector/agent_config.yaml
```

## Set the Collector Environment Variables

The collector service reads environment variables from a config file. The Splunk OTel Collector binary requires `SPLUNK_REALM` and `SPLUNK_ACCESS_TOKEN` (with the `SPLUNK_` prefix). Your instance has `REALM` and `ACCESS_TOKEN`, so we map them:

```bash
sudo bash -c "cat > /etc/otel/collector/splunk-otel-collector.conf << EOF
SPLUNK_REALM=${REALM}
SPLUNK_ACCESS_TOKEN=${ACCESS_TOKEN}
INSTANCE=${INSTANCE}
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
curl -s http://localhost:13133/
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-77-108 ~/workshop/appd $ curl -s http://localhost:13133/
{"status":"Server available","upSince":"2026-03-09T21:25:53.277371609Z","uptime":"22.684480311s"}%
```

{{% /tab %}}
{{< /tabs >}}

The collector is now listening for OTLP on ports **4317** (gRPC) and **4318** (HTTP).
