---
title: APM Span
linkTitle: 3. APM Spans
weight: 3
---

スパンを確認しながら、トレーシングに加えて **automatic discovery and configuration** を使用することで、**コードを変更せずに**利用できるいくつかのすぐに使える機能を見てみましょう

まず、Waterfall Pane で、以下のスクリーンショットに示すように `customers-service:SELECT petclinic` または類似のスパンが選択されていることを確認してください

![DB-query](../../images/db-query.png)

* 基本的なレイテンシー情報は、計装された関数または呼び出しのバーとして表示されます。上記の例では、17.8 ミリ秒かかっています。
* 複数の類似スパン **(1)** は、スパンが複数回繰り返される場合にのみ表示されます。この例では、10 回の繰り返しがあります。`10x` をクリックすることですべてのスパンを表示/非表示にでき、すべてのスパンが順番に表示されます。
* **Inferred Services**: 計装されていない外部システムへの呼び出しは、グレーの「推論された」スパンとして表示されます。この例での Inferred Service（推論されたスパン）は、上記に示すように MySQL Database `mysql:petclinic SELECT petclinic` **(2)** への呼び出しです。
* **Span Tags**: Tag Pane には、automatic discovery and configuration によって生成された標準タグが表示されます。この場合、スパンはデータベースを呼び出しているため、`db.statement` タグ **(3)** が含まれています。このタグは DB クエリステートメントを保持し、このスパン中に実行されたデータベース呼び出しで使用されます。これは DB-Query Performance 機能で使用されます。次のセクションで DB-Query Performance を確認します。
* **Always-on Profiling**: システムがスパンのライフサイクル中に Profiling データをキャプチャするように設定されている**場合**、スパンのタイムラインにキャプチャされた Call Stack の数が表示されます。上記の例では、`customer-service:GET /owners` スパンに 18 個の Call Stack が表示されています。**(4)**

次のセクションで Profiling を確認します。

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
