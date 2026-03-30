---
draft: true
title: Zero-Code APM with OBI and eBPF
linkTitle: Zero-Code APM with OBI
weight: 16
archetype: chapter
time: 90 minutes
authors: ["Jeremy Hicks"]
description: OpenTelemetry eBPF Instrumentation (OBI) がコードを一行も変更せずにアプリケーションに完全な分散トレーシングを追加し、Splunk Observability Cloud にテレメトリを送信する方法を実演するハンズオンワークショップです。
---

このワークショップでは、**OpenTelemetry eBPF Instrumentation (OBI)** の威力を体験します。これは、Linuxカーネルから直接サービスを計装するゼロコードのアプリケーションパフォーマンス監視アプローチです。

以下の3つのフェーズを順番に進めていきます。各フェーズは前のフェーズの上に構築されています：

- **Phase 0 -- Python Warm-up**: ホスト上でシンプルなPythonアプリを実行します。OBIバイナリを使用してカーネルからAPMトレーシングを追加します -- SDKもコード変更も不要です。
- **Phase 1 -- Docker (Before OBI)**: Docker Composeで3つのポリグロットマイクロサービス (Node.js + Go + Go) をデプロイします。APMが空であることを確認します。
- **Phase 2 -- Docker (The Magic)**: OBIコンテナを1つ追加します。3つのサービスすべてで完全な分散トレースがSplunk APMに表示されます。コード変更はゼロです。
- **Phase 3 -- Kubernetes**: Splunk OTel Collector Helm chartを使用して同じサービスをK8sにデプロイします。1つのフラグでOBIを有効にします。同じゼロコードトレーシングを、エンタープライズグレードのオーケストレーションで実現します。

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
このワークショップ内の移動には以下の方法が便利です：

- このページの右上にある左右の矢印 (**<** | **>**)
- キーボードの左右カーソルキー
{{% /notice %}}
