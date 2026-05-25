---
title: Splunk Observability Cloud による Cisco AI Pods の監視
linkTitle: Splunk Observability Cloud による Cisco AI Pods の監視
weight: 14
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: このハンズオンワークショップでは、Splunk Observability Cloud を使用して Cisco AI Pods を監視する方法を紹介します。Red Hat OpenShift に OpenTelemetry Collector をデプロイし、Prometheus レシーバーを使用してインフラストラクチャメトリクスを取り込み、Large Language Models (LLMs) と連携する Python サービスを監視するための APM の設定方法を学びます。
draft: false
hidden: false
---

**Cisco の AI-ready PODs** は、ハードウェアとソフトウェアの最高の技術を組み合わせて、多様なニーズに合わせた堅牢でスケーラブルかつ効率的な AI 対応インフラストラクチャを構築します。

**Splunk Observability Cloud** は、このインフラストラクチャ全体と、このスタック上で実行されているすべてのアプリケーションコンポーネントに対して包括的な可視性を提供します。

Cisco AI POD 環境向けに Splunk Observability Cloud を構成する手順は完全にドキュメント化されています（詳細は[こちら](https://github.com/signalfx/splunk-opentelemetry-examples/tree/main/collector/cisco-ai-ready-pods)を参照してください）。

ただし、Cisco AI POD 環境にアクセスしてインストール手順を練習することが常に可能とは限りません。

このワークショップでは、実際の Cisco AI POD へのアクセスを必要とせずに、Splunk Observability Cloud で Cisco AI PODs を監視するために使用されるいくつかの技術をデプロイおよび操作するハンズオン体験を提供します。以下の内容が含まれます:

* Red Hat OpenShift クラスターに **OpenTelemetry Collector** をデプロイする練習
* コレクターに **Prometheus** レシーバーを追加してインフラストラクチャメトリクスを取り込む練習
* クラスターに **Weaviate** ベクトルデータベースをデプロイする練習
* Large Language Models (LLMs) と連携する Python サービスを **OpenTelemetry** で計装する練習
* LLM と連携するアプリケーションのトレースで OpenTelemetry がキャプチャする詳細の理解

> 注: ワークショップのセットアップセクションは、ワークショップの主催者のみが実行する必要があります
