---
title: Overview of the Workshop Environment
linkTitle: 1. Overview of the Workshop Environment
weight: 1
time: 5 minutes
---

**Cisco's AI-ready PODs** combine cutting-edge hardware and software to 
deliver a robust, scalable, and efficient AI infrastructure. 
**Splunk Observability Cloud** provides comprehensive visibility 
into this entire stack: from infrastructure to application components.

This hands-on workshop teaches you how to monitor AI infrastructure 
using OpenTelemetry and Prometheus, **without requiring 
access to an actual Cisco AI POD**. You'll gain practical experience 
deploying and configuring monitoring technologies in a realistic environment.

## Lab Environment

The workshop uses a shared **OpenShift Cluster** running in AWS, equipped 
with NVIDIA GPUs and NVIDIA AI Enterprise software. 

### Pre-Deployed Infrastructure

The workshop instructor has deployed the following shared components to the 
workshop environment: 

* **NVIDIA NIM models**:
  * `meta/llama-3.2-1b-instruct` - Processes user prompts
  * `nvidia/llama-3.2-nv-embedqa-1b-v2` - Generates embeddings
* **Weaviate** - A vector database for semantic search and retrieval
* **Prometheus exporter** - Simulates Pure Storage metrics typical of production AI PODs

### Your Workspace

Each participant receives a dedicated namespace within the shared cluster, 
ensuring isolated environments for independent work.

## Workshop Activities

During the workshop, each participant will execute the following tasks: 

1. Deploy and configure an **OpenTelemetry collector** in your namespace
2. Integrate observability data collection with the cluster infrastructure
3. Deploy a **Python application** that leverages the NVIDIA NIM models
4. Monitor application performance and infrastructure metrics using Splunk Observability Cloud

## What is Prometheus?

While **Prometheus** typically refers to a full-stack monitoring system 
used for storage and alerting, this workshop focuses on the Prometheus 
ecosystem's data standards.

We will be leveraging **Prometheus Exporters**, which are small utilities 
that translate a component's internal health into a standardized 
metrics endpoint (e.g., http://localhost:9100/metrics). 

Instead of using a full Prometheus server to collect this data, we will use 
the **OpenTelemetry Collector**. By using its **Prometheus receiver**, 
the collector can **scrape** these endpoints, allowing us to gather 
rich telemetry data using a widely-supported industry format.


