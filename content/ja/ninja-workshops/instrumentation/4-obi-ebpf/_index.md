---
title: OBIとeBPFによるゼロコードAPM
linkTitle: OBIによるゼロコードAPM
weight: 4
time: 90分
authors: ["Jeremy Hicks"]
description: OpenTelemetry eBPF Instrumentationを使用して、コード変更なしでアプリケーションに完全な分散トレーシングを追加し、Splunk Observability Cloudにテレメトリをストリーミングします。
aliases:
  - /ninja-workshops/16-obi-ebpf/
---

このワークショップでは、 **OpenTelemetry eBPF Instrumentation（OBI）** のパワーを体験します。これはLinuxカーネルから直接サービスを計装する、ゼロコードのアプリケーションパフォーマンスモニタリングアプローチです。

3つのフェーズを順に進めていきます。各フェーズは前のフェーズの上に構築されます。

- **Phase 0 -- Python Warm-up**: ホスト上で素のPythonアプリを実行します。OBIバイナリを使用してカーネルからAPMトレーシングを追加します。SDKもコード変更も不要です。
- **Phase 1 -- Docker（OBI導入前）**: Docker Composeで3つのポリグロットマイクロサービス（Node.js + Go + Go）をデプロイします。APMが空であることを確認します。
- **Phase 2 -- Docker（The Magic）**: OBIコンテナを1つ追加します。3つのサービスすべてでSplunk APMに完全な分散トレースが表示されます。コード変更はゼロです。
- **Phase 3 -- Kubernetes**: 同じサービスをK8sにデプロイし、Splunk OTel Collector Helmチャートを使用します。1つのフラグでOBIを有効にします。同じゼロコードトレーシングで、エンタープライズグレードのオーケストレーションを実現します。

```text
Phase 0:  Python (:5150) ──── instrumented by OBI binary on host

Phase 1:  Frontend (Node.js :3000) → Order-Processor (Go :8080) → Payment-Service (Go :8081)
          ↑ infrastructure metrics only, APM is empty

Phase 2:  Same three services + one OBI container
          ↑ full distributed traces, zero code changes

Phase 3:  Same services on Kubernetes + Splunk OTel Collector Helm chart + obi.enabled=true
          ↑ same tracing, scales to any cluster
```
