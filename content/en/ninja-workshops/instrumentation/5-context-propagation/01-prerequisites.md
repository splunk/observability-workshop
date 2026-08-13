---
title: Prerequisites
linkTitle: 01. Prerequisites
weight: 1
time: 5 minutes

---

Before starting this workshop, ensure you have the following tools installed and have a Splunk Observability Cloud account ready.

## Knowledge Requirement

This workshop assumes familiarity with:

- Basic Kubernetes concepts (pods, deployments, services)
- HTTP request/response flow
- The idea of distributed tracing (spans, traces...)

OpenTelemetry experience is required - we'll explain context propagation challenges as we go.

## Required Software

These tools will already be installed on your instance:

| Tool | Minimum version | Verify |
|------|-----------------|--------|
| [Docker](https://docs.docker.com/get-docker/) | 24.x | `docker --version` |
| [kubectl](https://kubernetes.io/docs/tasks/tools/) | 1.28+ | `kubectl version --client` |
| [k3d](https://k3d.io/) | 5.6+ | `k3d version` |
| [Git](https://git-scm.com/) | 2.x | `git --version` |
| [Helm](https://helm.sh/docs/intro/install/) | 3.12+ | `helm version` |
| [Node.js](https://nodejs.org/) (optional) | 20.x | `node --version` |


## Splunk Observability Access

You'll need access to a Splunk Observability Cloud org with permission to:

1. **View APM traces** - APM → Service Map & APM → Traces
2. **View RUM sessions** - Digital Experience → Session Search
3. **[Optional] Gather Realm & Token Details** - NOTE: These values are configured in your instance and detail are provided in the next step.

{{% notice title="Note" style="info" %}}
This Workshop uses the Splunk4Ninjas - Observability template.
Your instructor will provide you with all the required login credentials and environment details
{{% /notice %}}

## Validation Checklist

Run these commands from your assigned instance before continuing. Each section includes expected output so you can confirm you're ready.

#### 1. Verify required tools

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
Docker version 29.1.3, build 29.1.3-0ubuntu3~22.04.2
Client Version: v1.34.1
Kustomize Version: v5.7.1
k3d version v5.9.0
k3s version v1.35.5-k3s1 (default)
v3.21.3+g1ad6e68
git version 2.34.1
```

{{% /tab %}}
{{< /tabs >}}

#### 2. Confirm required ports are free

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

