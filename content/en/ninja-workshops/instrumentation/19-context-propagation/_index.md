---
draft: true
title: Manual Trace Propagation
linkTitle: Manual Trace Propagation
weight: 19
layout: chapter
time: 90 minutes
authors: ["Diana Omuoyo"]
description: Instrument a containerized Python application with Splunk OpenTelemetry, observe fragmented traces when W3C headers are stripped, and fix issue with manual context propagation.
aliases:
  - /ninja-workshops/19-context-propagation/
---

Learn how to deploy the **Splunk Distribution of the OpenTelemetry Collector**, instrument microservices with the **Splunk OpenTelemetry Python** agent, reproduce broken distributed traces when reverse proxies strip `traceparent`, and restore end-to-end trace continuity using manual context propagation—**validated in Splunk Observability Cloud**.

In this workshop, you'll get hands-on experience with the following:

- Phase 0 - Understand why W3C Trace Context breaks at header-stripping boundaries
- Phase 1 - Deploy a containerized reference architecture on **k3d** (Kubernetes)
- Phase 2 - Deploy Pythom microservice application first and validate end-to-end requests
- Phase 3 - Deploy **splunk-otel-collector** & instrument the Python services exporting data to Splunk Observability Cloud
- Phase 4 - Observe **fragmented traces** in Splunk APM (Step 1), then restore **connected traces** with manual propagation (Step 2)
- Phase 5 - Summary and cleanup

Let's get started!
