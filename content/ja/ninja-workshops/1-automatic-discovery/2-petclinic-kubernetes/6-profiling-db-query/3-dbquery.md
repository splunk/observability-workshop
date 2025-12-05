---
title: Database Query Performance
linkTitle: 3. Database Query Performance
weight: 3
---

Database Query Performanceを使用すると、Splunk APMで直接、データベース (database) クエリ (query) がサービス (service) の可用性に与える影響をモニター (monitor) できます。これにより、データベース (database) をインストルメント (instrument) することなく、長時間実行されるクエリ (query)、最適化されていないクエリ (query)、または重いクエリ (query) を迅速に特定し、それらが引き起こしている可能性のある問題を軽減できます。

データベース (database) クエリ (query) のパフォーマンス (performance) を確認するには、ブラウザ (browser) で戻るか、メニュー (menu) バー (bar) のAPMセクション (section) に移動してAPMの**Service Map**ページ (page) に移動し、**Service Map**タイル (tile) をクリックします。

Dependency mapで推論されたデータベース (database) サービス (service) `mysql:petclinic` Inferred Database serverを選択し **(1)**、次に右側のペイン (pane) をスクロール (scroll) して**Database Query Performance** Pane **(2)**を見つけます。

![DB-query from map](../../images/db-query-map.png)

マップ (map) で選択したサービス (service) が実際に（推論された）データベース (database) サーバー (server) である場合、このペイン (pane) には期間に基づく上位90%（P90）のデータベース (database) コール (call) が表示されます。db-queryパフォーマンス (performance) 機能をさらに詳しく調べるには、ペイン (pane) の上部にある**Database Query Performance**という単語のどこかをクリックします。

これにより、DB-query Performanceの概要画面が表示されます：

![DB-query full](../../images/db-query-full.png)

{{% notice title="Database Query Normalization" style="info" %}}
デフォルト (default) では、Splunk APMインストルメンテーション (instrumentation) はデータベース (database) クエリ (query) をサニタイズ (sanitize) して、`db.statements`からシークレット (secret) や個人を特定できる情報（PII）などの機密データ (data) を削除またはマスク (mask) します。データベース (database) クエリ (query) の正規化 (normalization) をオフにする方法は[こちら](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/monitor-database-query-performance/troubleshoot-database-query-performance#turn-off-database-query-normalization)で確認できます。
{{% /notice %}}

この画面には、Splunk Observability Cloudに送信されたTraces & Spansに基づいて、アプリケーション (application) からデータベース (database) に対して実行されたすべてのDatabase queries **(1)**が表示されます。時間ブロック (block) 間で比較したり、Total Time、P90 Latency & Requests **(2)**でソート (sort) したりできることに注意してください。

リスト (list) 内の各Database queryについて、時間ウィンドウ (window) 中の最高レイテンシ (latency)、コール (call) の総数、および1秒あたりのリクエスト (request) 数 **(3)**が表示されます。これにより、クエリ (query) を最適化できる場所を特定できます。

右側のペイン (pane) **(5)**の2つのチャート (chart) を使用して、Database Callsを含むトレース (trace) を選択できます。Tag Spotlightペイン (pane) **(6)**を使用して、エンドポイント (endpoint) やタグ (tag) に基づいて、データベース (database) コール (call) に関連するタグ (tag) を確認します。

クエリ (query) の詳細ビュー (view) を表示する必要がある場合：

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
