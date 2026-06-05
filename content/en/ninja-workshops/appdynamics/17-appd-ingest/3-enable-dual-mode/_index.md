---
title: "Phase 2: Enable Dual Signal Mode"
linkTitle: 3. Enable Dual Mode
weight: 3
archetype: chapter
time: 15 minutes
description: Install the OpenTelemetry Collector, enable dual signal mode on the AppDynamics agent, and verify traces appear in both AppDynamics and Splunk Observability Cloud.
---

In this phase you will deploy an OpenTelemetry Collector to forward data to Splunk Observability Cloud, then restart the application with dual signal mode enabled.  

The same agent that was sending data only to AppDynamics will now send to both destinations simultaneously.
