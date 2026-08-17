---
title: "Phase 3: Kubernetes"
linkTitle: 5. Kubernetes
weight: 5
archetype: chapter
time: 25 minutes
description: Deploy the same three services to Kubernetes, add the OBI DaemonSet, and get full distributed tracing same zero-code story, enterprise-grade orchestration.
---

このフェーズでは、Phase 2 とまったく同じ「素の」アプリケーションコードを使用し、[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) を使って Kubernetes にデプロイします。

Collector は Helm を通じてデプロイされ、OBI は `obi.enabled=true` という単一のフラグで有効化されます。これにより、すべてのノードのすべての Pod を計装する OBI DaemonSet がデプロイされます。
