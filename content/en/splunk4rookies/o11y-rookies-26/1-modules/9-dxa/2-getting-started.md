---
title: 2. Getting Started with DXA
weight: 2
time: 8 minutes
---

**Digital Experience Analytics (DXA)** complements Splunk Real User Monitoring (RUM) and Synthetic Monitoring by adding a product-analytics layer on top of session data you already collect. DXA helps digital product teams identify friction points, refine user journeys, increase conversion rates, and improve feature engagement — without writing queries or changing application code for this workshop.

Learn more in the [Introduction to Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/introduction-to-digital-experience-analytics).

## Key concepts

DXA organizes work into four building blocks:


| Concept               | Purpose                                                                                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Projects**          | Collaborative workspaces for a product or application                                                                                                                          |
| **Event definitions** | Named user actions (clicks, navigation, errors) that power analyses. You can add custom event definitions in the DXA UI on top of what is already coming in from RUM sessions. |
| **User segments**     | Groups of users based on attributes, behaviors, or session criteria                                                                                                            |
| **Analyses**          | Visualizations — time series, conversion funnels, and journey maps                                                                                                             |


Projects are described further in [Projects in Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics/projects-in-digital-experience-analytics).

{{% notice title="Instrumentation" style="info" %}}
DXA uses the same RUM agents and instrumentation as Splunk RUM. The Astronomy Shop is already instrumented for this workshop. If you need to set up DXA in your own environment later, see [Set up Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics).
{{% /notice %}}

{{% exercise title="Navigate to DXA" %}}

1. Sign in to **Splunk Observability Cloud** using credentials provided by your instructor.
2. From the left navigation, open **Digital Experience → Digital Experience Analytics**.
3. Open the workshop **Astronomy Shop** project (your facilitator will confirm the exact project name).
4. Orient yourself to the project tabs:
  - **Overview**
  - **Event Definitions**
  - **User Segments**
  - **Analyses**



{{< tabs >}}
{{% tab title="Question" %}}
Why is DXA valuable if we already have RUM dashboards and session replay?
{{% /tab %}}
{{% tab title="Answer" %}}
RUM tells you *what happened* in individual sessions — page loads, errors, and performance. DXA adds a product-analytics lens: reusable event definitions, conversion funnels, frustration trends, and user segments that connect session-level data to business questions like "Are users adopting our new feature?" or "Where do we lose checkout conversions?" — all configurable in the UI without code changes.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

The workshop project includes pre-built analyses you will explore next. First, let's see how **event definitions** translate raw RUM interactions into named, reusable events.