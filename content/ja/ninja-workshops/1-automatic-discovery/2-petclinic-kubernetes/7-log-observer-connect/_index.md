---
title: Log Observer
linkTitle: 7. Log Observer
weight: 8
archetype: chapter
time: 10 minutes
---

この時点まで、**コード変更は一切なく**、トレーシング、プロファイリング、データベースクエリパフォーマンスのデータがSplunk Observability Cloudに送信されています。

次に、**Splunk Log Observer** を使用してSpring PetClinicアプリケーションからログデータを取得します。

**Splunk OpenTelemetry Collector** は、Spring PetClinicアプリケーションからログを自動的に収集し、OTLPエクスポーターを使用してSplunk Observability Cloudに送信します。その際、ログイベントには `trace_id`、`span_id`、トレースフラグが付与されます。

**Splunk Log Observer** を使用してログを表示し、ログ情報をサービスやトレースと自動的に関連付けます。

この機能は [**Related Content**](https://help.splunk.com/en/splunk-observability-cloud/data-tools/related-content) と呼ばれています。
