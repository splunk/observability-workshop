---
title: Prerequisites
linkTitle: 01. Prerequisites
weight: 1
time: 5 minutes
description: Goals and architecture for the workshop.
---

# Prerequisites

Before starting this workshop, ensure you have the following tools installed and a Splunk Observability Cloud account ready.

---

## Knowledge prerequisites

This workshop assumes familiarity with:

- Basic Kubernetes concepts (pods, deployments, services)
- HTTP request/response flow
- The idea of distributed tracing (spans, trace IDs)

No prior OpenTelemetry experience is required - we'll explain context propagation as we go.

---

## Required software

Install these tools on your workstation:

| Tool | Minimum version | Verify |
|------|-----------------|--------|
| [Docker](https://docs.docker.com/get-docker/) | 24.x | `docker --version` |
| [kubectl](https://kubernetes.io/docs/tasks/tools/) | 1.28+ | `kubectl version --client` |
| [k3d](https://k3d.io/) | 5.6+ | `k3d version` |
| [Helm](https://helm.sh/docs/intro/install/) | 3.12+ | `helm version` |
| [Node.js](https://nodejs.org/) (optional, for local dev) | 20.x | `node --version` |
| [Git](https://git-scm.com/) | 2.x | `git --version` |

---

## Splunk Observability Cloud access

You'll need access to a Splunk Observability Cloud org with permission to:

1. **Create an org access token** — used by the OTel Collector and APM agents
2. **Create a RUM access token** — used by the browser agent (public token)
3. **View APM traces** — APM → Traces
4. **View RUM sessions** — RUM → Sessions

### Gather these values before step 2

| Variable | Where to find it |
|----------|------------------|
| `SPLUNK_REALM` | Your org URL, e.g. `us0` from `https://app.us0.signalfx.com` |
| `SPLUNK_ACCESS_TOKEN` | Settings → Access Tokens → Create Token (Ingest scope) |
| `SPLUNK_RUM_ACCESS_TOKEN` | Data Management → RUM → Create RUM access token |                            /api/email/send-confirmation

```
## Validation checklist

Run these commands from your assigned instance before continuing. Each section includes expected output so you can confirm you're ready.

### 1. Verify required tools
**Expected output (versions may vary):**

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker --version
kubectl version --client
k3d version
helm version --short
git --version
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Docker version 27.4.0, build bde2b89
Client Version: v1.31.0
k3d version v5.7.4
v3.16.2+gf786678
git version 2.47.0
```

{{% /tab %}}
{{< /tabs >}}

### 2. Confirm required ports are free

{{< tabs >}}
{{% tab title="Script" %}}

```bash
lsof -i :30080 -i :5111 -i :15672 2>/dev/null || echo "Ports 30080, 5111, and 15672 are available"
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
Ports 30080, 5111, and 15672 are available
```

**If a port is in use:** Note the process name in the output and stop it, or edit `scripts/setup-k3d.sh` to use different ports.

{{% /tab %}}
{{< /tabs >}}

### 3. Confirm project directory

{{< tabs >}}
{{% tab title="Script" %}}

```bash
ls workshop/index.md docker-compose.yml .env.example Makefile
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` text
.env.example
docker-compose.yml
Makefile
workshop/index.md
```

{{% /tab %}}
{{< /tabs >}}

---
