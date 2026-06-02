---
title: 3. Splunk で確認する
weight: 3
---

## インフラストラクチャメトリクスを確認する

{{% notice title="演習" style="green" icon="running" %}}

1. [Metric Finder](https://app.us1.signalfx.com/#/metrics) を開く（または [チャートを作成](https://app.us1.signalfx.com/#/chart/new?template=default&filters=sf_metric%3Aworkshop_heartbeat)）して `workshop_heartbeat` を検索します。
2. `host.name` が `WORKSHOP_HOST_NAME` の値と一致するメトリクスが表示されるはずです。
3. その `host.name` で検索して、collector が送信している他のメトリクス（CPU、メモリ、ディスクなど）を確認します。

{{% /notice %}}

## APM が空であることを確認する

{{% notice title="演習" style="green" icon="running" %}}

1. Splunk Observability Cloud で **APM** に移動します。
2. 定義した environment（`WORKSHOP_ENVIRONMENT`）でフィルタします。
3. **空** になっている（または存在しない）はずです。サービスもトレースもサービスマップもありません。

{{% /notice %}}

collector はデフォルトの動作としてインフラストラクチャメトリクスを送信していますが、トレースを生成するものがないため、エクスポートするトレースはありません。

{{% notice title="Note" style="info" %}}
これが「before」の状態です。実際のリクエストを処理する 3 つのサービスが稼働していますが、Splunk APM はそれらのリクエストをまったく可視化できていません。次のセクションでは、**アプリケーションコードに手を加えることなく** これを解決します。
{{% /notice %}}
