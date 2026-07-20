---
title: はじめに
linkTitle: 1. はじめに
weight: 1
---

この _**テクニカル**_ Ingest Processor[^1] for Splunk Observability Cloudワークショップでは、Splunk Enterprise CloudのIngest Processorをハンズオン形式で体験できます。

ワークショップモジュールを簡素化するために、事前設定済みのSplunk Enterprise Cloudインスタンスが提供されます。

このインスタンスには、Ingest Processorパイプラインを作成するためのすべての要件が事前に設定されています。

このワークショップでは、Ingest Processorを使用してログをメトリクスに変換し、そのメトリクスをSplunk Observability Cloudに送信する利点を紹介します。このテクニカルワークショップを終了する頃には、Splunk Enterprise CloudにおけるIngest Processorの主要な機能についての理解が深まり、Ingest ProcessorパイプラインのDestinationとしてSplunk Observability Cloudを使用する価値を把握できるようになります。

事前設定済みの [Splunk Enterprise Cloud](./1-access-cloud-instances/) インスタンスへのアクセス方法はこちらです。

![Splunk Ingest Processor Architecture](../images/IngestProcessor-architecture-diagram_release_updated2.png)

[^1]: [**Ingest Processor**](https://docs.splunk.com/Documentation/SplunkCloud/9.3.2408/IngestProcessor/AboutIngestProcessorSolution) は、Splunk Cloud Platformデプロイメント内で動作するデータ処理機能です。Ingest Processorを使用して、データフローの設定、データ形式の制御、インデックス作成前の変換ルールの適用、およびDestinationへのルーティングを行います。
