---
draft: false
hidden: true
title: OBI と eBPF によるゼロコード APM
linkTitle: OBI によるゼロコード APM
weight: 16
archetype: chapter
time: 90 minutes
authors: ["Jeremy Hicks"]
description: OpenTelemetry eBPF Instrumentation（OBI）が、コードを一行も変更することなくアプリケーションに完全な分散トレーシングを追加し、Splunk Observability Cloud にテレメトリーを送信する方法を実践的に学ぶワークショップです。
---

このワークショップでは、**OpenTelemetry eBPF Instrumentation（OBI）** のパワーを体験します。これは、Linux カーネルから直接サービスを計装するゼロコードのアプリケーションパフォーマンスモニタリング手法です。

3つのフェーズを順に進めていきます。各フェーズは前のフェーズの上に構築されます

- **Phase 0 -- Python ウォームアップ**: ホスト上でシンプルな Python アプリを実行します。OBI バイナリを使用してカーネルから APM トレーシングを追加します。SDK もコード変更も不要です。
- **Phase 1 -- Docker（OBI 導入前）**: Docker Compose で3つのポリグロットマイクロサービス（Node.js + Go + Go）をデプロイします。APM が空であることを確認します。
- **Phase 2 -- Docker（マジック）**: OBI コンテナを1つ追加します。3つのサービスすべてで完全な分散トレースが Splunk APM に表示されます。コード変更はゼロです。
- **Phase 3 -- Kubernetes**: 同じサービスを Splunk OTel Collector Helm チャートとともに K8s にデプロイします。1つのフラグで OBI を有効にします。同じゼロコードトレーシングで、エンタープライズグレードのオーケストレーションが実現します。

```text
Phase 0:  Python (:5150) ──── instrumented by OBI binary on host

Phase 1:  Frontend (Node.js :3000) → Order-Processor (Go :8080) → Payment-Service (Go :8081)
          ↑ infrastructure metrics only, APM is empty

Phase 2:  Same three services + one OBI container
          ↑ full distributed traces, zero code changes

Phase 3:  Same services on Kubernetes + Splunk OTel Collector Helm chart + obi.enabled=true
          ↑ same tracing, scales to any cluster
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
このワークショップを進める最も簡単な方法は以下を使用することです

- このページの右上にある左右の矢印（**<** | **>**）
- キーボードの左右カーソルキー
{{% /notice %}}
