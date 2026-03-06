---
title: "Phase 3: Kubernetes"
linkTitle: 5. Kubernetes
weight: 5
archetype: chapter
time: 25 minutes
description: Deploy the same three services to Kubernetes, add the OBI DaemonSet, and get full distributed tracing -- same zero-code story, enterprise-grade orchestration.
---

This phase takes the exact same "naked" application code from Phase 2 and deploys it to Kubernetes using the [Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart).

The collector is deployed via Helm, and OBI is enabled with a single flag -- `obi.enabled=true` -- which deploys the OBI DaemonSet to instrument every pod on every node.
