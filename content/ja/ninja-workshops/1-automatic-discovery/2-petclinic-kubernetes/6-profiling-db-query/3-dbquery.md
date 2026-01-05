---
title: Database Query Performance
linkTitle: 3. Database Query Performance
weight: 3
---

Database Query Performanceを使用すると、Splunk APMで直接、データベースクエリがサービスの可用性に与える影響をモニターできます。これにより、データベースをインストルメントすることなく、長時間実行されるクエリ、最適化されていないクエリ、または重いクエリを迅速に特定し、それらが引き起こしている可能性のある問題を軽減できます。

データベースクエリのパフォーマンスを確認するには、ブラウザで戻るか、メニューバーのAPMセクションに移動してAPMの**Service Map**ページに移動し、**Service Map**タイルをクリックします。

Dependency mapで推論されたデータベースサービス `mysql:petclinic` Inferred Database serverを選択し **(1)**、次に右側のペインをスクロールして**Database Query Performance** Pane **(2)**を見つけます。

![DB-query from map](../../images/db-query-map.png)

マップで選択したサービスが実際に（推論された）データベースサーバーである場合、このペインには期間に基づく上位90%（P90）のデータベースコールが表示されます。db-queryパフォーマンス機能をさらに詳しく調べるには、ペインの上部にある**Database Query Performance**という単語のどこかをクリックします。

これにより、DB-query Performanceの概要画面が表示されます：

![DB-query full](../../images/db-query-full.png)

{{% notice title="Database Query Normalization" style="info" %}}
デフォルトでは、Splunk APMインストルメンテーションはデータベースクエリをサニタイズして、`db.statements`からシークレットや個人を特定できる情報（PII）などの機密データを削除またはマスクします。データベースクエリの正規化をオフにする方法は[こちら](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/monitor-database-query-performance/troubleshoot-database-query-performance#turn-off-database-query-normalization)で確認できます。
{{% /notice %}}

この画面には、Splunk Observability Cloudに送信されたTraces & Spansに基づいて、アプリケーションからデータベースに対して実行されたすべてのDatabase queries **(1)**が表示されます。時間ブロック間で比較したり、Total Time、P90 Latency & Requests **(2)**でソートしたりできることに注意してください。

リスト内の各Database queryについて、時間ウィンドウ中の最高レイテンシ、コールの総数、および1秒あたりのリクエスト数 **(3)**が表示されます。これにより、クエリを最適化できる場所を特定できます。

右側のペイン **(5)**の2つのチャートを使用して、Database Callsを含むトレースを選択できます。Tag Spotlightペイン **(6)**を使用して、エンドポイントやタグに基づいて、データベースコールに関連するタグを確認します。

クエリの詳細ビューを表示する必要がある場合：

![details](../../images/query-details.png)

特定のQuery **(1)**をクリックします。これにより、Query Details pane **(2)**が開き、より詳細な調査に使用できます。

<!--

## 4. Adding Resource Attributes to Spans

Resource attributes can be added to every reported span. For example `version=0.314`. A comma-separated list of resource attributes can also be defined e.g. `key1=val1,key2=val2`.

Let's launch the PetClinic again using new resource attributes. Note, that adding resource attributes to the run command will override what was defined when we installed the collector. Let's add two new resource attributes `deployment.environment=$INSTANCE-petclinic-env,version=0.314`:

```bash
java \
-Dserver.port=8083 \
-Dotel.service.name=$INSTANCE-petclinic-service \
-Dotel.resource.attributes=deployment.environment=$INSTANCE-petclinic-env,version=0.314 \
-jar target/spring-petclinic-*.jar --spring.profiles.active=mysql
```

Back in the Splunk APM UI we can drill down on a recent trace and see the new `version` attribute in a span.
-->
