---
title: 1. Add the OBI Service
weight: 1
---

## Add OBI to docker-compose.yaml

{{% notice title="Exercise" style="green" icon="running" %}}

Open `docker-compose.yaml` in your editor:

``` bash
cd ~/workshop/obi/02-obi-docker
vi docker-compose.yaml
```

Scroll to the very bottom of the file -- you'll see a comment block that says `PHASE 2`. Paste the following block **directly below that comment**, keeping the **2-space indentation** so it lines up with the other services (like `frontend:`, `load-generator:`, etc.):

``` yaml
  obi:
    image: otel/ebpf-instrument:main
    pid: host
    privileged: true
    network_mode: host
    volumes:
      - ./obi-config.yaml:/config/obi-config.yaml
      - /sys/fs/cgroup:/sys/fs/cgroup
    environment:
      OTEL_EBPF_CONFIG_PATH: /config/obi-config.yaml
```

Save the file.

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Make sure `obi:` is indented 2 spaces (same level as `frontend:`, `load-generator:`, etc.). If it's at the far left with no indentation, Docker Compose will reject it with `Additional property obi is not allowed`. It must be **inside** the `services:` block.
{{% /notice %}}

### What Does Each Line Do?

| Line | What it does | Why it matters |
|---|---|---|
| `image: otel/ebpf-instrument:main` | The [OBI container image](https://hub.docker.com/r/otel/ebpf-instrument) | This is the only thing you're adding to your stack |
| `pid: host` | Shares the host's PID namespace | OBI needs to see processes running in **other** containers |
| `privileged: true` | Grants kernel-level access | eBPF programs need to attach probes to kernel functions |
| `network_mode: host` | Shares the host's network stack | Required for context propagation -- OBI injects trace context at the network level |
| `volumes: ./obi-config.yaml:...` | Mounts the service discovery config | Tells OBI which processes to instrument and what to name them |
| `volumes: /sys/fs/cgroup:...` | Mounts the cgroup filesystem | OBI uses this to detect which processes are running inside containers |
| `OTEL_EBPF_CONFIG_PATH` | Points to the config file inside the container | Standard OBI env var for configuration |

## Start OBI

Docker Compose will detect that only the `obi` service is new and start it. Your existing services keep running.

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker compose up -d
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
[+] Running 6/6
 ✔ Container 02-obi-docker-payment-service-1      Running
 ✔ Container 02-obi-docker-order-processor-1       Running
 ✔ Container 02-obi-docker-frontend-1              Running
 ✔ Container 02-obi-docker-splunk-otel-collector-1 Running
 ✔ Container 02-obi-docker-load-generator-1        Running
 ✔ Container 02-obi-docker-obi-1                   Started
```

{{% /tab %}}
{{< /tabs >}}
