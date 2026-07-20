---
title: エージェントとは
linkTitle: 2. エージェントとは
weight: 2
time: 5 minutes
---

## エージェントの用語

さまざまな種類のエージェントについて説明する前に、混乱を避けるために使用する用語を整理しておきましょう。

## OpenTelemetry

OpenTelemetryには、システムからデータを収集するためのさまざまなコンポーネントがあります。

### Collector

OpenTelemetryではCollectorを以下のように定義しています:
> The OpenTelemetry Collector offers a vendor-agnostic implementation of how to receive, process and export telemetry data. It removes the need to run, operate, and maintain multiple agents/collectors. This works with improved scalability and supports open source observability data formats (e.g. Jaeger, Prometheus, Fluent Bit, etc.) sending to one or more open source or commercial backends.

- 出典: [Open Telemetry Docs](https://opentelemetry.io/docs/collector/)

**Collectorはそれ自体がエージェントなのでしょうか？** ある意味ではそうです。データを収集するための **Receiver** を持ち、それを処理するための **Processor** を持ち、そして1つ以上の宛先（ルーティング用のゲートウェイやオブザーバビリティバックエンドなど）にデータを送信するための **Exporter** を持っています。

#### Receiver

**Receiver** は、その名前に反してプッシュまたはプルのどちらの方法でもデータを取得できます。例えば、ホストのCPU、メモリ、ディスク情報をスクレイピングして収集できます。また、他のシステムが情報をプッシュできるエンドポイントを公開することもできます。

#### Processor

**Processor** はデータを処理します。例えば、Processorは以下のことができます:
- [redact](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor)
- [filter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor)
- [sample (tail)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor)
- [sample (probabilistic)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/probabilisticsamplerprocessor)
- [transform](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor)

よく使われるコアProcessorとして、[memory limit processor](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/memorylimiterprocessor)（メモリ不足の状況を軽減するのに役立ちます）や[batch processor](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/batchprocessor)（テレメトリをバッチにまとめ、データを圧縮してより少ない接続数で送信します）があります。

#### Exporter

次に、データをどこかに送信する必要があります。それを行うのが **Exporter** です。Splunk Platformへのログ送信には通常[hec exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/splunkhecexporter)を使用します。その他のテレメトリは、宛先に応じて異なるExporterを使用します。

#### パイプライン

これらのReceiver、Processor、Exporterはすべて[パイプライン](https://opentelemetry.io/docs/collector/configuration/#basics)にまとめられます。

### 計装エージェント

Collectorはデータ収集の優れた基盤を提供しますが、アプリケーション側からデータを収集するにはどうすればよいでしょうか？ ここで計装エージェントの出番です。
