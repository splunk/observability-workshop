---
title: Introduction
weight: 2
---

The Splunk OpenTelemetry Workshop will teach you how to level up your Observability practice by using the OpenTelemetry Collector and APM Instrumentation to emit industry standard telemetry from your infrastructure and applications.

Source repo is here: [https://github.com/signalfx/otelworkshop](https://github.com/signalfx/otelworkshop)

## Requirements

### Audience

- Intermediate and advanced developers, devops, and SREs who have already set up their Splunk Observability Cloud account and have tried out integrations and dashboards Skill level should include setting up and troubleshooting Linux and Kubernetes environments as well as deploying applications written in current versions of Java, Python, Node.
- This workshop is designed to run as a single user, or be run in a small group (upwards of 6) along with a leader guiding the group.
- If running as a group, a pre-workshop prep call is necessary to ensure that all group members can spin up and/or access an Ubuntu Linux lab environment. Details are below.

### Prerequisites

- Completion of [Splunk Observability Workshop](https://signalfx.github.io/observability-workshop/latest/) which trains on using metrics/APM and charts/dashboards/alerts or equivalent devops/SRE skills
- Splunk Observability Cloud Account
- Ability to use a multi-terminal IDE i.e. Microsoft Visual Studio Code or equivalent
- Ability to spin up a VM or access a host with a Debian Linux environment with the following specs: Debian (i.e. Ubuntu) Linux environment with minimum 12G RAM and 20G disk w/ lightweight Kubernetes (Rancher k3s) installed OR your own k8s cluster. The Prep section has some tools to help build a local or AWS environment.

## Document Conventions

Variables from your Splunk Observability account are displayed like this: YOURVARIABLEHERE.
I.e. to change your REALM to `us1` change `api.YOURREALMHERE.signalfx.com` to `api.us1.signalfx.com`  

- K8s = Kubernetes
- K3s = a lightweight Kubernetes from [Rancher](https://www.k3s.io)
- signalfx = Splunk Observability domain name/endpoint/technology name
- otel = OpenTelemetry

## Workshop Agenda

- (Optional) Build a local Lab Environment Ubuntu Sandbox on Mac or Windows
- OpenTelemetry Collector and APM Labs
  - Linux Host
    - Set up OpenTelemetry Collector Agent on a Linux Host
    - OpenTelemetry APM Instrumentation on Java, Python, and Node apps
  - Kubernetes (k8s) [Click to start at k8s labs](../apm/k8s)
    - Set up OpenTelemetry Collector Agent on a k8s cluster
    - OpenTelemetry APM Instrumentation on k8s on Java, Python k8s pods
    - Manual APM Instrumentation for Java
    - JVM Metrics
    - Span processing with redaction example
    - APM for Istio service mesh
    - OpenTelemetry Collector configuration / troubleshooting
    - Prometheus scraping and custom metrics
    - Collectd: receive metrics from any platform
    - Troubleshooting the Collector
  - Option: Docker workshop w/ Otel Collector and APM Examples

## Disclaimers

- This is not product documentation: [Click for Official documentation](https://docs.splunk.com/Observability)
- Breaking changes to OpenTelemetry and Splunk services may occur- please submit issues on the GitHub repo if any are encountered
- These examples are not commercial products and are for experimentation and educational purposes only