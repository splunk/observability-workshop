---
title: 2. Getting Started with DXA
weight: 2
---

**Digital Experience Analytics (DXA)** complements Splunk Real User Monitoring (RUM) and Synthetic Monitoring by adding an analytics layer on top of session data already collected by RUM. DXA helps product teams identify friction points, refine user journeys, increase conversion rates, and improve feature engagement — without writing queries or changing application code every time.

Learn more in the [Introduction to Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/introduction-to-digital-experience-analytics).

## Key concepts

DXA organizes work into four building blocks:


| Concept               | Purpose                                                                                                                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Projects**          | Collaborative workspaces for a product or application                                                                                                                          |
| **Event definitions** | Named user actions (clicks, navigation, errors) that power analyses. You can add custom event definitions in the DXA UI on top of what is already coming in from RUM sessions. |
| **User segments**     | Groups of users based on attributes, behaviors, or session criteria                                                                                                            |
| **Analyses**          | Visualizations — time series, conversion funnels, and journey maps                                                                                                             |


For more information about Projects in DXA, see [documentation on Projects in Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics/projects-in-digital-experience-analytics).

{{% notice title="Instrumentation" style="info" %}}
DXA uses the same RUM agents and instrumentation as Splunk RUM. The Astronomy Shop is already instrumented for this workshop. If you need to set up DXA in your own environment later, see [Set up Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics).
{{% /notice %}}

{{% exercise title="Navigate to DXA" %}}

1. Sign in to **Splunk Observability Cloud** using credentials provided by your instructor.
2. From the left navigation, open **Digital Experience → Digital Experience Analytics**.
3. Open the workshop **Astronomy Shop** project (your facilitator will confirm the exact project name).
4. Orient yourself to the project tabs:
    - Overview
    - Event Definitions
    - User Segments
    - Analyses

{{< tabs >}}
{{% tab title="Question" %}}
What value are we trying to get out of DXA if we already have RUM dashboards and session replay?
{{% /tab %}}
{{% tab title="Answer" %}}
RUM tells us *what happened* in user sessions over time: page loads, errors, and performance. 

DXA shows us *user impact*, adding an analytics lens to RUM data. DXA does this with reusable event definitions, conversion funnels, frustration trends, and user segments that connect session-level data to business-relevant questions like "Are users adopting our new feature?" or "Where do we lose checkout conversions?" — all configurable in the UI without code changes.
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

The workshop project includes pre-built analyses we will explore next. First, let's see how **event definitions** translate raw RUM interactions into named, reusable events.