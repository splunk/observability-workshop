---
title: 5. Scenario 4 — APM to Kubernetes
weight: 5
draft: true
---

{{< presenter >}}
On `/Feature`, set **S-imagePullBackoff** to **off**, then set **S-Resource-management** to **on**. Wait until the first memory sawtooth is visible — typically about **two minutes**. The dummy **`email-oom`** leaks from 16Mi toward a **100Mi** limit (+20Mi every 30s), fails probes near 80Mi, then OOMKills and restarts.

APM `service.name` is **`email`**. The pod name starts with **`email-oom`**. This does **not** patch live `email`. Do not ask participants to edit cluster YAML; the story fix is “raise the container memory limit.”
{{< /presenter >}}

Email looks fine when you log in — Kubernetes already restarted the pod. You suspect the infrastructure, not the latest request. Start in APM and land on the exact pod.

{{% exercise title="Go from APM to the crashing pod" %}}

* From the main menu, select **APM**, then **Overview**.
* Select the **`email`** service. Set **Environment** to the workshop name your instructor already gave you for Intro, and set the time range to **Last 15 minutes** (or **Last 1 hour** if you need a wider window).
* Open **Instances**. Focus on the instance whose pod name starts with **`email-oom`** — that is the one with restarts.
* Click the pod to open it in the Kubernetes **new experience** (node, namespace, and cluster come with it).

This dummy emits traces as `service.name=email` so APM can link to the pod. It is **not** the live email Deployment checkout uses.

<!-- TODO screenshot: APM email Instances highlighting the email-oom pod -->

{{% /exercise %}}

{{% exercise title="Confirm the sawtooth and OOM cycle" %}}

* On the pod, open the **memory** chart. Keep **Last 15 minutes** (or widen to **1 hour**). You should see a **sawtooth**: memory climbs toward the **100Mi** container limit, the pod dies, kubelet recreates it, and the climb repeats.
* Open the **Events** tab. You should see liveness/readiness probe failures (**Unhealthy**) and then **OOMKilled** / container recreate.

The leak is fast on purpose so the pattern fits a workshop window. In production the same shape often takes hours; the investigation is the same: extend the time range until the restart cycle is visible.

<!-- TODO screenshot: email-oom memory sawtooth and Events showing Unhealthy then OOMKilled -->

{{< quiz question="What is the root cause of the email-oom restart cycle?" >}}
{{< quiz-option correct=true >}}The container memory limit (100Mi) is too low for the working set, so the kubelet OOMKills the container.{{< /quiz-option >}}
{{< quiz-option >}}The image tag is misspelled, so the pod never starts.{{< /quiz-option >}}
{{< quiz-option >}}Required anti-affinity is blocking the pod from scheduling.{{< /quiz-option >}}
{{< quiz-feedback >}}
**The container memory limit (100Mi) is too low for the working set, so the kubelet OOMKills the container.**
Memory climbs to the limit, probes fail, then the container is OOMKilled and recreated — the sawtooth. The fix in this story is to raise the container memory limit. Do not change live shop YAML in the cluster.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

{{% notice title="Info" style="info" %}}
**APM-to-Kubernetes correlation.** OpenTelemetry links the APM service instance to the pod with no extra mapping from you. The Kubernetes new experience then keeps node, namespace, cluster, memory, and events on one page.

**Historical pattern detection** matters: the default short window can look healthy right after a restart. Widen the time range until the sawtooth is obvious, then use events to confirm OOMKills.
{{% /notice %}}
