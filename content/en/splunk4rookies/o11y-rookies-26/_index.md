---
title: Observability Cloud (2026)
weight: 1
authors: ["Pieter Hagen"]
time: Variable
description: "Start with the basics, then choose your path: infrastructure, digital experience, AI, and more."
layout: "hero"
badge: "Beta"
#build:
#  list: never
#  render: always
params:
  images:
    - images/card-hero.png
difficulty: Rookie
---

{{< presenter >}}
Make sure the Splunk Show instance is started in time , building the EC2 instance after boot can take ~30 minutes.
{{< /presenter >}}

## Introduction

This is the **2026** Splunk Observability Cloud workshop for rookies. It is no
longer one fixed sequence of lessons. You complete a short introduction, then
choose **self-contained modules** or a **recommended path**.

Every module uses the same lab application: the OpenTelemetry Demo, also known
as the Astronomy Shop. You generate real user, application, and infrastructure
telemetry, then investigate it in Splunk Observability Cloud.

If you are new to the platform, start with the **Introduction** module. It
covers login, the Astronomy Shop, and a first pass through RUM, APM, logs, and
Synthetics.

After that, pick what matches your session:

- A **path** if you want a guided route (infrastructure, digital experience, or
  AI monitoring).
- Individual **modules** if you only need one topic, such as logs, databases,
  application security, or digital experience analytics.

Your instructor may still run a subset of modules to fit the time available.

{{< cta href="/splunk4rookies/o11y-rookies-26/modules/1-intro/" icon="rocket" >}}Start the Introduction module{{< /cta >}}

{{< divider >}}

### Continue your workshop journey

{{< cards >}}
{{< card title="Choose Your Path" href="/splunk4rookies/o11y-rookies-26/pathways/" hero-icon="route" >}}
Follow a recommended route through the modules based on your area of interest.
{{< /card >}}
{{< card title="Browse All Modules" href="/splunk4rookies/o11y-rookies-26/modules/" hero-icon="library" >}}
View every available workshop module and choose the ones you want to complete.
{{< /card >}}
{{< /cards >}}

<!--{{% notice style="note" title="Parking Lot" icon="circle-info" %}}
Login instructions and Astronomy Shop setup details are available at the end of the workshop navigation for reference.
{{% /notice %}}-->
