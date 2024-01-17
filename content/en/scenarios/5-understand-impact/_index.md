---
title: Understand Impact
linkTitle: 5. Understand Impact
weight: 5
archetype: chapter
---

{{% badge icon="clock" style="primary" %}}2 minutes{{% /badge %}} {{% badge style="blue" title="Authors" %}}Derek Mitchell{{% /badge %}}


**Splunk Observability Cloud** includes powerful features that dramatically reduce the time required for SREs to isolate issues across services, so they know which team to engage to troubleshoot the issue further.

Unlocking these features requires tags to be included with your application traces.  But how do you know which tags are the most valuable and how do you capture them?

In this workshop, we'll explore: 

* What are tags and why are they such a critical part of making an application observable.
* How to use **OpenTelemetry** to capture tags of interest from your application.
* How to index tags in **Splunk Observability Cloud** and the differences between **Troubleshooting Metric Sets** and **Monitoring Metric Sets**.
* How to utilize tags in **Splunk Observability Cloud** to find “unknown unknowns” using the **Tag Spotlight** and **Dynamic Service Map** features.
* How to utilize tags for alerting and dashboards. 

The workshop uses a simple microservices-based application to illustrate these concepts.  Let's get started! 
