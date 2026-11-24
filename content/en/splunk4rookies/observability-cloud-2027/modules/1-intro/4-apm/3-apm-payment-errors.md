---
title: "Investigate Payment Errors"
linkTitle: "3. Payment Errors"
weight: 3
---

{{% exercise title="Identify the Payment Error" %}}

* Scroll down to ***Error* breakdown** and expand the section if necessary **(1)**.
* Examine **Errors by HTTP** status code **(2)**.

![Service Dashboard](../images/apm-service-dashboard.webp)

{{< quiz question="Which HTTP status code is associated with the payment errors, and what does it usually indicate?" >}}
{{< quiz-option >}}403: the credentials are valid, but the caller is not allowed to access the resource.{{< /quiz-option >}}
{{< quiz-option correct=true >}}401: the authentication credentials are missing, invalid, or no longer accepted.{{< /quiz-option >}}
{{< quiz-option >}}404: the requested resource does not exist.{{< /quiz-option >}}
{{< quiz-option >}}500: the server hit an unexpected internal error.{{< /quiz-option >}}
{{< quiz-feedback >}}
The errors return *HTTP status code* **401**, which means *Unauthorized*. It usually indicates that authentication credentials are missing, invalid, or no longer accepted. A **403** is different: the caller has been identified but is not permitted to perform the action.

Notice that **401** also appears in the *exception* and *gRPC* breakdowns. This confirms that the same authentication-related failure is being recorded consistently across the service telemetry.
{{< /quiz-feedback >}}
{{< /quiz >}}
{{% /exercise %}}
The overview confirms that the **payment** service has recurring *authentication* failures, but it does not yet show what the affected requests have in common. To look for a pattern, select the **Tag Spotlight** tab **(3)**.


