---
title: 3. Metadata
weight: 3
---

The **Metadata** tab is the smallest tab in the Navigator and the easiest to skip — but it is where you confirm the basics about the instance you have been investigating. Engine version, host, edition, and configuration parameters all live here.

Use it to answer questions like: *Is this the engine version we think it is? Is this a primary or a replica? Is the configuration the same as the other instance in the same cluster?*

{{% notice title="Exercise" style="green" icon="running" %}}

* Click the **Metadata** tab in the Navigator.
* Scan the metadata fields and note the **engine version** and **host** for the instance.

<!-- TODO screenshot: Metadata tab showing engine version, host, and other instance configuration details -->
![Metadata](../images/metadata.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Why is engine version worth checking before you spend time tuning a query?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Optimiser behaviour, supported syntax, and even default index strategies change between versions** — a fix that worked on a different version may not apply, and an issue you are seeing may already be fixed in a newer one.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
