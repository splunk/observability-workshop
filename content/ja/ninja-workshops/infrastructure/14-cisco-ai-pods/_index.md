---
title: Cisco AI Pods の監視
weight: 14
archetype: chapter
time: 60 minutes
authors: ["Derek Mitchell"]
description: Red Hat OpenShift 上に OpenTelemetry Collector をデプロイし、Prometheus 経由で Cisco AI Pod メトリクスを収集し、LLM を呼び出す Python サービスをトレースします。
draft: false
hidden: false
aliases:
  - /ninja-workshops/14-cisco-ai-pods/
product: "Observability Cloud"
---

**Cisco の AI 対応 POD** は、ハードウェアとソフトウェアの最先端技術を組み合わせ、多様なニーズに対応する堅牢でスケーラブルかつ効率的な AI 対応インフラストラクチャを提供します。

**Splunk Observability Cloud** は、このインフラストラクチャ全体と、このスタック上で実行されるすべてのアプリケーションコンポーネントに対する包括的な可視性を提供します。

Cisco AI POD 環境向けに Splunk Observability Cloud を設定する手順は[完全にドキュメント化されています](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods)。

ただし、インストール手順を練習するために Cisco AI POD 環境にアクセスできるとは限りません。

このワークショップでは、実際の Cisco AI POD にアクセスすることなく、Splunk Observability Cloud で Cisco AI POD を監視するために使用されるいくつかの技術をデプロイおよび操作する実践的な経験を提供します。以下の内容が含まれます

* Red Hat OpenShift クラスターへの **OpenTelemetry Collector** のデプロイを練習します。
* インフラストラクチャメトリクスを取り込むための **Prometheus** レシーバーのコレクターへの追加を練習します。
* クラスターへの **Weaviate** ベクトルデータベースのデプロイを練習します。
* 大規模言語モデル（LLM）と対話する Python サービスの **OpenTelemetry** による計装を練習します。
* LLM と対話するアプリケーションからのトレースで OpenTelemetry がキャプチャする詳細情報を理解します。

> [!NOTE]
> ワークショップのセットアップセクションは、ワークショップの主催者のみが実行する必要があります
