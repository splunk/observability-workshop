---
title: 2. Instrument with OBI
weight: 2
---

Now add APM tracing to this running app **without touching a single line of code**.

## Download OBI

Download the pre-built OBI binary from the [GitHub releases page](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases):

{{< tabs >}}
{{% tab title="Script" %}}

```bash
VERSION=0.6.0
ARCH=amd64
wget "https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/download/v$VERSION/obi-v$VERSION-linux-$ARCH.tar.gz"
wget "https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/releases/download/v$VERSION/SHA256SUMS"
sha256sum -c SHA256SUMS --ignore-missing
tar -xzf "obi-v$VERSION-linux-$ARCH.tar.gz"
ls -la ./obi
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
obi-v0.6.0-linux-amd64.tar.gz: OK
-rwxr-xr-x 1 splunk splunk 112345678 Feb 27 14:47 ./obi
```

{{% /tab %}}
{{< /tabs >}}

## Run OBI

{{% notice title="Exercise" style="green" icon="running" %}}

In a **separate terminal**, run OBI with `sudo`. Replace the three placeholders with your realm, token, and hostname from the previous step (this may take a minute or two to complete):

{{< tabs >}}
{{% tab title="Script" %}}

```bash
cd ~/workshop/obi/01-obi-python

sudo env \
  OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://ingest.${REALM}.signalfx.com:443" \
  OTEL_EXPORTER_OTLP_TRACES_PROTOCOL="grpc" \
  OTEL_EXPORTER_OTLP_HEADERS="X-SF-Token=${ACCESS_TOKEN}" \
  OTEL_SERVICE_NAME="warmup-app" \
  OTEL_RESOURCE_ATTRIBUTES="deployment.environment=ebpf-bare-app,host.name=${INSTANCE}" \
  OTEL_EBPF_OPEN_PORT=5150 \
  ./obi
```

{{% /tab %}}
{{% tab title="Look for this in your Output" %}}
Generate traffic and look for this output

```text
...
time=2026-02-27T19:29:56.296Z level=INFO msg="instrumenting process" component=discover.traceAttacher cmd=/usr/bin/python3.10 pid=245031 ino=7094 type=python service=warmup-app logenricher=false
...
time=2026-02-27T19:29:58.278Z level=INFO msg="Launching p.Tracer" component=generic.Tracer
```

{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

### What Do These Variables Do?

| Variable | Purpose |
|---|---|
| `sudo` | eBPF probes require root/kernel access |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Full URL for Splunk's OTLP trace ingest. The per-signal env var sends to this URL exactly the base `OTEL_EXPORTER_OTLP_ENDPOINT` would append `/v1/traces` which doesn't match Splunk's path |
| `OTEL_EXPORTER_OTLP_HEADERS` | Auth header for Splunk |
| `OTEL_SERVICE_NAME` | The service name that appears in Splunk APM |
| `OTEL_RESOURCE_ATTRIBUTES` | Sets `deployment.environment` and `host.name` on every trace so you can filter to your data |
| `OTEL_EBPF_OPEN_PORT` | Tells OBI to instrument the process listening on port 5150 |

{{% notice title="Note" style="info" %}}
You may see warnings like `failed to upload metrics: 404 Not Found` in the OBI logs. This is expected Splunk's direct ingest doesn't have a standard OTLP metrics endpoint. The traces still export correctly. In Phase 2, a collector handles both traces and metrics properly.
{{% /notice %}}

## Generate Traffic

Go back to your first terminal and generate some requests:

```bash
for i in $(seq 1 20); do curl -s "http://localhost:5150/hello"; sleep 1; done
```
***NOTE:*** If you get a 404 error double check that there is no `\` appended to the url you are curling. In some termings the `;` will attempt to escape and cause an invalid url

