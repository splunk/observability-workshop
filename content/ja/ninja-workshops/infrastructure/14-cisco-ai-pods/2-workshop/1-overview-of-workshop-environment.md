---
title: ワークショップ環境の概要
linkTitle: 1. ワークショップ環境の概要
weight: 1
time: 5 minutes
---

**Cisco's AI-ready PODs** は、最先端のハードウェアとソフトウェアを組み合わせ、
堅牢でスケーラブル、かつ効率的なAIインフラストラクチャを提供します。
**Splunk Observability Cloud** は、インフラストラクチャからアプリケーションコンポーネントに至るまで、
このスタック全体を包括的に可視化します。

このハンズオンワークショップでは、OpenTelemetryとPrometheusを使用してAIインフラストラクチャを監視する方法を、
**実際のCisco AI PODへのアクセスを必要とせずに** 学習します。
現実的な環境で監視技術をデプロイし設定する実践的な経験を得られます。

## ラボ環境

このワークショップでは、AWS上で動作する共有 **OpenShift Cluster** を使用します。
このクラスターはNVIDIA GPUおよびNVIDIA AI Enterpriseソフトウェアを備えています。

### 事前デプロイ済みのインフラストラクチャ

ワークショップのインストラクターは、以下の共有コンポーネントをワークショップ環境にデプロイ済みです:

* **NVIDIA NIM models**:
  * `meta/llama-3.2-1b-instruct` - ユーザープロンプトを処理します
  * `nvidia/llama-3.2-nv-embedqa-1b-v2` - エンベディングを生成します
* **Weaviate** - セマンティック検索と取得のためのベクトルデータベースです
* **Prometheus exporter** - 本番AI PODに典型的なPure Storageメトリクスをシミュレートします

### あなたのワークスペース

各参加者には共有クラスター内に専用の名前空間が割り当てられ、
独立した作業のための分離された環境が確保されます。

## ワークショップのアクティビティ

ワークショップの中で、各参加者は以下のタスクを実行します:

1. 自分の名前空間に **OpenTelemetry collector** をデプロイして設定します
2. クラスターインフラストラクチャとオブザーバビリティデータ収集を統合します
3. NVIDIA NIM modelsを活用する **Python application** をデプロイします
4. Splunk Observability Cloudを使用してアプリケーションのパフォーマンスとインフラストラクチャメトリクスを監視します

## Prometheusとは

**Prometheus** は通常、ストレージとアラート用途に使われるフルスタックの監視システムを指しますが、
このワークショップではPrometheusエコシステムのデータ標準に焦点を当てます。

ここでは **Prometheus Exporters** を活用します。これは、コンポーネントの内部状態を標準化された
メトリクスエンドポイント (例: <http://localhost:9100/metrics>) に変換する小さなユーティリティです。

このデータの収集にPrometheusサーバー全体を使用する代わりに、
**OpenTelemetry Collector** を使用します。コレクターの **Prometheus receiver** を使うことで、
これらのエンドポイントを **scrape** することができ、広くサポートされた業界標準フォーマットを用いて
豊富なテレメトリデータを収集できます。
