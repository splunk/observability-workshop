---
title: 3. Pick an Instance and Open the Navigator
weight: 3
---

Once you have a candidate instance, you click it to open the **Navigator** — an instance-specific view that is going to be your home for the rest of the workshop.

The Navigator has five tabs across the top:

- **Queries** — top SQL statements running on this instance.
- **Query samples** — individual captured executions, with parameters and execution plans.
- **Query metrics** — per-query trends over time.
- **Dependencies** — applications and hosts calling this instance.
- **Metadata** — engine version, host, and configuration details.

Any active alerts for the instance appear in the upper-right corner.

{{% notice title="Exercise" style="green" icon="running" %}}

* Back on the **Overview** page, switch the chart back to **Duration** so we are working with the slowest instance.
* In the instance list, click the name of the **top instance** to open it.
* You will land on the **Navigator** view for that instance.
* Take a look at the five tabs across the top **(1)** and the alerts area in the upper-right **(2)**.

<!-- TODO screenshot: Navigator view for an instance with the five tabs annotated (1) and the alerts area annotated (2) -->
![Navigator view](../images/navigator.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Which tab is selected by default when you open the Navigator?**
{{% /tab %}}
{{% tab title="Answer" %}}
**Queries** — the Navigator opens on the top-queries view because that is almost always where an investigation continues from the overview.
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
