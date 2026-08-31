---
title: "Investigate Payment Errors"
linkTitle: "3. Payment Errors"
weight: 3
---

{{% exercise title="Identify the Payment Error" %}}

* Scroll down to ***Error* breakdown** and expand the section if necessary **(2)**.
* Examine **Errors by HTTP** status code **(3)**.

![Service Dashboard](../images/apm-service-dashboard.png)

{{< tabs >}}
{{% tab title="Questions" %}}
* Which *HTTP status code* is associated with the *payment* errors, and what does it usually indicate?
{{% /tab %}}
{{% tab title="Answers" %}}

1. The errors return *HTTP status code* **401**. This means *Unauthorized* and usually indicates that authentication credentials are missing, invalid, or no longer accepted.
2. Notice that **401** also appears in the *exception* and *gRPC* breakdowns. This confirms that the same authentication-related failure is being recorded consistently across the service telemetry.

{{% /tab %}}
{{< /tabs >}}
{{% /exercise %}}
The overview confirms that the **payment** service has recurring *authentication* failures, but it does not yet show what the affected requests have in common. To look for a pattern, select the **Tag Spotlight** tab **(4)**.


