---
title: ThousandEyes Integration with Splunk Observability Cloud
linkTitle: ThousandEyes Integration
weight: 5
archetype: chapter
authors: ["Alec Chamberlain"]
time: 120 minutes
description: Deploy ThousandEyes Enterprise Agent in Kubernetes, stream synthetic data into Splunk Observability Cloud, and enable bi-directional drilldowns between ThousandEyes and Splunk APM.
---

This workshop demonstrates integrating **ThousandEyes with Splunk Observability Cloud** to provide unified visibility across your synthetic monitoring and observability data.

## What You'll Learn

By the end of this workshop, you will:

- Deploy a ThousandEyes Enterprise Agent as a containerized workload in Kubernetes
- Deploy the included Spring PetClinic application as an internal Kubernetes test target
- Integrate ThousandEyes metrics with Splunk Observability Cloud using OpenTelemetry
- Configure distributed tracing so ThousandEyes and Splunk APM can link to the same requests
- Create synthetic tests for internal Kubernetes services and external dependencies
- Monitor test results in Splunk Observability Cloud dashboards
- Move from ThousandEyes into Splunk APM traces and back to the originating ThousandEyes test

## Sections

### Core path

- [Overview](./1-overview/_index.md) - Understand ThousandEyes agent types and architecture
- [Deployment](./2-deployment/_index.md) - Deploy the Enterprise Agent in Kubernetes
- [Splunk Integration](./3-splunk-integration/_index.md) - Stream ThousandEyes metrics into Splunk Observability Cloud
- [Distributed Tracing](./4-distributed-tracing/_index.md) - Enable supported bi-directional drilldowns between ThousandEyes and Splunk APM

### Scenario extensions

- [Kubernetes Testing](./4-kubernetes-testing/_index.md) - Create internal tests that are useful for both synthetic monitoring and trace correlation
- [RUM](./6-rum-thousandeyes/_index.md) - Correlate ThousandEyes network signals with Splunk RUM for end-user investigations

### Support

- [Troubleshooting](./5-troubleshooting/_index.md) - Common issues and solutions

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Think of this scenario as two connected integrations: the OpenTelemetry stream gets ThousandEyes metrics into Splunk, and distributed tracing gives you the reverse path back into ThousandEyes from Splunk APM.
{{% /notice %}}

## Prerequisites

- A Kubernetes cluster (v1.16+)
- RBAC permissions to deploy resources in your chosen namespace
- A ThousandEyes account with access to Enterprise Agent tokens
- A Splunk Observability Cloud account with ingest token access and permission to create an API token for APM lookups

## Benefits of Integration

By connecting ThousandEyes to Splunk Observability Cloud, you gain:

- 🔗 **Unified visibility**: Correlate synthetic test results with RUM, APM traces, and infrastructure metrics
- 📊 **Enhanced dashboards**: Visualize ThousandEyes data alongside your existing Splunk observability metrics
- 🔄 **Bi-directional drilldowns**: Move from ThousandEyes Service Map to Splunk traces and from Splunk APM back to the ThousandEyes test that generated the request
- 🚨 **Centralized alerting**: Configure alerts based on ThousandEyes test results within Splunk
- 🔍 **Root cause analysis**: Quickly identify if issues are network-related (ThousandEyes) or application-related (APM)
- 📈 **Comprehensive analytics**: Analyze synthetic monitoring trends with Splunk's powerful analytics engine
