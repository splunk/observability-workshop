---
title: 1. Prerequisites
weight: 1
time: 15 minutes
---

This workshop uses a local Kubernetes runtime for the application and hosted Splunk services for observability and service intelligence.

## Accounts and Access

You need:

- A Splunk Observability Cloud organization and an access token with ingest permissions.
- A Splunk Cloud Platform or Splunk Enterprise environment with ITSI installed.
- Permission to create Observability Cloud detectors and notification integrations.
- Permission to create or edit ITSI services, KPIs, episode aggregation policies, and glass tables.
- A Splunk platform HTTP Event Collector (HEC) token for Observability Cloud alert notifications.

## Recommended ITSI Packages

Use the packaged content where available:

| Package | Why it matters |
|---|---|
| Splunk App for Content Packs | Installs and manages supported ITSI content packs. |
| Content Pack for Splunk Observability Cloud | Provides prebuilt ITSI/ITE Work content for Observability Cloud metrics, including APM, Infrastructure Monitoring, and Synthetic Monitoring views. |
| Splunk Infrastructure Monitoring Add-on | Supplies the `sim` SPL command and metric/event access used by the Observability Cloud content pack. |

{{% notice title="Package Scope" style="info" %}}
The content pack accelerates metric-based ITSI visibility and gives students a supported starting point. You still need the business transaction map from this workshop to decide how Astronomy Shop services roll up into customer journeys and business impact.
{{% /notice %}}

{{% notice title="Data Flow" style="info" %}}
The laptop lab sends metrics, traces, and logs to Splunk Observability Cloud. ITSI does not need to ingest every trace. ITSI receives detector alert and clear events from Observability Cloud through the Splunk platform integration, then uses those events to update business services and episodes.
{{% /notice %}}

{{% notice title="Local ITSI Runtime" style="warning" %}}
Do not plan this workshop around ITSI running in the official Splunk Enterprise Docker image. Splunk Enterprise can run in Docker for hands-on experience, but the Docker-Splunk app installation guidance states that installing Splunk Enterprise Security or Splunk IT Service Intelligence is not supported with that image. Use an existing Splunk Enterprise + ITSI environment, Splunk Cloud Platform with ITSI, or a properly sized VM-based Splunk Enterprise instance for the ITSI side of the lab.
{{% /notice %}}

## Laptop Tools

Install these tools before class:

```bash
docker version
minikube version
kubectl version --client
helm version
jq --version
```

The lab assumes a Minikube profile named `business-journey`. You can change it with `MINIKUBE_PROFILE`.

## Environment Variables

Set your Splunk Observability Cloud realm and access token:

```bash
export SPLUNK_REALM=us1
export SPLUNK_ACCESS_TOKEN=<your-access-token>
```

Optional settings:

```bash
export MINIKUBE_PROFILE=business-journey
export CLUSTER_NAME=business-journey-minikube
export DEPLOYMENT_ENVIRONMENT=business-journey-workshop
```

## Workshop Directory

Run lab commands from:

```bash
cd workshop/observing-business-journeys
```

Check local prerequisites:

```bash
./scripts/status.sh doctor
```

{{% notice title="Minikube Sizing" style="info" %}}
Astronomy Shop is a multi-service demo. The deployment script starts Minikube with 4 CPUs and 8 GB of memory by default. Override with `MINIKUBE_CPUS` and `MINIKUBE_MEMORY` if your laptop needs different settings.
{{% /notice %}}
