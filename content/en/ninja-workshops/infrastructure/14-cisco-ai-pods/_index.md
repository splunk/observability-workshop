---
title: Monitoring Cisco AI Pods with Splunk Observability Cloud 
linkTitle: Monitoring Cisco AI Pods with Splunk Observability Cloud
weight: 14
archetype: chapter
time: 60 minutes
authors: ["Derek Mitchell"]
description: Deploy the OpenTelemetry Collector on Red Hat OpenShift to scrape Cisco AI Pod metrics via Prometheus, and trace the Python services calling LLMs.
draft: false
hidden: false
aliases:
  - /ninja-workshops/14-cisco-ai-pods/
---

**Cisco’s AI-ready PODs** combine the best of hardware and software technologies to create a robust, scalable, and efficient AI-ready infrastructure tailored to diverse needs.

**Splunk Observability Cloud** provides comprehensive visibility into all of this infrastructure along with all the application components that are running on this stack.

The steps to configure Splunk Observability Cloud for a Cisco AI POD environment are [fully documented](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods).

However, it's not always possible to get access to a Cisco AI POD environment to practice the installation steps.

This workshop provides hands-on experience deploying and working with several of the technologies that are used to monitor Cisco AI PODs with Splunk Observability Cloud, without requiring access to an actual Cisco AI POD.  This includes:

* Practice deploying the **OpenTelemetry Collector** in the Red Hat OpenShift cluster.
* Practice adding **Prometheus** receivers to the collector to ingest infrastructure metrics.
* Practice deploying the **Weaviate** vector database to the cluster.
* Practice instrumenting Python services that interact with Large Language Models (LLMs) with **OpenTelemetry**.
* Understanding which details which OpenTelemetry captures in the trace from applications that interact with LLMs.

> Note: the workshop setup section only needs to be executed by the workshop organizer
