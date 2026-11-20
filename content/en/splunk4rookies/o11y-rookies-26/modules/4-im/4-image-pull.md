---
title: 4. Scenario 3 — Image pull
weight: 4
draft: true
---

{{< presenter >}}
On `/Feature`, set **S-Degraded-deployments** to **off**, then set **S-imagePullBackoff** to **on**. Wait about 30 seconds for dummy Deployment **`cart-imagepull`**.

The image is `ghcr.io/splunk/opentelemetry-demo/otel-cart:lastest` — typo **`lastest`**, not `latest`. This does **not** change live `cart`.
{{< /presenter >}}

Pod failures are frequent and often cryptic. You need one place that shows which pods are failing and **why**, without stitching logs, events, and metrics yourself. Common Kubernetes reasons such as `CrashLoopBackOff` and `ImagePullBackOff` should be visible out of the box.

{{% exercise title="Find the ImagePullBackOff pod" %}}

* In Kubernetes (new experience), open **Pods**. Keep the filter `k8s.cluster.name` = **[NAME OF WORKSHOP]-k3d-cluster**.
* **Sort by Status**. Status here is the **container reason code** (for example `ImagePullBackOff`), not only Failed or Pending. That is the shortcut that saves a long troubleshooting loop.
* Find the pod whose name starts with **`cart-imagepull`**. It should show **ImagePullBackOff**.

This dummy is **not** the live Astronomy Shop `cart` service.

<!-- TODO screenshot: Pods list sorted by Status showing cart-imagepull ImagePullBackOff -->

{{% /exercise %}}

{{% exercise title="Prove the image tag is wrong" %}}

* Open the **`cart-imagepull`** pod.
* Open the **Pod lifecycle** tab. Note how long the pod has been stuck in this state.
* Select the pod **events** row for that time and status. You should see a back-off pulling:

  `ghcr.io/splunk/opentelemetry-demo/otel-cart:lastest`

* Open the **YAML** tab. On the right, expand `spec` → `containers` → `[0]` → `image`. The tag is **`lastest`** — a typo of **`latest`**.

<!-- TODO screenshot: cart-imagepull events plus YAML image field showing :lastest -->

{{< quiz question="Why is cart-imagepull stuck in ImagePullBackOff?" >}}
{{< quiz-option correct=true >}}The image tag is misspelled as lastest instead of latest.{{< /quiz-option >}}
{{< quiz-option >}}The live cart Deployment was scaled to zero.{{< /quiz-option >}}
{{< quiz-option >}}The node is under MemoryPressure, so kubelet will not pull images.{{< /quiz-option >}}
{{< quiz-feedback >}}
**The image tag is misspelled as lastest instead of latest.**
Events show kubelet backing off that exact URL, and YAML confirms `spec.containers[0].image` uses `:lastest`. The registry has no such tag, so the pod never becomes Ready. Live `cart` is unchanged.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

{{% notice title="Info" style="info" %}}
**Reason codes out of the box.** Sorting pods by container status tells you *ImagePullBackOff* immediately. Events name the URL; YAML shows the typo. That is the same path you would use for `CrashLoopBackOff` and other common Kubernetes failures, with metrics, events, and config in one place.
{{% /notice %}}
