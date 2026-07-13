---
title: エージェントとは
linkTitle: 2. エージェントとは
weight: 2
time: 5 minutes
---

## エージェントの用語

さまざまなタイプのエージェントについて説明する前に、混乱を避けるために使用する用語を確認しておきましょう。

## OpenTelemetry

OpenTelemetryには、システムからデータを収集するために使用されるさまざまなコンポーネントがあります。

### Collector

OpenTelemetryではCollectorを次のように定義しています:
> The OpenTelemetry Collector offers a vendor-agnostic implementation of how to receive, process and export telemetry data. It removes the need to run, operate, and maintain multiple agents/collectors. This works with improved scalability and supports open source observability data formats (e.g. Jaeger, Prometheus, Fluent Bit, etc.) sending to one or more open source or commercial backends.

- 出典: [Open Telemetry Docs](https://opentelemetry.io/docs/collector/)

**Collectorはそれ自体がエージェントなのでしょうか？** ある意味ではそうです。データを収集するための **Receiver** を持ち、それを処理するための **Processor** を持ち、そしてデータを1つ以上の宛先（ルーティング用のゲートウェイやオブザーバビリティバックエンドなど）に送信するための **Exporter** を持っています。

#### Receivers

**Receiver** は、その名前に反して、データのプッシュとプルの両方で動作できます。例えば、ホストのCPU、メモリ、ディスク情報をスクレイピングして収集できます。また、他のシステムが情報をプッシュできるエンドポイントを提供することもできます。

#### Processors

**Processor** はデータを処理します。例えば、Processorは以下のことができます:
- [redact](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor)
- [filter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor)
- [sample (tail)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor)
- [sample (probabilistic)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/probabilisticsamplerprocessor)
- [transform](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/metricstransformprocessor)

よく使用されるコアProcessorとして、[memory limit processor](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/memorylimiterprocessor)（メモリ不足の状況を緩和するのに役立ちます）や[batch processor](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/batchprocessor)（テレメトリデータを圧縮し、より少ない接続でバッチ送信します）があります。

#### Exporters

データをどこかに送信する必要があり、それを行うのが **Exporter** です。Splunk Platformへのログは通常、[hec exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/splunkhecexporter)を使用します。その他のテレメトリは、宛先に応じて異なるExporterを使用します。

#### パイプライン

これらのReceiver、Processor、Exporterはすべて[パイプライン](https://opentelemetry.io/docs/collector/configuration/#basics)で統合されます。

### 計装エージェント

Collectorはデータ収集のための優れた基盤を提供しますが、アプリケーション側からデータを収集するにはどうすればよいでしょうか？ そこで計装エージェントが登場します。
