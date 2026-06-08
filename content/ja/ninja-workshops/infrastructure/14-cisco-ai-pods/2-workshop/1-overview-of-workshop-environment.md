---
title: ワークショップ環境の概要
linkTitle: 1. ワークショップ環境の概要
weight: 1
time: 5 minutes
---

**Cisco の AI 対応 POD** は、最先端のハードウェアとソフトウェアを組み合わせて、堅牢でスケーラブルかつ効率的な AI インフラストラクチャを提供します。
**Splunk Observability Cloud** は、インフラストラクチャからアプリケーションコンポーネントまで、このスタック全体の包括的な可視性を提供します。

このハンズオンワークショップでは、OpenTelemetry と Prometheus を使用して AI インフラストラクチャを監視する方法を学びます。**実際の Cisco AI POD へのアクセスは不要です**。現実的な環境で監視技術のデプロイと設定に関する実践的な経験を得ることができます。

## ラボ環境

このワークショップでは、AWS 上で動作する共有の **OpenShift Cluster** を使用します。このクラスターには NVIDIA GPU と NVIDIA AI Enterprise ソフトウェアが搭載されています。

### デプロイ済みのインフラストラクチャ

ワークショップのインストラクターが、以下の共有コンポーネントをワークショップ環境にデプロイしています

* **NVIDIA NIM models**:
  * `meta/llama-3.2-1b-instruct` - ユーザープロンプトを処理します
  * `nvidia/llama-3.2-nv-embedqa-1b-v2` - エンベディングを生成します
* **Weaviate** - セマンティック検索と検索のためのベクターデータベース
* **Prometheus exporter** - 本番環境の AI POD に典型的な Pure Storage メトリクスをシミュレートします

### ワークスペース

各参加者は、共有クラスター内に専用の namespace を受け取り、独立した作業のための隔離された環境が確保されます。

## ワークショップのアクティビティ

ワークショップ中に、各参加者は以下のタスクを実行します

1. 自分の namespace に **OpenTelemetry collector** をデプロイして設定する
2. クラスターインフラストラクチャとオブザーバビリティデータ収集を統合する
3. NVIDIA NIM models を活用する **Python アプリケーション**をデプロイする
4. Splunk Observability Cloud を使用してアプリケーションのパフォーマンスとインフラストラクチャメトリクスを監視する

## Prometheus とは？

**Prometheus** は通常、ストレージとアラートに使用されるフルスタック監視システムを指しますが、このワークショップでは Prometheus エコシステムのデータ標準に焦点を当てます。

**Prometheus Exporters** を活用します。これは、コンポーネントの内部ヘルス情報を標準化されたメトリクスエンドポイント（例<http://localhost:9100/metrics）に変換する小さなユーティリティです。>

フル Prometheus サーバーを使用してこのデータを収集する代わりに、**OpenTelemetry Collector** を使用します。その **Prometheus receiver** を使用することで、コレクターはこれらのエンドポイントを**スクレイプ**でき、広くサポートされている業界標準フォーマットを使用してリッチなテレメトリデータを収集できます。
