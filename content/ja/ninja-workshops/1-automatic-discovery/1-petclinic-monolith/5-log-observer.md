---
title: 4. Log Observer
weight: 4
---

Splunk Log Observer コンポーネントでは、Splunk OpenTelemetry Collector が Spring PetClinic アプリケーションからログを自動的に収集し、OTLP エクスポーターを使用して Splunk Observability Cloud に送信します。その際、ログイベントに `trace_id`、`span_id`、トレースフラグを付与します。

Log Observer は、アプリケーションとインフラストラクチャからのログをリアルタイムで表示します。ログの検索、フィルタリング、分析を行って、問題のトラブルシューティングや環境の監視が可能です。

PetClinic Web アプリケーションに戻り、**Error** リンクを数回クリックしてください。これにより、PetClinic アプリケーションログにいくつかのログメッセージが生成されます。

![PetClinic Error](../images/petclinic-error.png)

左側のメニューから **Log Observer** をクリックし、**Index** が **splunk4rookies-workshop** に設定されていることを確認してください。

次に、**Add Filter** をクリックし、フィールド `service.name` を検索して、値 `<INSTANCE>-petclinic-service` を選択し、`=`（include）をクリックします。これで、PetClinic アプリケーションからのログメッセージのみが表示されるはずです。

PetClinic アプリケーションの **Error** リンクをクリックして生成されたログエントリの1つを選択してください。ログメッセージと、ログメッセージに自動的にインジェクションされたトレースメタデータが表示されます。また、APM と Infrastructure の Related Content が利用可能であることにも注目してください。

![Log Observer](../images/log-observer.png)

これでワークショップは終了です。多くの内容をカバーしました。この時点で、メトリクス、トレース（APM と RUM）、ログ、データベースクエリパフォーマンス、コードプロファイリングが Splunk Observability Cloud に報告されているはずです。しかも、PetClinic アプリケーションのコードを変更することなく実現できました（RUM を除く）。

**おめでとうございます！**
