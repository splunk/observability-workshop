---
title: Neighbours are a pain
weight: 4
draft: true
layout: chapter
time: 45 minutes
description: A noisy neighbour is hogging resources — learn how to spot the culprit using infrastructure monitoring.
params:
  images:
    - images/im.webp
---

{{< presenter >}}
This module needs Astronomy Shop **2.0.9+** with `k8s-scenario-controller` and the `S-*` Feature flags. Do not run it on 2.0.8 Show instances.

Feature flags are **sequential**. Leave every `S-*` flag **off** until the matching scenario page. Leave **S-TEST-shelltester** off for the whole module.

* Open the Astronomy Shop URL and append `/Feature`.
* If this module is standalone, disable other fault demos (`paymentFailure` off). If it follows Intro, `paymentFailure` at **50%** can stay.
* Each scenario page has the next toggle. Turn the previous `S-*` flag **off** before you enable the next one, then wait about 30 seconds.
* Wrap-up: turn remaining `S-*` flags **off**.

Cluster name in Kubernetes: **`[NAME OF WORKSHOP]-k3d-cluster`**. Workshop k3s/k3d instances are typically **one node**, so a 5-replica anti-affinity Deployment shows **1 Running / 4 Pending**. If the cluster has three nodes, expect 3 Running / 2 Pending.
{{< /presenter >}}

{{< persona role="SRE / platform engineer" >}}
{{< persona-situation >}}You are responsible for the Astronomy Shop cluster. Pods are pending, a deployment looks degraded, and a service that looked healthy a minute ago has already restarted.{{< /persona-situation >}}
{{< persona-goal >}}Use Kubernetes in Splunk Observability Cloud to find the cause and the blast radius — which pods, deployments, and services are affected — without stitching metrics, events, and YAML by hand.{{< /persona-goal >}}
{{< /persona >}}

> [!splunk] **Infrastructure Monitoring** is where Splunk Observability Cloud shows Kubernetes clusters, nodes, workloads, and pods. In this module you use the Kubernetes **new experience** to investigate four production-style issues in the Astronomy Shop.

This module contains four scenarios:

- **Scenario 1: Noisy neighbour** — Find the pod that is holding extra memory and the deployment that cannot schedule.
- **Scenario 2: Degraded deployments** — Start from Kubernetes Overview and inventory every deployment that does not have the desired number of pods.
- **Scenario 3: Image pull** — Identify a pod stuck in `ImagePullBackOff` and confirm the typo in the image tag.
- **Scenario 4: APM to Kubernetes** — Start from APM, land on the crashing pod, and confirm a memory-limit OOM restart cycle.

{{% notice title="Wait for your instructor" style="info" icon="chalkboard-user" %}}
Your instructor enables each scenario in turn. Stay on the current page until they give you the **go-ahead** to start the next scenario. If you jump ahead, the Kubernetes view will not match the steps.
{{% /notice %}}
