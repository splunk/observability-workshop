---
title: Prepare the Environment
linkTitle: 2. Prepare the Environment
weight: 2
archetype: chapter
time: 20 minutes
description: Confirm tools, namespace access, Splunk identity values, and lab file locations.
---

{{% notice icon="user" style="orange" title="Persona" %}}
You are a **student operator** preparing your assigned namespace. Your goal is to prove you can run namespace-scoped commands without exposing secrets.
{{% /notice %}}

## Required Tools

Check your local tools:

```bash
kubectl version --client
helm version
curl --version
jq --version
```

You do not need an AWS account, NVIDIA account, cluster-admin permissions, Docker, or container registry login for the student path.

## Set Lab Variables

Replace the placeholders with values from your lab handout.

```bash
export STUDENT_ID="<STUDENT-ID>"
export STUDENT_NAMESPACE="<STUDENT-NAMESPACE>"
export SPLUNK_REALM="<SPLUNK-REALM>"
export SPLUNK_ACCESS_TOKEN_SECRET="splunk-observability-token"
export LOGICAL_CLUSTER_NAME="clus-ltrobs-2001-<STUDENT-ID>"
export COLLECTOR_CHART=splunk-otel-collector-chart/splunk-otel-collector
```

{{% notice title="Do Not Print Tokens" style="warning" %}}
`SPLUNK_ACCESS_TOKEN_SECRET` is the Kubernetes Secret name, not the token value. Do not export, paste, print, or share the actual Splunk token.
{{% /notice %}}

## Confirm Namespace Access

```bash
kubectl get pods -n "$STUDENT_NAMESPACE"
kubectl auth can-i get pods -n "$STUDENT_NAMESPACE"
kubectl auth can-i create deployments -n "$STUDENT_NAMESPACE"
kubectl auth can-i create services -n "$STUDENT_NAMESPACE"
```

Expected result:

- Commands succeed for your namespace.
- You do not need cluster-admin permissions.

If this fails, check:

```bash
kubectl config current-context
kubectl auth can-i --list -n "$STUDENT_NAMESPACE"
```

Stop and ask the instructor to fix access if normal namespaced permissions are missing.

## Confirm The Preloaded Splunk Secret

```bash
kubectl get secret "$SPLUNK_ACCESS_TOKEN_SECRET" -n "$STUDENT_NAMESPACE"
```

Expected result:

- The Secret exists in your namespace.
- You do not inspect or print Secret data.

If collector logs later show `401 Unauthorized`, the Kubernetes deployment is running but Splunk rejected the credential. Ask the instructor to validate the preloaded token, organization, and realm.

## Lab Files

The local source copy includes the files from the original lab:

```bash
cd workshop/clus-shopmate-exercises
ls workshop/lab-files
```

Key files:

| File | Purpose |
| --- | --- |
| `workshop/lab-files/shopmate-ai.yaml` | Kubernetes manifest for ShopMate Sports. |
| `workshop/lab-files/collector-observability-snippet.yaml` | Reference collector sections for GPU and NIM scraping. |
| `workshop/lab-files/student-collector-values-gpu-nim-reference.yaml` | Complete reference collector values after GPU and NIM scraping. |
