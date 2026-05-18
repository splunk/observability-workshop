---
draft: false
hidden: false
title: Zero-Code APM with OBI and eBPF
linkTitle: Zero-Code APM with OBI
weight: 16
archetype: chapter
time: 90 minutes
authors: ["Jeremy Hicks"]
description: OpenTelemetry eBPF Instrumentation (OBI) がコードを一切変更せずにアプリケーションへ完全な分散トレーシングを追加し、Splunk Observability Cloud にテレメトリを送信する方法を体験するハンズオンワークショップです。
---

このワークショップでは、**OpenTelemetry eBPF Instrumentation (OBI)** のパワーを体験します。OBI は、Linux カーネルから直接サービスを計装する、コード変更不要のアプリケーションパフォーマンスモニタリング手法です。

3つのフェーズを順に進めていきます。各フェーズは前のフェーズを基に構築されています:

- **Phase 0 -- Python ウォームアップ**: ホスト上で素の Python アプリを実行します。OBI バイナリを使用してカーネルから APM トレーシングを追加します -- SDK もコード変更も不要です。
- **Phase 1 -- Docker (OBI 導入前)**: 3つのポリグロットマイクロサービス (Node.js + Go + Go) を Docker Compose でデプロイします。APM が空であることを確認します。
- **Phase 2 -- Docker (マジック)**: OBI コンテナを1つ追加します。3つのサービスすべてにわたる完全な分散トレースが Splunk APM に表示されます。コード変更はゼロです。
- **Phase 3 -- Kubernetes**: 同じサービスを K8s にデプロイし、Splunk OTel Collector Helm chart を使用します。1つのフラグで OBI を有効化します。同じコード変更不要のトレーシングを、エンタープライズグレードのオーケストレーションで実現します。

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
このワークショップを進める最も簡単な方法は以下を使用することです:

- このページの右上にある左右の矢印 (**<** | **>**)
- キーボードの左右カーソルキー
{{% /notice %}}
