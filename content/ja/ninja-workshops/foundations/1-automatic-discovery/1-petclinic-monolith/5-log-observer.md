---
title: 4. Log Observer
weight: 4
---

Splunk Log Observer コンポーネントでは、Splunk OpenTelemetry Collector が Spring PetClinic アプリケーションからログを自動的に収集し、OTLP エクスポーターを使用して Splunk Observability Cloud に送信します。その際、ログイベントに `trace_id`、`span_id`、およびトレースフラグが付与されます。

Log Observer は、アプリケーションとインフラストラクチャからのログをリアルタイムで表示します。ログの検索、フィルタリング、分析を行い、問題のトラブルシューティングや環境の監視が可能です。

Web ブラウザで PetClinic Web アプリケーションに戻り、**Error** リンクを数回クリックしてください。これにより、PetClinic アプリケーションのログにいくつかのログメッセージが生成されます。

![PetClinic Error](../images/petclinic-error.png)

Splunk Observability Cloud の左側メニューから **Logs → Log Observer** をクリックし、**Index** が **splunk4rookies-workshop** に設定されていることを確認してください。

次に、**Add Filter** をクリックし、フィールド `service.name` を検索して、値 `<INSTANCE>-petclinic-service` を選択し、`=`（include）をクリックします。**Run search** をクリックしてください。これで、PetClinic アプリケーションからのログメッセージのみが表示されるはずです。

PetClinic アプリケーションの **Error** リンクをクリックして生成されたログエントリの1つを選択してください。ログメッセージと、ログメッセージに自動的に挿入されたトレースメタデータが表示されます。また、APM と Infrastructure の Related Content が利用可能であることも確認できます。

![Log Observer](../images/log-observer.png)

これでワークショップは終了です。多くの内容をカバーしました。この時点で、メトリクス、トレース（APM & RUM）、ログ、データベースクエリパフォーマンス、コードプロファイリングが Splunk Observability Cloud にレポートされており、PetClinic アプリケーションのコードを変更することなく実現できています（RUM を除く）。

**おめでとうございます！**
