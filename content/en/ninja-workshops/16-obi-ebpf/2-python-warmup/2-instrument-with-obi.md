---
title: 2. Instrument with OBI
weight: 2
---

Now add APM tracing to this running app **without touching a single line of code**.

## Extract the OBI Binary

OBI doesn't have a standalone download yet, so we extract the binary from the Docker image:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
IMAGE=otel/ebpf-instrument:main
sudo docker pull $IMAGE
ID=$(sudo docker create $IMAGE)
sudo docker cp "$ID:/obi" ./obi
sudo docker rm -v $ID
ls -la ./obi
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
main: Pulling from otel/ebpf-instrument
...
Status: Downloaded newer image for otel/ebpf-instrument:main
-rwxr-xr-x 1 root root 47234560 ... ./obi
```

{{% /tab %}}
{{< /tabs >}}

## Run OBI

{{% notice title="Exercise" style="green" icon="running" %}}

In a **separate terminal**, run OBI with `sudo`. Replace the three placeholders with your realm, token, and hostname from the previous step:

``` bash
sudo OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="https://ingest.<YOUR_REALM>.signalfx.com/v2/trace/otlp" \
     OTEL_EXPORTER_OTLP_HEADERS="X-SF-Token=<YOUR_TOKEN>" \
     OTEL_SERVICE_NAME="warmup-app" \
     OTEL_RESOURCE_ATTRIBUTES="deployment.environment=ebpf-bare-app,host.name=<YOUR_NAME>" \
     OTEL_EBPF_OPEN_PORT=5150 \
     ./obi
```

{{% /notice %}}

### What Do These Variables Do?

| Variable | Purpose |
|---|---|
| `sudo` | eBPF probes require root/kernel access |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | Full URL for Splunk's OTLP trace ingest. The per-signal env var sends to this URL exactly -- the base `OTEL_EXPORTER_OTLP_ENDPOINT` would append `/v1/traces` which doesn't match Splunk's path |
| `OTEL_EXPORTER_OTLP_HEADERS` | Auth header for Splunk |
| `OTEL_SERVICE_NAME` | The service name that appears in Splunk APM |
| `OTEL_RESOURCE_ATTRIBUTES` | Sets `deployment.environment` and `host.name` on every trace so you can filter to your data |
| `OTEL_EBPF_OPEN_PORT` | Tells OBI to instrument the process listening on port 5150 |

{{% notice title="Note" style="info" %}}
You may see warnings like `failed to upload metrics: 404 Not Found` in the OBI logs. This is expected -- Splunk's direct ingest doesn't have a standard OTLP metrics endpoint. The traces still export correctly. In Phase 2, a collector handles both traces and metrics properly.
{{% /notice %}}

## Generate Traffic

Go back to your first terminal and generate some requests:

``` bash
for i in $(seq 1 20); do curl -s http://localhost:5150/hello; sleep 1; done
```
