---
title: 3. Deploy in Cloud Kubernetes
weight: 3
---

Use this path when students have access to an existing Kubernetes cluster in a cloud provider or shared workshop environment. The app image must be pushed to a registry that the cluster can pull from.

{{% notice title="Exercise" style="green" icon="running" %}}

* Confirm your current Kubernetes context points to the intended non-production cluster:

```bash
kubectl config current-context
kubectl get nodes
```

* Set your Splunk Observability Cloud realm and access token:

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<your-access-token>
```

* Set a writable image registry path. Examples:

```bash
export IMAGE_REGISTRY=ghcr.io/<org-or-user>
export IMAGE_REGISTRY=<account-id>.dkr.ecr.<region>.amazonaws.com
export IMAGE_REGISTRY=<region>.gcr.io/<project-id>
```

* Optional: set an image tag and cluster name:

```bash
export IMAGE_TAG=<your-initials>
export CLUSTER_NAME=ai-remediation-cloud
export ENVIRONMENT=ai-remediation-workshop
```

* Deploy the cloud lab:

```bash
cd workshop/ai-troubleshooting-remediation
./scripts/deploy-cloud.sh
```

* Confirm the app is running:

```bash
kubectl -n ai-remediation get pods
kubectl -n ai-remediation get deploy
```

* Send a smoke test:

```bash
./scripts/smoke-test.sh
```

{{< tabs >}}
{{% tab title="Question" %}}
**What is the most common cloud deployment failure in this lab?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The cluster cannot pull the image because the registry path, image tag, authentication, or repository permissions are wrong. Check `kubectl describe pod` for `ImagePullBackOff` details.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Cloud Safety" style="info" %}}
Use a non-production cluster. The lab creates a namespace named `ai-remediation`, installs or upgrades a Helm release named `splunk-otel-collector`, and generates continuous test traffic.
{{% /notice %}}

