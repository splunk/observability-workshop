---
title: Database Query Performance
linkTitle: 3. Database Query Performance
weight: 3
---

Database Query Performance を使用すると、データベースクエリがサービスの可用性に与える影響を Splunk APM で直接モニタリングできます。これにより、データベースをインストルメントすることなく、長時間実行されているクエリ、最適化されていないクエリ、重いクエリを迅速に特定し、それらが引き起こしている可能性のある問題を軽減できます。

データベースクエリのパフォーマンスを確認するには、ブラウザで戻るか、メニューバーの APM セクションに移動して **Service Map** タイルをクリックし、APM の **Service Map** ページにいることを確認してください。

Dependency map で推論されたデータベースサービス `mysql:petclinic` Inferred Database server を選択し **(1)**、右側のペインをスクロールして **Database Query Performance** ペインを見つけます **(2)**。

![DB-query from map](../../images/db-query-map.png)

マップで選択したサービスが実際に（推論された）データベースサーバーである場合、このペインは継続時間に基づく上位 90%（P90）のデータベース呼び出しで埋められます。db-query performance 機能をさらに深く掘り下げるには、ペイン上部の **Database Query Performance** という単語のあたりをクリックします。

これにより、DB-query Performance 概要画面が表示されます。

![DB-query full](../../images/db-query-full.png)

{{% notice title="Database Query Normalization" style="info" %}}
デフォルトでは、Splunk APM のインストルメンテーションは、シークレットや個人を特定できる情報（PII）などの機密データを `db.statements` から削除またはマスクするためにデータベースクエリをサニタイズします。データベースクエリの正規化を無効にする方法は[こちら](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/monitor-database-query-performance/troubleshoot-database-query-performance#turn-off-database-query-normalization)で確認できます。
{{% /notice %}}

この画面では、Splunk Observability Cloud に送信された Traces と Spans に基づいて、アプリケーションからデータベースに対して行われたすべてのデータベースクエリ **(1)** が表示されます。時間ブロック間で比較したり、Total Time、P90 Latency、Requests でソートしたりできることに注意してください **(2)**。

リスト内の各データベースクエリについて、最も高いレイテンシー、時間枠内の総呼び出し回数、1 秒あたりのリクエスト数が表示されます **(3)**。これにより、クエリを最適化できる箇所を特定できます。

右側のペインの 2 つのチャート **(5)** を介して、データベース呼び出しを含むトレースを選択できます。Tag Spotlight ペイン **(6)** を使用して、エンドポイントやタグに基づいて、データベース呼び出しに関連するタグを掘り下げて確認します。

クエリの詳細ビューを確認する必要がある場合は、次のとおりです。

![details](../../images/query-details.png)

特定のクエリをクリックします **(1)**。これにより、Query Details ペイン **(2)** が開き、より詳細な調査に使用できます。

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
