---
title: はじめに
linkTitle: 1. はじめに
weight: 1
---

この _**テクニカル**_ なSplunk Observability Cloud向けIngest Processor[^1] ワークショップでは、Splunk Enterprise CloudでIngest Processorを実際に操作する機会があります。

ワークショップモジュールを簡素化するために、事前設定されたSplunk Enterprise Cloudインスタンスが提供されます。

このインスタンスは、Ingest Processorパイプラインを作成するためのすべての要件が事前に設定されています。

このワークショップでは、Ingest Processorを使用して充実したログをメトリクスに変換し、それらのメトリクスをSplunk Observability Cloudに送信するメリットを紹介します。このテクニカルワークショップを終える頃には、Splunk Enterprise CloudにおけるIngest Processorの主要な機能と能力、およびIngest Processorパイプライン内の宛先としてSplunk Observability Cloudを使用する価値について十分に理解できるようになります。

事前設定された [Splunk Enterprise Cloud](./1-access-cloud-instances/) インスタンスにアクセスする方法については、以下の手順を参照してください。

![Splunk Ingest Processor Architecture](../images/IngestProcessor-architecture-diagram_release_updated2.png)

[^1]: [**Ingest Processor**](https://docs.splunk.com/Documentation/SplunkCloud/9.3.2408/IngestProcessor/AboutIngestProcessorSolution) は、Splunk Cloud Platformデプロイメント内で動作するデータ処理機能です。Ingest Processorを使用して、データフローの設定、データ形式の制御、インデックス作成前の変換ルールの適用、および宛先へのルーティングを行います。
