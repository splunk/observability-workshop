---
title: OpenTelemetry Collector Processors
linkTitle: 4.1 Batch
weight: 1
---

## Batch Processor

デフォルトでは、**batch** プロセッサーのみが有効になっています。このプロセッサーは、データをエクスポートする前にバッチ処理するために使用されます。これにより、エクスポーターへのネットワーク呼び出し回数を削減できます。本ワークショップでは、Collector にハードコードされている以下のデフォルト値を継承します。

- `send_batch_size` (default = 8192): タイムアウトに関わらずバッチが送信される、スパン、メトリックデータポイント、またはログレコードの数です。send_batch_size はトリガーとして機能し、バッチのサイズには影響しません。パイプラインの次のコンポーネントに送信するバッチサイズの上限を強制したい場合は、send_batch_max_size を参照してください。
- `timeout` (default = 200ms): サイズに関わらずバッチが送信されるまでの時間です。ゼロに設定すると、send_batch_size は無視され、データは send_batch_max_size のみを条件として直ちに送信されます。
- `send_batch_max_size` (default = 0): バッチサイズの上限です。0 はバッチサイズに上限がないことを意味します。このプロパティは、より大きなバッチが小さな単位に分割されることを保証します。send_batch_size 以上の値である必要があります。

Batch プロセッサーの詳細については、[**Batch Processor documentation**](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md) を参照してください。
