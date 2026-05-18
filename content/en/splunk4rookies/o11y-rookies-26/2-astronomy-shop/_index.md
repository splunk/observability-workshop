---
title: The Astronomy Shop
linkTitle: 2. The Astronomy Shop
weight: 2
archetype: chapter
time: 10 minutes
description: Explore the OpenTelemetry Demo application and generate telemetry data for the workshop modules.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are a **curious astronomer**, browsing the Astronomy Shop for telescopes, star charts, and accessories.

> [!splunk] The **Astronomy Shop** is the Splunk distribution of the OpenTelemetry Demo (v2.0.1) — a microservices e-commerce application fully instrumented with OpenTelemetry. It generates metrics, traces, and logs across multiple services written in different languages. The telemetry data you generate here will be used in whichever modules your trainer selects.

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* Your instructor will provide the URL to the Astronomy Shop.
* Browse the catalog — view product details, read descriptions.
* Add several items to your cart.
* Proceed to checkout and complete a purchase.
* **Repeat 3-5 times** to generate enough telemetry data.

<!-- TODO screenshot: Astronomy Shop storefront -->

{{< tabs >}}
{{% tab title="Question" %}}
**Did everything work smoothly, or did you notice anything unusual during checkout?**
{{% /tab %}}
{{% tab title="Answer" %}}
Some services in the Astronomy Shop have deliberately injected issues. You may have noticed slow responses or errors during checkout — this is intentional and will be investigated in the workshop modules.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
