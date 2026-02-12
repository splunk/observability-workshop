---
title: Splunk Observability Cloud による Cisco AI Pods のモニタリング
linkTitle: Splunk Observability Cloud による Cisco AI Pods のモニタリング
weight: 14
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: This hands-on workshop demonstrates how to monitor Cisco AI Pods with Splunk Observability Cloud. Learn to deploy the OpenTelemetry Collector in Red Hat OpenShift, ingest infrastructure metrics using Prometheus receivers, and configure APM to monitor Python services that interact with Large Language Models (LLMs).
draft: false
hidden: false
---

**Cisco の AI 対応 PODs** は、ハードウェアとソフトウェアの最高の技術を組み合わせ、多様なニーズに合わせた堅牢でスケーラブルかつ効率的な AI 対応インフラストラクチャを構築します。

**Splunk Observability Cloud** は、このインフラストラクチャ全体と、このスタック上で実行されるすべてのアプリケーションコンポーネントに対する包括的な可視性を提供します。

Cisco AI POD 環境向けに Splunk Observability Cloud を構成する手順は完全に文書化されています（詳細は [こちら](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods) を参照してください）。

ただし、インストール手順を練習するために Cisco AI POD 環境にアクセスできるとは限りません。

このワークショップでは、実際の Cisco AI POD にアクセスすることなく、Splunk Observability Cloud で Cisco AI PODs をモニタリングするために使用されるいくつかの技術をデプロイし、操作するハンズオン体験を提供します。以下の内容が含まれます：

* Red Hat OpenShift クラスターへの **OpenTelemetry Collector** のデプロイを練習します。
* インフラストラクチャメトリクスを取り込むために、コレクターに **Prometheus** レシーバーを追加する練習をします。
* クラスターへの **Weaviate** ベクトルデータベースのデプロイを練習します。
* 大規模言語モデル（LLM）と連携する Python サービスを **OpenTelemetry** でインストルメントする練習をします。
* LLM と連携するアプリケーションのトレースで OpenTelemetry がキャプチャする詳細情報を理解します。

> 注意：ワークショップセットアップセクションは、ワークショップ主催者のみが実行する必要があります

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
このワークショップを最も簡単にナビゲートする方法は以下の通りです：

* このページの右上にある左右の矢印（ **<** | **>** ）を使用する
* キーボードの左（◀️）および右（▶️）カーソルキーを使用する
  {{% /notice %}}
