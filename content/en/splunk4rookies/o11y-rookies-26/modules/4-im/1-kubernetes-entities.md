---
title: 1. Kubernetes entities
weight: 1
draft: true
---

{{< presenter >}}
Keep every `S-*` flag **off** on this page. Participants only open Kubernetes and filter to their cluster. Enable **S-Noisy-neighbour** on the next page.
{{< /presenter >}}

The Astronomy Shop runs on Kubernetes. Before you chase a noisy neighbour, get oriented: one cluster, its nodes, and the workloads on those nodes.

{{% notice title="Kubernetes terminology" style="info" %}}

**Kubernetes** (K8s) is an open-source platform for deploying and running containers. This workshop hosts the Astronomy Shop on it.

* A **cluster** is a group of machines, called **nodes**, that run containerized applications. Workshop instances are typically a **single node**.
* A **pod** is the smallest deployable unit — one or more containers that share network and storage.
* A **namespace** is a logical boundary inside the cluster (for example, the shop namespace).
* A **workload** (Deployment, DaemonSet, and similar) declares how many pod replicas should run and how they restart.

{{% /notice %}}

{{< notice tip >}}
Replace [NAME OF WORKSHOP] with the workshop name assigned to you by your instructor. If that name is **workshop**, the cluster is **workshop-k3d-cluster**.
{{< /notice >}}

{{% exercise title="Open Kubernetes and filter to your cluster" %}}

* From the main menu in Splunk Observability Cloud, select **Infrastructure**.
* Open **Kubernetes**. If you are offered a choice, use the **new experience**.
* Set the time range to **Last 15 minutes** using the time picker.
* Filter to your workshop cluster:
  * Click {{% button style="blue" %}}Add Filter{{% /button %}}
  * Select `k8s.cluster.name`
  * Set the value to **[NAME OF WORKSHOP]-k3d-cluster**
  * Click {{% button style="blue" %}}Apply Filter{{% /button %}}

You should now see a single cluster. Keep this filter for the rest of the module.

<!-- TODO screenshot: Kubernetes new experience filtered to [NAME OF WORKSHOP]-k3d-cluster -->

{{% /exercise %}}

{{% notice title="Info" style="info" %}}
Shared Observability orgs contain many clusters. Filtering to `k8s.cluster.name` first keeps every later click — nodes, pods, and overview — on **your** Astronomy Shop.
{{% /notice %}}
