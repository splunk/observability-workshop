---
title: "Phase 3: Kubernetes"
linkTitle: 5. Kubernetes
weight: 5
archetype: chapter
time: 25 minutes
description: 同じ3つのサービスをKubernetesにデプロイし、OBI DaemonSetを追加することで、完全な分散トレーシングを実現します。ゼロコードのまま、エンタープライズグレードのオーケストレーションを利用できます。
---

このフェーズでは、Phase 2で使用した「素の」アプリケーションコードをそのまま流用し、[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart)を使用してKubernetesにデプロイします。

CollectorはHelmでデプロイされ、`obi.enabled=true`という単一のフラグでOBIを有効化することで、すべてのノード上のすべてのPodをインストルメントするOBI DaemonSetがデプロイされます。
