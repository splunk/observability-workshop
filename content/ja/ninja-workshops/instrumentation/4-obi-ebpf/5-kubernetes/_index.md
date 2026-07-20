---
title: "Phase 3: Kubernetes"
linkTitle: 5. Kubernetes
weight: 5
archetype: chapter
time: 25 minutes
description: 同じ3つのサービスをKubernetesにデプロイし、OBI DaemonSetを追加して完全な分散トレーシングを取得します。コード変更不要のまま、エンタープライズグレードのオーケストレーションを実現します。
---

このフェーズでは、Phase 2とまったく同じ「素の」アプリケーションコードを [Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart) を使用してKubernetesにデプロイします。

CollectorはHelmを通じてデプロイされ、OBIは `obi.enabled=true` という単一のフラグで有効化されます。これにより、すべてのノードのすべてのPodを計装するOBI DaemonSetがデプロイされます。
