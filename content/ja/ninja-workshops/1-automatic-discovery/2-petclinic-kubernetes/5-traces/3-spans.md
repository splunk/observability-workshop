---
title: APM Span
linkTitle: 3. APM Spans
weight: 3
---

スパン (span) を調べる際、トレーシング (tracing) の上で**自動検出と設定 (automatic discovery and configuration)** を使用すると、**コード変更なし**で得られるいくつかの標準機能を見てみましょう：

まず、Waterfall Paneで、以下のスクリーンショットに示すように`customers-service:SELECT petclinic`または類似のスパンが選択されていることを確認してください：

![DB-query](../../images/db-query.png)

* 基本的なレイテンシ (latency) 情報は、インストルメント (instrument) された関数または呼び出しのバーとして表示されます。上記の例では、17.8ミリ秒かかりました。
* いくつかの類似したスパン**(1)**は、スパンが複数回繰り返される場合にのみ表示されます。この場合、例では10回の繰り返しがあります。`10x`をクリックすると、すべてのスパンが順番に表示されるように表示/非表示を切り替えることができます。
* **Inferred Services**：インストルメントされていない外部システムへの呼び出しは、グレーの「推測された (inferred)」スパンとして表示されます。この例のInferred Serviceまたはスパンは、上記に示すようにMysqlデータベース (Database) `mysql:petclinic SELECT petclinic` **(2)**への呼び出しです。
* **Span Tags**：Tag Paneには、自動検出と設定によって生成された標準タグが表示されます。この場合、スパンはデータベースを呼び出しているため、`db.statement`タグ**(3)**が含まれています。このタグは、このスパン中に実行されたデータベース呼び出しで使用されるDBクエリ (query) ステートメント (statement) を保持します。これはDB-Query Performance機能で使用されます。DB-Query Performanceについては次のセクションで見ていきます。
* **Always-on Profiling**：システムがスパンのライフサイクル (life cycle) 中にプロファイリング (Profiling) データをキャプチャ (capture) するように設定されている**場合**、スパンのタイムライン (timeline) でキャプチャされたコールスタック (Call Stack) の数が表示されます。上記の例では、`customer-service:GET /owners`スパンに対して18個のコールスタックがあることがわかります。**(4)**

次のセクションでプロファイリングを見ていきます。

<!--
## 3. Review Profiling Data Collection

You can now visit the Splunk APM UI and examine the application components, traces, profiling, DB Query performance and metrics. From the left-hand menu **APM** → **Explore**, click the environment dropdown and select your environment e.g. `<INSTANCE>-petclinic` (where`<INSTANCE>` is replaced with the value you noted down earlier).

![APM Environment](../images/apm-environment.png)

Once your validation is complete you can stop the application by pressing `Ctrl-c`.

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
