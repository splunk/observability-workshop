---
title: Beat the tweet
linkTitle: 4. Beat the tweet
weight: 4
time: 6 minutes
---

A test that finds a problem nobody is told about is just a nicely formatted record of an outage. The thing that actually beats social media to the issue is the **detector**.

In the Introduction module we previewed a detector on run duration and closed it without saving. This time we are going to activate one.

![Social media post about the shop being down](../../1-intro/6-synthetics/images/social-media-post.webp)

## Alert on uptime, not on duration

Run duration is a good signal for *slow*. For *broken*, we use **Uptime**, because the uptime metric is `0` on a failed run and `100` on a successful one. That makes it the one metric that catches every kind of failure — a timeout, a failed assertion, a certificate problem, or the site being gone entirely — without us having to predict which.

{{% exercise title="Create and activate an uptime detector" %}}

* On our test's page, select {{% button style="blue" %}}Create Detector{{% /button %}}.
* Name it something that states the goal, for example:

  ```text
  [NAME OF WORKSHOP]-[YOUR INITIALS] checkout journey failing
  ```

* Set the **metric** to **Uptime**.
* In **Alert details**:

  | Setting | Value | Why |
  |---|---|---|
  | **Trigger threshold** | `100` | Anything below a perfect run is a customer who could not buy |
  | **Orientation** | Below | Alert when uptime *drops* |
  | **Violates threshold** | `1` | Fire on the first failure, so we see it during the workshop |
  | **Split by location** | No | We are only running one or two locations |
  | **Auto-clear alerts** | On | Resolve automatically once runs stop reporting |

* Set the **severity** to **Warning**.
* Leave **Recipients** empty.
* Select {{% button style="blue" %}}Activate{{% /button %}}.

![Synthetics detector configured on the Uptime metric](../images/synth-uptime-detector.webp)

{{% /exercise %}}

{{% notice title="Why no recipients?" style="warning" %}}
All of us are building a detector against a shop that fails half its checkouts. With recipients attached, that is a lot of email for everyone. The alert still fires and is fully visible without one — we just read it in the UI instead of an inbox.

To see the notification itself, add **only our own email address**, and expect several messages.
{{% /notice %}}

## Watch it fire

{{% exercise title="Find our alert" %}}

* Go back to our test and select {{% button style="grey" %}}Run test now{{% /button %}} a couple of times until we get a failed run.
* From the main menu, open **Alerts & Detectors**.
* Find our detector by name and open the active alert.
* Read what the alert tells us: which test failed, from which location, when, and against which threshold.

{{% /exercise %}}

{{< notice tip >}}
Alerts from Synthetics detectors support **alert enrichment**, so the notification itself can carry test context — which step failed and a link to the run — rather than just a metric name and a number, reducing time to investigate.
{{< /notice >}}

## Four things we can scope a detector to

Currently our detector watches the uptime of the whole checkout test. When creating detectors, think about what is the most useful, actionable, and easy to understand, and change the scope accordingly.

| Detector scope | Alerts on | Typical use |
|---|---|---|
| **Test-level** | Metrics for the whole run: uptime, run count, run duration | "Checkout is down" — what we just built |
| **Page-level** | Metrics for one page, scoped with `page_position` | "The product page LCP broke our 2.5 s budget" |
| **Transaction-level** | Duration, requests, or size for one synthetic transaction | "The Checkout transaction breached its 8 s SLA" |
| **CA certificate-level** | SSL certificate validity and expiry, on SSL tests | "The storefront certificate expires in 30 days" |

Because we named our transactions, we can alert on **Duration** scoped to `transaction:Checkout` and hold the checkout flow to its own SLA without the noise of the rest of the journey.

{{< quiz question="Which scope do you use if you want to focus on the time it takes for the checkout portion of the user journey?" >}}
{{< quiz-option >}}Test-level uptime. It already covers every step.{{< /quiz-option >}}
{{< quiz-option >}}Page-level, scoped to the cart page.{{< /quiz-option >}}
{{< quiz-option correct=true >}}Transaction-level, on Duration scoped to transaction:Checkout.{{< /quiz-option >}}
{{< quiz-feedback >}}
Uptime says the journey is broken. Duration scoped to the Checkout transaction says it is slow, and it stays quiet when only browsing gets slower. That scope exists because the transactions were named.
{{< /quiz-feedback >}}
{{< /quiz >}}

![Synthetics detector configured on the transaction duration metric](../images/synth-transaction-detector.webp)

{{% notice title="In real life, reduce noise" style="info" %}}
Firing on a single failure is great in a workshop but not a good idea in real life. Fine tune the threshold, violation, and location split to get a manageable level of noise based on the estimated alert count.
{{% /notice %}}

{{< presenter >}}
After the session, delete or deactivate the attendee detectors along with their tests. Search **Alerts & Detectors** for the workshop name.
{{< /presenter >}}

Learn more in [Detectors and alerts](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/detectors-and-alerts).
