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
0f5fbf7fdc05: Pull complete
c9d0c8eb6b20: Pull complete
05db807c0ef0: Pull complete
9414859de0f9: Pull complete
04083a69ab27: Pull complete
Digest: sha256:f1b61af237c7ec02ea83afb7108ec8d65f3e308f9501818a15b67983f243cf97
Status: Downloaded newer image for otel/ebpf-instrument:main
docker.io/otel/ebpf-instrument:main
Successfully copied 108MB to /home/splunk/workshop/obi/01-obi-python/obi
baa799720f42deaeeeb7690a39b91a5ae16f71ec33833d8a963808f14109ea0f
-rwxr-xr-x 1 root root 107922836 Feb 27 14:47 ./obi
```

{{% /tab %}}
{{< /tabs >}}

## Run OBI

{{% notice title="Exercise" style="green" icon="running" %}}

In a **separate terminal**, run OBI with `sudo`. Replace the three placeholders with your realm, token, and hostname from the previous step:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
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
``` text
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
