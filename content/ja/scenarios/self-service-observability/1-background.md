---
title: 背景
linkTitle: 1 Background
weight: 1
time: 3 minutes
---

## 背景

詳細に入る前に、**Open Telemetry** に関するいくつかの背景概念を確認しましょう。

まず、ホストや Kubernetes ノード上に存在する **Open Telemetry Collector** があります。これらのコレクターは、ローカル情報（CPU、ディスク、メモリなど）を収集できます。また、Prometheus（プッシュまたはプル）やデータベース、その他のミドルウェアなど、他のソースからメトリクスを収集することもできます。

![OTel Diagram](../images/otel-diagram.svg?width=60vw)
Source: [OTel Documentation](https://opentelemetry.io/docs/)

**OTel Collector** がデータを収集・送信する方法は、**パイプライン** を使用します。パイプラインは以下で構成されます

* **Receivers**: 1つ以上のソースからテレメトリを収集します。プルベースまたはプッシュベースです。
* **Processors**: レシーバーからデータを受け取り、変更または変換します。レシーバーやエクスポーターとは異なり、プロセッサーは特定の順序でデータを処理します。
* **Exporters**: 1つ以上のオブザーバビリティバックエンドまたはその他の宛先にデータを送信します。

![OTel Diagram](../images/otel-collector-details.svg?width=60vw)
Source: [OTel Documentation](https://opentelemetry.io/docs/collector/)

最後のピースは、計装されたアプリケーションです。これらはトレース（スパン）、メトリクス、およびログを送信します。

デフォルトでは、計装はローカルコレクター（ホストまたは Kubernetes ノード上）にデータを送信するように設計されています。これは、どの Pod やどのノード/ホストでアプリケーションが実行されているかなどのメタデータを追加できるため、望ましい動作です。
