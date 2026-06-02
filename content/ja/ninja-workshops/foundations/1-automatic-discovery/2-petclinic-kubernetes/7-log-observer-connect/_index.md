---
title: Log Observer
linkTitle: 7. Log Observer
weight: 8
archetype: chapter
time: 10 minutes
---

ここまでの工程では**コードの変更は一切行っていません**が、トレース、プロファイリング、Database Query Performance のデータが Splunk Observability Cloud に送信されています。

次は **Splunk Log Observer** を使って、Spring PetClinic アプリケーションからログデータを取得します。

**Splunk OpenTelemetry Collector** は Spring PetClinic アプリケーションからログを自動的に収集し、OTLP exporter を使って Splunk Observability Cloud に送信します。その際、ログイベントには `trace_id`、`span_id`、トレースフラグが付与されます。

そして **Splunk Log Observer** を使ってログを表示し、ログ情報をサービスやトレースと自動的に相関付けします。

この機能は [**Related Content**](https://help.splunk.com/en/splunk-observability-cloud/data-tools/related-content) と呼ばれます。
