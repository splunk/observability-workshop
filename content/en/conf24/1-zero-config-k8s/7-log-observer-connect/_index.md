---
title: Introduction
linkTitle: 7. Log Observer
weight: 8
archetype: chapter
---

Until this point, we have not touched or changed our code, yet we did receive Trace & Profiling/DB Query performance information.
If we want to get more out of our Java application, we can introduce a small change to our application log setup.

This change will configure the Spring PetClinic application to use an OpenTelemetry-based format to write logs, This will allow the Auto-Instrumentation to add OpenTelemetry relevant information into the logs.

The **Splunk Log Observer** component is used to view the logs and with this information can automatically relate log information with APM Services and Traces. This feature called **Related Content** will also work with Infrastructure.

Let's grab the actual code for the application now.
