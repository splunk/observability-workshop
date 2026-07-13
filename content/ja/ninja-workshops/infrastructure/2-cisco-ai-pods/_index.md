---
title: Cisco AI Podsのモニタリング
weight: 2
archetype: chapter
time: 60 minutes
authors: ["Derek Mitchell"]
description: Red Hat OpenShift上にOpenTelemetry Collectorをデプロイし、Prometheusを使用してCisco AI Podのメトリクスを収集し、LLMを呼び出すPythonサービスをトレースします。
draft: false
hidden: false
aliases:
  - /ninja-workshops/14-cisco-ai-pods/
product: "Observability Cloud"
---

**Cisco AI-ready PODs** は、ハードウェアとソフトウェアの最高の技術を組み合わせ、多様なニーズに対応する堅牢でスケーラブルかつ効率的なAI対応インフラストラクチャを提供します。

**Splunk Observability Cloud** は、このインフラストラクチャ全体と、このスタック上で稼働するすべてのアプリケーションコンポーネントに対する包括的な可視性を提供します。

Cisco AI POD環境向けにSplunk Observability Cloudを構成する手順は[完全にドキュメント化されています](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods)。

しかし、インストール手順を実践するためにCisco AI POD環境にアクセスできるとは限りません。

このワークショップでは、実際のCisco AI PODへのアクセスを必要とせずに、Splunk Observability CloudでCisco AI PODsを監視するために使用される複数の技術のデプロイと操作を実践的に体験できます。内容は以下の通りです

* Red Hat OpenShiftクラスターに **OpenTelemetry Collector** をデプロイする練習
* Collectorに **Prometheus** Receiverを追加してインフラストラクチャメトリクスを取り込む練習
* クラスターに **Weaviate** ベクターデータベースをデプロイする練習
* 大規模言語モデル（LLM）と連携するPythonサービスを **OpenTelemetry** で計装する練習
* LLMと連携するアプリケーションからOpenTelemetryがトレースでキャプチャする詳細の理解

> [!NOTE]
> ワークショップのセットアップセクションは、ワークショップの主催者のみが実行する必要があります
