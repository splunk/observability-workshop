---
title: 3. Scenario 2 — Degraded deployments
weight: 3
draft: true
---

{{< presenter >}}
On `/Feature`, set **S-Noisy-neighbour** to **off**, then set **S-Degraded-deployments** to **on**. Wait about 30 seconds until `storefront-spread` and `otel-collector-noisy` disappear and dummy Deployment **`paymentservice`** appears (5 replicas, required hostname anti-affinity).

Do **not** leave both flags on — Kubernetes Overview would list two degraded dummies.

This dummy is **not** live `payment` / `payment-vA` / `payment-vB`. Expected on a 1-node cluster: **1/5** available.
{{< /presenter >}}

As a Kubernetes admin you want a **single pane of glass** across the cluster, not a reactive hop from one entity to the next. Start from inventory, then drill into the deployment that does not have the pods it asked for.

{{% exercise title="Inventory degraded deployments" %}}

* From the main menu, select **Infrastructure**, then **Kubernetes Overview**.
* Confirm the cluster filter is still **[NAME OF WORKSHOP]-k3d-cluster**. You can stay on a single cluster for this lab.
* Walk **Inventory**, then open **Top issues** → **degraded deployments**.
* Find **`paymentservice`**. Desired replicas are **5**. Running / available should be **1** on a one-node workshop cluster (or **3** on a three-node cluster).

This is a dummy workload created for the lab. It is **not** the live Astronomy Shop `payment` service that checkout uses.

<!-- TODO screenshot: Kubernetes Overview Top issues showing paymentservice degraded (1/5 or 3/5) -->

{{% /exercise %}}

{{% exercise title="Confirm the scheduling rule" %}}

* Open the **`paymentservice`** deployment, then the **pod list**.
* Pick a **Pending** pod.
* Open **Pod lifecycle**. You should see failed scheduling for the same reason as Scenario 1: not enough nodes satisfy the placement rule.
* Open **YAML** and search for `affinity`. Under `spec` you should again see **required** `podAntiAffinity` on `kubernetes.io/hostname`.

<!-- TODO screenshot: paymentservice pending pod lifecycle and YAML affinity -->

{{< quiz question="In Kubernetes Overview, what does a degraded deployment mean?" >}}
{{< quiz-option correct=true >}}Running (available) pods are fewer than the desired replica count.{{< /quiz-option >}}
{{< quiz-option >}}The deployment has no YAML.{{< /quiz-option >}}
{{< quiz-option >}}Every pod in the cluster is in CrashLoopBackOff.{{< /quiz-option >}}
{{< quiz-feedback >}}
**Running (available) pods are fewer than the desired replica count.**
`paymentservice` wants five pods. Required hostname anti-affinity plus a small cluster leaves extras Pending, so Overview flags the deployment as degraded. The same YAML root cause you saw on `storefront-spread` shows up here from an inventory starting point.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

{{% notice title="Info" style="info" %}}
**Proactive inventory.** Kubernetes Overview lists every workload that is not at desired count, so you do not have to wait for an alert or guess which entity to open. From that list you still drill all the way to the anti-affinity rule in YAML — the kind of configuration root cause a Kubernetes SRE expects to reach in the product.
{{% /notice %}}
