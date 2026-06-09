---
title: 1. Check Feature and Alert Prerequisites
weight: 1
---

The AI troubleshooting agent runs from the alert experience. It is not a generic chat prompt that can investigate every chart or custom metric. Start by proving that your environment and alert are in the supported path.

{{% notice title="Exercise" style="green" icon="running" %}}

* Open Splunk Observability Cloud and confirm that your URL is in the `us1` realm, for example `https://app.us1.signalfx.com`.
* Confirm with your workshop facilitator or Splunk representative that the AI troubleshooting agent and remediation plan are enabled for the organization.
* Navigate to **Alerts & Detectors** and open **Active Alerts**.
* Find an alert that comes from one of these domains:
  * A Splunk APM service detector using standard APM service metrics.
  * A Kubernetes detector in Infrastructure Monitoring using standard Kubernetes metrics.
* Avoid custom metric detectors for this workshop. They can still be useful detectors, but they are outside the current supported scope for this feature.
* Record the following in your incident notes:

| Field | Value |
|-------|-------|
| Realm | `us1` |
| Alert name | |
| Detector name | |
| Domain | `APM service` or `Kubernetes Infrastructure Monitoring` |
| Service, workload, pod, node, or cluster | |
| Environment | |
| Alert start time | |

{{< tabs >}}
{{% tab title="Question" %}}
**Why is a custom metric detector a poor fit for this workshop, even if it produced a real alert?**
{{% /tab %}}
{{% tab title="Answer" %}}
**The current feature support is limited to standard, default metrics for APM services and Kubernetes alerts, so a custom metric detector may not produce AI troubleshooting or remediation output.**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{% notice title="Instructor Note" style="info" %}}
If the organization does not have an active supported alert, use a pre-captured alert for the investigation chapters and run the remediation discussion as a tabletop exercise. Do not lower production detector thresholds just to create an alert.
{{% /notice %}}

