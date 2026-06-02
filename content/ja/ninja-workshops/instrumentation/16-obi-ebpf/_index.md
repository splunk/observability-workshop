---
draft: false
hidden: false
title: Zero-Code APM with OBI and eBPF
linkTitle: Zero-Code APM with OBI
weight: 16
archetype: chapter
time: 90 minutes
authors: ["Jeremy Hicks"]
description: Add full distributed tracing to apps with zero code changes using OpenTelemetry eBPF Instrumentation, streaming telemetry to Splunk Observability Cloud.
aliases:
  - /ninja-workshops/16-obi-ebpf/
---

このワークショップでは、**OpenTelemetry eBPF Instrumentation (OBI)** の威力を体験します。OBI は Linux カーネルから直接サービスを計装する、ゼロコードのアプリケーションパフォーマンスモニタリング手法です。

3 つのフェーズを順番に進め、それぞれ前のフェーズの上に積み重ねていきます。

- **Phase 0 -- Python Warm-up**: ホスト上で素の Python アプリを実行します。OBI バイナリを使用してカーネルから APM トレーシングを追加します。SDK もコード変更も不要です。
- **Phase 1 -- Docker (Before OBI)**: 3 つの多言語マイクロサービス (Node.js + Go + Go) を Docker Compose でデプロイします。APM が空であることを確認します。
- **Phase 2 -- Docker (The Magic)**: OBI コンテナを 1 つ追加します。3 つすべてのサービスで完全な分散トレースが Splunk APM に表示されます。コード変更はゼロです。
- **Phase 3 -- Kubernetes**: 同じサービスを Splunk OTel Collector Helm chart を使用して K8s にデプロイします。1 つのフラグで OBI を有効化します。同じゼロコードトレーシングを、エンタープライズグレードのオーケストレーションで実現します。

```text
Phase 0:  Python (:5150) ──── instrumented by OBI binary on host

Phase 1:  Frontend (Node.js :3000) → Order-Processor (Go :8080) → Payment-Service (Go :8081)
          ↑ infrastructure metrics only, APM is empty

Phase 2:  Same three services + one OBI container
          ↑ full distributed traces, zero code changes

Phase 3:  Same services on Kubernetes + Splunk OTel Collector Helm chart + obi.enabled=true
          ↑ same tracing, scales to any cluster
```
