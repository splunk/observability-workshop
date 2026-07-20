---
title: Cisco AI Podsのモニタリング
weight: 1
time: 60 minutes
authors: ["Derek Mitchell"]
description: Red Hat OpenShift上にOpenTelemetry Collectorをデプロイし、Prometheusを介してCisco AI Podメトリクスをスクレイピングし、LLMを呼び出すPythonサービスをトレースします。
aliases:
  - /ninja-workshops/14-cisco-ai-pods/
product: "Observability Cloud"
---

**Cisco AI-ready PODs** は、ハードウェアとソフトウェアの最高の技術を組み合わせ、多様なニーズに対応する堅牢でスケーラブルかつ効率的なAI対応インフラストラクチャを構築します。

**Splunk Observability Cloud** は、このインフラストラクチャ全体と、このスタック上で実行されるすべてのアプリケーションコンポーネントに対する包括的な可視性を提供します。

Cisco AI POD環境向けにSplunk Observability Cloudを構成する手順は[完全にドキュメント化されています](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods)。

しかし、インストール手順を練習するためにCisco AI POD環境にアクセスできるとは限りません。

このワークショップでは、実際のCisco AI PODへのアクセスを必要とせずに、Splunk Observability CloudでCisco AI PODsをモニタリングするために使用されるいくつかの技術をデプロイし、操作するハンズオン体験を提供します。内容は以下の通りです

* Red Hat OpenShiftクラスターに **OpenTelemetry Collector** をデプロイする練習
* インフラストラクチャメトリクスを取り込むためにCollectorに **Prometheus** Receiverを追加する練習
* クラスターに **Weaviate** ベクターデータベースをデプロイする練習
* 大規模言語モデル（LLM）と対話するPythonサービスを **OpenTelemetry** で計装する練習
* LLMと対話するアプリケーションからOpenTelemetryがトレースでキャプチャする詳細の理解

> [!NOTE]
> ワークショップのセットアップセクションは、ワークショップの主催者のみが実行する必要があります
