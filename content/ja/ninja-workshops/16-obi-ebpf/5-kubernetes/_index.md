---
title: "Phase 3: Kubernetes"
linkTitle: 5. Kubernetes
weight: 5
archetype: chapter
time: 25分
description: 同じ3つのサービスをKubernetesにデプロイし、OBI DaemonSetを追加して、完全な分散トレーシングを取得します -- コード変更不要のまま、エンタープライズグレードのオーケストレーションを実現します。
---

このフェーズでは、Phase 2とまったく同じ「素の」アプリケーションコードを使用し、[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart)を使ってKubernetesにデプロイします。

コレクターはHelmでデプロイされ、OBIは単一のフラグ `obi.enabled=true` で有効化されます。これにより、OBI DaemonSetがデプロイされ、すべてのノード上のすべてのPodが計装されます。
