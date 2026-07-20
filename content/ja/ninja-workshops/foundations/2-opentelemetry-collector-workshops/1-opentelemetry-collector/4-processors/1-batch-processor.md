---
title: OpenTelemetry Collector Processors
linkTitle: 4.1 Batch
weight: 1
---

## Batch Processor

デフォルトでは、**batch** Processorのみが有効になっています。このProcessorは、データをエクスポートする前にバッチ処理するために使用されます。これにより、Exporterへのネットワーク呼び出し回数を削減できます。このワークショップでは、Collectorにハードコードされている以下のデフォルト値を使用します。

- `send_batch_size`（デフォルト = 8192）: タイムアウトに関係なくバッチが送信されるSpan、メトリクスデータポイント、またはログレコードの数。send_batch_sizeはトリガーとして機能し、バッチのサイズには影響しません。パイプラインの次のコンポーネントに送信されるバッチサイズの制限を適用する必要がある場合は、send_batch_max_sizeを参照してください。
- `timeout`（デフォルト = 200ms）: サイズに関係なくバッチが送信されるまでの時間。ゼロに設定すると、send_batch_sizeは無視され、send_batch_max_sizeのみに従ってデータが即座に送信されます。
- `send_batch_max_size`（デフォルト = 0）: バッチサイズの上限。0はバッチサイズに上限がないことを意味します。このプロパティにより、大きなバッチがより小さな単位に分割されます。send_batch_size以上の値である必要があります。

Batch Processorの詳細については、[**Batch Processorドキュメント**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md)を参照してください。
