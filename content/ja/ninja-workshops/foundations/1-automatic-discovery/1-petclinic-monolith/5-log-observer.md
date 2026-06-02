---
title: 4. Log Observer
weight: 4
---

Splunk Log Observer コンポーネントについては、Splunk OpenTelemetry Collector が Spring PetClinic アプリケーションのログを自動的に収集し、OTLP エクスポーターを使用して Splunk Observability Cloud に送信します。その際、ログイベントには `trace_id`、`span_id` およびトレースフラグが付与されます。

Log Observer は、アプリケーションやインフラストラクチャのログをリアルタイムで表示します。ログを検索、フィルタリング、分析することで、問題のトラブルシューティングや環境のモニタリングが可能です。

PetClinic Web アプリケーションに戻り、**Error** リンクを数回クリックしてください。これにより、PetClinic アプリケーションのログにいくつかのログメッセージが生成されます。

![PetClinic Error](../images/petclinic-error.png)

左側のメニューから **Log Observer** をクリックし、**Index** が **splunk4rookies-workshop** に設定されていることを確認します。

次に、**Add Filter** をクリックして `service.name` フィールドを検索し、`<INSTANCE>-petclinic-service` の値を選択して `=`（include）をクリックします。これで、PetClinic アプリケーションのログメッセージのみが表示されるようになります。

PetClinic アプリケーションで **Error** リンクをクリックして生成されたログエントリのいずれかを選択してください。ログメッセージと、ログメッセージに自動的に挿入されたトレースメタデータが表示されます。また、APM とインフラストラクチャの Related Content が利用可能であることがわかります。

![Log Observer](../images/log-observer.png)

これでワークショップは終了です。ここまで非常に多くの内容を扱ってきました。この時点で、メトリクス、トレース（APM および RUM）、ログ、データベースクエリのパフォーマンス、コードプロファイリングが Splunk Observability Cloud にレポートされているはずです。しかも、PetClinic アプリケーションのコードを変更することなく実現できています（ただし RUM は例外です）。

**おめでとうございます!**
