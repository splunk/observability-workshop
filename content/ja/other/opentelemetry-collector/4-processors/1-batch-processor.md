---
title: OpenTelemetry Collector プロセッサー
linkTitle: 4.1 Batch
weight: 1
---

## Batch プロセッサー

デフォルトでは、**batch** プロセッサーだけが有効になっています。このプロセッサーは、データをエクスポートする前にバッチ処理して、エクスポーターへのネットワーク・コールの回数を減らすために使われます。このワークショップではデフォルトの設定を使用します：

- `send_batch_size` (デフォルト = 8192): タイムアウトに関係なく、バッチを送信するスパン、メトリクスデータポイント、またはログレコードの数。パイプラインの次のコンポーネントに送信されるバッチサイズを制限する場合には、 `send_batch_max_size` を使います。
- `timeout` (デフォルト = 200ms): サイズに関係なく、バッチが送信されるまでの時間。ゼロに設定すると、`send_batch_size` の設定を無視して `send_batch_max_size` だけが適用され、データは直ちに送信されます。
- `send_batch_max_size` (デフォルト = 0): バッチサイズの上限。`0` を設定すると、バッチサイズの上限がないことして扱われます。この設定は、大きなバッチが小さなユニットに分割されることを保証します。`send_batch_size` 以上でなければななりません。
