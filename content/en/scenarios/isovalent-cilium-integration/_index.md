---
title: Isovalent Enterprise Platform Integration with Splunk Observability Cloud
linkTitle: Isovalent Splunk Observability Integration
weight: 6
archetype: chapter
authors: ["Alec Chamberlain"]
time: 90 minutes
description: Deploy Isovalent Enterprise Platform (Cilium, Hubble, and Tetragon) on Amazon EKS and integrate with Splunk Observability Cloud for comprehensive eBPF-based monitoring and observability.
---

This workshop demonstrates integrating **Isovalent Enterprise Platform with Splunk Observability Cloud** to provide comprehensive visibility into Kubernetes networking, security, and runtime behavior using eBPF technology.

## What You'll Learn

By the end of this workshop, you will:

- Deploy Amazon EKS with Cilium as the CNI in ENI mode
- Configure Hubble for network observability with L7 visibility
- Install Tetragon for runtime security monitoring
- Integrate eBPF-based metrics with Splunk Observability Cloud using OpenTelemetry
- Monitor network flows, security events, and infrastructure metrics in unified dashboards
- Understand eBPF-powered observability and kube-proxy replacement

## Sections

- [Overview](./1-overview/_index.md) - Understand Cilium architecture and eBPF fundamentals
- [Prerequisites](./2-prerequisites/_index.md) - Required tools and access
- [EKS Setup](./3-eks-setup/_index.md) - Create EKS cluster for Cilium
- [Cilium Installation](./4-cilium-installation/_index.md) - Deploy Cilium, Hubble, and Tetragon
- [Splunk Integration](./5-splunk-integration/_index.md) - Connect metrics to Splunk Observability Cloud
- [Verification](./6-verification/_index.md) - Validate the integration

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
This integration leverages eBPF (Extended Berkeley Packet Filter) for high-performance, low-overhead observability directly in the Linux kernel.
{{% /notice %}}

## Prerequisites

- AWS CLI configured with appropriate credentials
- kubectl, eksctl, and Helm 3.x installed
- An AWS account with permissions to create EKS clusters, VPCs, and EC2 instances
- A Splunk Observability Cloud account with access token
- Approximately 90 minutes for complete setup

## Benefits of Integration

By connecting Isovalent Enterprise Platform to Splunk Observability Cloud, you gain:

- 🔍 **Deep visibility**: Network flows, L7 protocols (HTTP, DNS, gRPC), and runtime security events
- 🚀 **High performance**: eBPF-based observability with minimal overhead
- 🔐 **Security insights**: Process monitoring, system call tracing, and network policy enforcement
- 📊 **Unified dashboards**: Cilium, Hubble, and Tetragon metrics alongside infrastructure and APM data
- ⚡ **Efficient networking**: Kube-proxy replacement and native VPC networking with ENI mode

{{% children depth="1" type="card" description="true" %}}
