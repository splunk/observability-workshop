---
title: 3. Deploy on a Local Laptop
weight: 3
---

Use this path when students want to run the workshop on a local Kubernetes runtime. The workshop includes scripts for `kind`, Minikube, and MicroK8s. Each path builds the app image, loads it into the local cluster, installs the Splunk OpenTelemetry Collector, and deploys the app.

{{% notice title="Exercise" style="green" icon="running" %}}

* Choose one local Kubernetes runtime:

| Runtime | Good fit | Script |
|---------|----------|--------|
| `kind` | Repeatable workshop clusters running in Docker. | `./scripts/deploy-local-kind.sh` |
| Minikube | Students already using Minikube locally. | `./scripts/deploy-local-minikube.sh` |
| MicroK8s | Linux workstations or VMs using Canonical MicroK8s. | `./scripts/deploy-local-microk8s.sh` |

* Confirm the tools for your selected runtime are available:

```bash
docker version
kubectl version --client
helm version
```

For `kind`:

```bash
kind version
```

For Minikube:

```bash
minikube version
```

For MicroK8s:

```bash
microk8s status --wait-ready
microk8s kubectl version --client
microk8s helm3 version
```

* Set your Splunk Observability Cloud realm and access token:

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<your-access-token>
```

* Deploy the local lab with your selected runtime.

For `kind`:

```bash
cd workshop/ai-troubleshooting-remediation
./ai-remediation deploy kind
```

For Minikube:

```bash
cd workshop/ai-troubleshooting-remediation
./ai-remediation deploy minikube
```

For MicroK8s:

```bash
cd workshop/ai-troubleshooting-remediation
./ai-remediation deploy microk8s
```

* Confirm the app is running:

```bash
kubectl -n ai-remediation get pods
```

For MicroK8s, use:

```bash
microk8s kubectl -n ai-remediation get pods
```

Expected pods:

```text
checkout-service-...
inventory-service-...
remediation-loadgen-...
```

* Send a quick smoke test:

```bash
./ai-remediation smoke <runtime>
```

Replace `<runtime>` with `kind`, `minikube`, or `microk8s`.

{{< tabs >}}
{{% tab title="Question" %}}
**What do the local scripts do differently from a normal cloud deployment?**
{{% /tab %}}
{{% tab title="Answer" %}}
**They build the Docker image locally and load it into the selected local cluster instead of pushing the image to a remote registry.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Local Laptop Notes" style="info" %}}
If a student already has a Kubernetes cluster in Docker Desktop, Rancher Desktop, or OrbStack, they can still use the cloud deployment path with a registry. The `kind` path is the most repeatable local option, Minikube is common for individual developers, and MicroK8s is a good fit for Linux laptops or workshop VMs.
{{% /notice %}}
