---
title: 3. Check Splunk
weight: 3
---

## インフラストラクチャメトリクスの確認

{{% notice title="Exercise" style="green" icon="running" %}}

1. [Metric Finder](https://app.signalfx.com/#/metrics) を開き、`workshop_heartbeat` を検索します。
2. `host.name` が `WORKSHOP_HOST_NAME` の値と一致するメトリクスが表示されるはずです。
3. その `host.name` で検索して、Collectorが送信している他のメトリクス（CPU、メモリ、ディスクなど）を確認します。

{{% /notice %}}

## APM が空であることを確認

{{% notice title="Exercise" style="green" icon="running" %}}

1. Splunk Observability Cloudで **APM** に移動します。
2. 定義した環境（`WORKSHOP_ENVIRONMENT`）でフィルタリングします。
3. **空** であるはずです（または存在しない）。サービス、トレース、サービスマップはありません。

{{% /notice %}}

Collectorはデフォルトでインフラストラクチャメトリクスを送信しますが、トレースを生成しているものがないため、エクスポートするトレースがありません。

{{% notice title="Note" style="info" %}}
これは「導入前」の状態です。実際のリクエストを処理する3つのサービスが稼働していますが、Splunk APMはそれらのリクエストをまったく可視化できていません。次のセクションでは、**アプリケーションコードに一切触れることなく**、これを修正します。
{{% /notice %}}
