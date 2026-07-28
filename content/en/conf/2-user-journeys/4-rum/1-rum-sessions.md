---
title: User Sessions
linkTitle: 1. User Sessions
weight: 1
time: 5 minutes
---

In Splunk RUM, a **session** is a continuous period of user activity on your app (up to four hours, ending after inactivity or when the app closes). RUM sessions inform analyses like funnels and feature adoption timeseries.

**Session details** show metadata, replay events, and a waterfall of spans (loads, requests, custom events, web vitals, errors). See [Key concepts in Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/key-concepts-in-splunk-rum) for more info.

{{% exercise title="Explore an open user session" %}}

Use the user session you already have open, or open a new one.

* On **session details**, note the summary: **Session ID**, start time, **duration**, and client/OS.

* In **Session Events**, click through a few events and watch the event list and replay stay in sync.
* Select the event where the user **Place order** (or the longest page). In the span list, find examples of:
  * a **document load** or **page** span,
  * a **fetch/XHR** (network request) span,
  * a **custom event** span (like **PlaceOrder**),
  * and any **error** or slow span.

* Click one span and toggle **Parsed** vs **Raw**:
  * **Parsed** — curated tags and values for quick reading.
  * **Raw** — full detail for that span.

![RUM user session details](../images/rum-waterfall-place-order.png)

{{< tabs >}}
{{% tab title="Questions" %}}

What can you learn from session details that you cannot see from a funnel or aggregate chart alone?

{{% /tab %}}
{{% tab title="Answers" %}}

The exact sequence and timing for **one user session**: which pages and events ran, which requests or custom events were slow or failed, and which spans tie to backend traces. Additionally, all fields and tags on a span for deeper analysis or to share with another team.

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

Let's see how RUM Sessions roll up to give us an understanding of our application health and user experience!