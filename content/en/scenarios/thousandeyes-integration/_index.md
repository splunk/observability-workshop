---
title: ThousandEyes Integration with Splunk Observability Cloud
linkTitle: ThousandEyes Integration
weight: 5
archetype: chapter
authors: ["Alec Chamberlain"]
time: 90 minutes
description: Deploy ThousandEyes Enterprise Agent in Kubernetes and integrate synthetic monitoring data with Splunk Observability Cloud for unified visibility across your infrastructure.
---

This workshop demonstrates integrating **ThousandEyes with Splunk Observability Cloud** to provide unified visibility across your synthetic monitoring and observability data.

## What You'll Learn

By the end of this workshop, you will:

- Deploy a ThousandEyes Enterprise Agent as a containerized workload in Kubernetes
- Integrate ThousandEyes metrics with Splunk Observability Cloud using OpenTelemetry
- Create synthetic tests for internal Kubernetes services and external dependencies
- Monitor test results in Splunk Observability Cloud dashboards
- Correlate synthetic test data with APM traces and infrastructure metrics

## Sections

- [Overview](./1-overview/_index.md) - Understand ThousandEyes agent types and architecture
- [Deployment](./2-deployment/_index.md) - Deploy the Enterprise Agent in Kubernetes
- [Splunk Integration](./3-splunk-integration/_index.md) - Connect ThousandEyes to Splunk Observability Cloud
- [Kubernetes Testing](./4-kubernetes-testing/_index.md) - Monitor internal services and replicate AppDynamics test recommendations
- [Troubleshooting](./5-troubleshooting/_index.md) - Common issues and solutions

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
This integration enables you to correlate synthetic test results with real user monitoring (RUM), APM traces, and infrastructure metrics for comprehensive root cause analysis.
{{% /notice %}}

## Prerequisites

- A Kubernetes cluster (v1.16+)
- RBAC permissions to deploy resources in your chosen namespace
- A ThousandEyes account with access to Enterprise Agent tokens
- A Splunk Observability Cloud account with ingest token access

## Benefits of Integration

By connecting ThousandEyes to Splunk Observability Cloud, you gain:

- 🔗 **Unified visibility**: Correlate synthetic test results with RUM, APM traces, and infrastructure metrics
- 📊 **Enhanced dashboards**: Visualize ThousandEyes data alongside your existing Splunk observability metrics
- 🚨 **Centralized alerting**: Configure alerts based on ThousandEyes test results within Splunk
- 🔍 **Root cause analysis**: Quickly identify if issues are network-related (ThousandEyes) or application-related (APM)
- 📈 **Comprehensive analytics**: Analyze synthetic monitoring trends with Splunk's powerful analytics engine

{{% children depth="1" type="card" description="true" %}}
