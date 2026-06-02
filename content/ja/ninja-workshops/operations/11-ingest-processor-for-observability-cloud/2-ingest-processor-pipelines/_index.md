---
title: Ingest Processor の仕組み
linkTitle: 2. Ingest Processor の仕組み
weight: 1
---

###### システムアーキテクチャ

Ingest Processor サービスの主要コンポーネントには、Ingest Processor サービスと、データ処理をサポートする SPL2 パイプラインが含まれます。次の図は、Ingest Processor ソリューションのコンポーネントがどのように連携して動作するかの概要を示しています。

![Splunk Ingest Processor Architecture](../images/IngestProcessor-architecture-diagram_release_updated2.png)

###### Ingest Processor サービス

Ingest Processor サービスは、Splunk がホストするクラウドサービスです。これはデータ管理エクスペリエンスの一部であり、さまざまなデータ取り込みおよび処理のユースケースを実現する一連のサービスです。

Ingest Processor サービスを使用して、次のことが行えます。

* 各 Ingest Processor が受信したデータをどのように処理しルーティングするかを決定する SPL2 パイプラインを作成および適用する。
* 処理したいデータの種類を識別するソースタイプを定義し、Ingest Processor がそのデータをどのように個別のイベントに分割・結合するかを決定する。
* Ingest Processor が処理済みのデータを送信する宛先への接続を作成する。

###### パイプライン

パイプラインは、SPL2 で記述された一連のデータ処理命令です。パイプラインを作成する際には、どのデータを処理するか、どのように処理するか、結果をどこに送信するかを指定する専用の SPL2 ステートメントを記述します。パイプラインを適用すると、Ingest Processor は Splunk フォワーダー、HTTP クライアント、ロギングエージェントなどのデータソースから受信するすべてのデータを、その命令に従って処理します。

各パイプラインは、Ingest Processor が受信するすべてのデータのサブセットを選択して処理します。たとえば、受信データの中からソースタイプが `cisco_syslog` のイベントを選択し、Splunk Cloud Platform の指定したインデックスに送信するパイプラインを作成できます。この選択されたデータのサブセットをパーティションと呼びます。詳細については、[Partitions](http://docs.splunk.com/Documentation/SplunkCloud/latest/IngestProcessor/Architecture#Partitions) を参照してください。

Ingest Processor ソリューションは、`IngestProcessor` プロファイルに含まれるコマンドおよび関数のみをサポートします。Ingest Processor のパイプラインを記述するために使用できる具体的な SPL2 コマンドおよび関数については、[Ingest Processor pipeline syntax](http://docs.splunk.com/Documentation/SplunkCloud/latest/IngestProcessor/PipelinesOverview) を参照してください。`IngestProcessor` プロファイルが他の SPL2 プロファイルと比較して、さまざまなコマンドおよび関数をどのようにサポートするかの概要については、*SPL2 Search Reference* の次のページを参照してください。

* [Compatibility Quick Reference for SPL2 commands](http://docs.splunk.com/Documentation/SCS/current/SearchReference/CompatibilityQuickReferenceforSPL2commands)
* [Compatibility Quick Reference for SPL2 evaluation functions](http://docs.splunk.com/Documentation/SCS/current/SearchReference/CompatibilityQuickReferenceforSPL2evaluationfunctions)
