---
title: OpenTelemetry Collector Processors
linkTitle: 4.1 Batch
weight: 1
---

## Batch Processor

デフォルトでは、**batch** processor のみが有効になっています。この processor は、データをエクスポートする前にバッチ処理するために使用されます。これは、exporter へのネットワーク呼び出しの回数を減らすのに役立ちます。このワークショップでは、Collector にハードコードされている以下のデフォルト値を継承します：

- `send_batch_size`（デフォルト = 8192）：タイムアウトに関係なくバッチが送信されるスパン、メトリクスデータポイント、またはログレコードの数。send_batch_size はトリガーとして機能し、バッチのサイズには影響しません。パイプラインの次のコンポーネントに送信されるバッチサイズの制限を強制する必要がある場合は、send_batch_max_size を参照してください。
- `timeout`（デフォルト = 200ms）：サイズに関係なくバッチが送信されるまでの時間。ゼロに設定すると、send_batch_max_size のみに従ってデータが即座に送信されるため、send_batch_size は無視されます。
- `send_batch_max_size`（デフォルト = 0）：バッチサイズの上限。0 はバッチサイズに上限がないことを意味します。このプロパティは、大きなバッチを小さな単位に分割することを保証します。send_batch_size 以上である必要があります。

Batch processor の詳細については、[**Batch Processor のドキュメント**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md)を参照してください。
