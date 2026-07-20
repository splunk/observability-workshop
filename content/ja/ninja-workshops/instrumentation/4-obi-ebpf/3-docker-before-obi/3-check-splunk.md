---
title: 3. Splunkの確認
weight: 3
---

## インフラストラクチャメトリクスの確認

{{% notice title="Exercise" style="green" icon="running" %}}

1. [Metric Finder](https://app.us1.signalfx.com/#/metrics)（または[チャートの作成](https://app.us1.signalfx.com/#/chart/new?template=default&filters=sf_metric%3Aworkshop_heartbeat)）を開き、`workshop_heartbeat` を検索します
2. `host.name` が `WORKSHOP_HOST_NAME` の値と一致するメトリクスが表示されます
3. その `host.name` で検索して、Collectorが送信している他のメトリクス（CPU、メモリ、ディスクなど）を確認します

{{% /notice %}}

## APMが空であることの確認

{{% notice title="Exercise" style="green" icon="running" %}}

1. Splunk Observability Cloudで **APM** に移動します
2. 定義した環境（`WORKSHOP_ENVIRONMENT`）でフィルタリングします
3. **空** であるはずです（または存在しない）。サービス、トレース、サービスマップはありません

{{% /notice %}}

Collectorはデフォルトの動作としてインフラストラクチャメトリクスを送信していますが、トレースを生成しているものがないため、エクスポートするトレースがありません。

{{% notice title="注意" style="info" %}}
これが「導入前」の状態です。3つのサービスが実際のリクエストを処理していますが、Splunk APMにはそれらのリクエストに対する可視性がまったくありません。次のセクションでは、**アプリケーションコードに一切触れることなく** これを修正します。
{{% /notice %}}
