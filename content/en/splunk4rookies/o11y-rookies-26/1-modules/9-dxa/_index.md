---
title: Digital Experience Analytics
linkTitle: 9. Digital Experience Analytics
weight: 9
archetype: chapter
time: 45–60 minutes
authors: ["Sarah Ware"]
description: Understand user behavior, friction, and conversion in Astronomy Shop using DXA -- no code changes required.
draft: false
hidden: false
params:
  images:
    - images/funnel.png
---

**Digital Experience Analytics (DXA)** is a solution within Splunk Observability Cloud that turns RUM session data into actionable insights about end user adoption, friction, and conversion. In this module, you will explore a pre-configured DXA project for the Astronomy Shop — no instrumentation or code changes required.

{{% notice icon="user" style="orange" title="Persona" %}}

You are a **product manager** or **digital experience owner** for the Astronomy Shop. Leadership has asked you to improve checkout conversion and understand whether new features like **Ask AI** are delivering value. Your team already has RUM data — now you need business-focused insights without waiting on engineering to ship more code.

{{% /notice %}}

## Overview

In this hands-on module, you will:

- **Generate real user sessions** by browsing the Astronomy Shop
- **Navigate DXA** and understand how it builds on existing RUM data
- **Explore event definitions** that power analyses without custom instrumentation
- **Analyze feature adoption** with a time series and session replay
- **Monitor frustration signals** like rage clicks and dead clicks
- **Investigate conversion funnels** and checkout drop-off
- **Compare user segments** to uncover targeted improvement opportunities

For background, see the [Introduction to Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/introduction-to-digital-experience-analytics) documentation.

{{% notice title="Note" style="info" %}}
The workshop tenant includes a pre-configured DXA project with analyses, event definitions, and user segments. You will explore and interpret these artifacts — not build them from scratch.
{{% /notice %}}