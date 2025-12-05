---
title: Log Observer
linkTitle: 7. Log Observer
weight: 8
archetype: chapter
time: 10 minutes
---

この時点まで、**コード変更は一切なく**、トレース (tracing)、プロファイリング (profiling)、データベースクエリパフォーマンス (Database Query Performance) のデータが Splunk Observability Cloud に送信されています。

次に、**Splunk Log Observer** を使用して Spring PetClinic アプリケーションからログデータ (log data) を取得します。

**Splunk OpenTelemetry Collector** は、Spring PetClinic アプリケーションからログを自動的に収集し、OTLP エクスポーター (exporter) を使用して Splunk Observability Cloud に送信します。その際、ログイベントには `trace_id`、`span_id`、トレースフラグ (trace flags) が付与されます。

**Splunk Log Observer** を使用してログを表示し、ログ情報をサービス (services) やトレース (traces) と自動的に関連付けます。

この機能は [**Related Content**](https://help.splunk.com/en/splunk-observability-cloud/data-tools/related-content) と呼ばれています。
