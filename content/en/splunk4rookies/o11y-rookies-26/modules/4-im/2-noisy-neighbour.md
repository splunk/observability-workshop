---
title: 2. Scenario 1 — Noisy neighbour
weight: 2
draft: true
---

{{< presenter >}}
On `/Feature`, enable **S-Noisy-neighbour** only. Leave the other `S-*` flags **off**. Wait about 30 seconds for dummy Deployments `otel-collector-noisy` and `storefront-spread` to appear.

Do **not** raise the hog size. The dummy holds 256Mi so it is the memory outlier without putting the shop node under MemoryPressure.

Expected on a **1-node** workshop cluster: `storefront-spread` shows **5 needed, 1 running, 4 pending**. On a 3-node cluster: 3 running, 2 pending.
{{< /presenter >}}

You are an SRE on the Astronomy Shop cluster. Something is holding extra memory, and a deployment cannot get all of its pods running. Find the noisy neighbour and the blast radius.

{{% exercise title="Find the memory outlier" %}}

* In Kubernetes (new experience), open **Nodes**. Confirm the filter is still `k8s.cluster.name` = **[NAME OF WORKSHOP]-k3d-cluster**.
* Open the node. It should be **Ready**.
* From the node, open **related entities** and view the **pod** list.
* Find the **memory per pod** chart (or sort pods by memory). Identify the pod whose name starts with **`otel-collector-noisy`**.

This dummy collector is **not** the live Splunk OpenTelemetry Collector that ships shop telemetry. It is a sandbox process holding **256Mi** so you can see a noisy neighbour without taking the node down.

<!-- TODO screenshot: Node related pods with otel-collector-noisy as the memory outlier -->

{{% /exercise %}}

{{% exercise title="Confirm how the noisy neighbour behaves" %}}

* Open the **`otel-collector-noisy`** pod.
* Open **Logs**. Look for lines such as:

  `sandbox: allocated N/256 MiB (creating node memory condition)`

  and later:

  `sandbox: still holding 256 MiB`

Those logs are the sandbox script describing the allocation. They are the “how the app is behaving” signal for this incident.

<!-- TODO screenshot: otel-collector-noisy pod logs showing sandbox allocation messages -->

{{% /exercise %}}

{{% exercise title="Measure the scheduling blast radius" %}}

* From related entities, open the Deployment **`storefront-spread`**.
* Compare **desired** replicas with **running** replicas. On a typical one-node workshop cluster you should see **5 needed** and **1 running**, with the rest **Pending**.
* Open the **pod list** and pick a pod in **Pending**.
* Open the **Pod lifecycle** tab. The timeline should show failed scheduling — not enough nodes can accept the pod (for example `0/1 nodes available` on a single-node cluster).
* Open the **YAML** tab. Search (`Ctrl+F` / `Cmd+F`) for `affinity`. Under `spec` you should see **required** `podAntiAffinity` on `kubernetes.io/hostname`.

That rule means “never put two of these pods on the same node.” With five replicas and fewer than five nodes, the extras stay Pending.

<!-- TODO screenshot: storefront-spread pending pod YAML showing required podAntiAffinity -->

{{< quiz question="Why are the extra storefront-spread pods Pending?" >}}
{{< quiz-option correct=true >}}Required pod anti-affinity on hostname, with more replicas than nodes.{{< /quiz-option >}}
{{< quiz-option >}}The live Splunk OpenTelemetry Collector ran out of memory and evicted them.{{< /quiz-option >}}
{{< quiz-option >}}The cluster has no remaining CPU, so kubelet will never schedule pause pods.{{< /quiz-option >}}
{{< quiz-feedback >}}
**Required pod anti-affinity on hostname, with more replicas than nodes.**
`storefront-spread` asks for five replicas and forbids two of them on the same node. A one-node workshop cluster can run only one of those pods; the rest stay Pending. The noisy neighbour (`otel-collector-noisy`) is a separate memory hog — it is not what blocks scheduling.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

{{% notice title="Info" style="info" %}}
**Cause and impact in one flow.** You identified the memory outlier **and** traced the blast radius to a Deployment that cannot schedule.

Anti-affinity is usually the right idea for replicated components (for example a collector gateway): spread replicas so one node failure is not the whole service. A **required** rule plus too few nodes is what breaks scheduling. Node-agent collectors typically run as a **DaemonSet** (one pod per node) instead — that pattern does not use this anti-affinity.

Pod lifecycle overlays state changes with events, so you can see *when* and *why* a pod stuck in Pending after the fact.
{{% /notice %}}
