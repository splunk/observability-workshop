---
title: Ingest Processor の仕組み
linkTitle: 2. Ingest Processor の仕組み
weight: 1
---

###### システムアーキテクチャ

Ingest Processor サービスの主要コンポーネントには、Ingest Processor サービスとデータ処理をサポートする SPL2 パイプラインが含まれます。以下の図は、Ingest Processor ソリューションのコンポーネントがどのように連携するかの概要を示しています：

![Splunk Ingest Processor Architecture](../images/IngestProcessor-architecture-diagram_release_updated2.png)

###### Ingest Processor サービス

Ingest Processor サービスは、Splunk がホストするクラウドサービスです。これはデータ管理エクスペリエンスの一部であり、さまざまなデータ取り込みと処理のユースケースに対応するサービスセットです。

Ingest Processor サービスを使用して、以下のことができます：

* 各 Ingest Processor が受信したデータをどのように処理してルーティングするかを決定する SPL2 パイプラインを作成して適用する
* 処理したいデータの種類を識別し、Ingest Processor がそのデータを個別のイベントに分割およびマージする方法を決定するソースタイプを定義する
* Ingest Processor が処理済みデータを送信する宛先への接続を作成する

###### パイプライン

パイプラインは、SPL2 で記述されたデータ処理命令のセットです。パイプラインを作成する際、どのデータを処理するか、どのように処理するか、結果をどこに送信するかを指定する専用の SPL2 ステートメントを記述します。パイプラインを適用すると、Ingest Processor はそれらの命令を使用して、Splunk フォワーダー、HTTP クライアント、ロギングエージェントなどのデータソースから受信したすべてのデータを処理します。

各パイプラインは、Ingest Processor が受信するすべてのデータのサブセットを選択して処理します。たとえば、受信データからソースタイプ `cisco_syslog` のイベントを選択し、Splunk Cloud Platform の指定されたインデックスに送信するパイプラインを作成できます。この選択されたデータのサブセットはパーティションと呼ばれます。詳細については、[Partitions](http://docs.splunk.com/Documentation/SplunkCloud/latest/IngestProcessor/Architecture#Partitions) を参照してください。

Ingest Processor ソリューションは、`IngestProcessor` プロファイルの一部であるコマンドと関数のみをサポートしています。Ingest Processor 用のパイプラインを記述するために使用できる特定の SPL2 コマンドと関数の詳細については、[Ingest Processor pipeline syntax](http://docs.splunk.com/Documentation/SplunkCloud/latest/IngestProcessor/PipelinesOverview) を参照してください。`IngestProcessor` プロファイルが他の SPL2 プロファイルと比較して異なるコマンドと関数をどのようにサポートするかの概要については、*SPL2 Search Reference* の以下のページを参照してください：

* [Compatibility Quick Reference for SPL2 commands](http://docs.splunk.com/Documentation/SCS/current/SearchReference/CompatibilityQuickReferenceforSPL2commands)
* [Compatibility Quick Reference for SPL2 evaluation functions](http://docs.splunk.com/Documentation/SCS/current/SearchReference/CompatibilityQuickReferenceforSPL2evaluationfunctions)
