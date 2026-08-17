---
title: 3. Splunk の確認
weight: 3
---

## インフラストラクチャメトリクスの確認

{{% notice title="演習" style="green" icon="running" %}}

1. [Metric Finder](https://app.us1.signalfx.com/#/metrics) を開き（または[チャートを作成](https://app.us1.signalfx.com/#/chart/new?template=default&filters=sf_metric%3Aworkshop_heartbeat)して）、`workshop_heartbeat` を検索します
2. `host.name` が `WORKSHOP_HOST_NAME` の値と一致するメトリクスが表示されるはずです
3. その `host.name` で検索して、Collector が送信している他のメトリクス（CPU、メモリ、ディスクなど）を確認します

{{% /notice %}}

## APM が空であることを確認

{{% notice title="演習" style="green" icon="running" %}}

1. Splunk Observability Cloud で **APM** に移動します
2. 定義した環境（`WORKSHOP_ENVIRONMENT`）でフィルタリングします
3. **空**であるはずです（または存在しないはずです）。サービス、トレース、サービスマップはありません

{{% /notice %}}

Collector はインフラストラクチャメトリクスを送信しています。これはデフォルトの動作ですが、何もトレースを生成していないため、エクスポートするトレースがありません。

{{% notice title="注記" style="info" %}}
これが「導入前」の状態です。3つのサービスが実際のリクエストを処理していますが、Splunk APM からはそれらのリクエストがまったく見えていません。次のセクションでは、**アプリケーションコードに触れることなく**、これを解決します。
{{% /notice %}}
