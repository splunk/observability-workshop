---
title: 4. Log Observer
weight: 4
---

Splunk Log Observerコンポーネントでは、Splunk OpenTelemetry CollectorがSpring PetClinicアプリケーションからログを自動的に収集し、OTLPエクスポーターを使用してSplunk Observability Cloudに送信します。その際、ログイベントに `trace_id`、`span_id`、トレースフラグを付与します。

Log Observerは、アプリケーションとインフラストラクチャからのログをリアルタイムで表示します。ログの検索、フィルタリング、分析を行って、問題のトラブルシューティングや環境の監視が可能です。

PetClinic Webアプリケーションに戻り、**Error** リンクを数回クリックしてください。これにより、PetClinicアプリケーションログにいくつかのログメッセージが生成されます。

![PetClinic Error](../images/petclinic-error.png)

左側のメニューから **Log Observer** をクリックし、**Index** が **splunk4rookies-workshop** に設定されていることを確認してください。

次に、**Add Filter** をクリックし、フィールド `service.name` を検索して、値 `<INSTANCE>-petclinic-service` を選択し、`=`（include）をクリックします。これで、PetClinicアプリケーションからのログメッセージのみが表示されるはずです。

PetClinicアプリケーションの **Error** リンクをクリックして生成されたログエントリの1つを選択してください。ログメッセージと、ログメッセージに自動的にインジェクションされたトレースメタデータが表示されます。また、APMとInfrastructureのRelated Contentが利用可能であることにも注目してください。

![Log Observer](../images/log-observer.png)

これでワークショップは終了です。多くの内容をカバーしました。この時点で、メトリクス、トレース（APMとRUM）、ログ、データベースクエリパフォーマンス、コードプロファイリングがSplunk Observability Cloudに報告されているはずです。しかも、PetClinicアプリケーションのコードを変更することなく実現できました（RUMを除く）。

**おめでとうございます！**
