---
title: 高カーディナリティディメンションの集約と削除
linkTitle: 4.2 高カーディナリティディメンションの集約と削除
weight: 3
---

パイプラインにディメンションを追加したので、メトリクスをチャートに表示して、これらのディメンションをグループ化やフィルタリングにどのように使用できるかを確認します。次に、Metrics Pipeline Management を使用してメトリクスを集約し、ノイズの多い `auditID` ディメンションを削除することで、Ingest Processor Pipeline を変更することなくカーディナリティを削減します。

{{% notice title="演習: 新しいディメンションの確認" style="green" icon="running" %}}

**1.** 前のセクションで作成したチャートを閉じた場合は、右上隅の **+** アイコン → **Chart** をクリックして新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** で、**Ingest Processor Pipeline** で作成したメトリクス名（`k8s_audit_UNIQUE_FIELD`）をメトリクス名フィールドに入力します。

**3.** メトリクスが1つから多数に変化していることに注目してください。これは、ディメンションを含むようにパイプラインを更新した際に発生しました。`auditID` ディメンションは Kubernetes の各監査イベントで一意であるため、すべてのメトリクスデータポイントが独自の MTS を作成するようになりました。これはカーディナリティの爆発であり、メトリクスは技術的にはより詳細になっていますが、それらの単一用途の時系列はすべて、チャートやアラートに実際に使用できる価値を提供することなく利用量を膨張させます。

![Metric Timeseries](../../images/metric_timeseries.png?width=40vw)

{{% notice title="注意" style="info" icon="info" %}}
これは実環境でよくある状況です。チームが便利な識別子をディメンションとして追加すると、MTS 数が予想よりもはるかに速く増加します。次の演習では、Metrics Pipeline Management を使用してカーディナリティを制御下に戻します。これはすべて Splunk Observability Cloud の UI から行い、Ingest Processor Pipeline やデータを送信しているシステムに触れることなく実行できます。
{{% /notice %}}

{{% /notice %}}

{{% notice title="演習: auditID ディメンションの集約と削除" style="green" icon="running" %}}

ここでは **Metrics Pipeline Management** を使用して、メトリクスを一意の `auditID` ディメンションを含まない新しい低カーディナリティメトリクスにロールアップする集約ルールを作成します。その後、不要になった高カーディナリティの生メトリクスを削除します。

**1.** Splunk Observability Cloud で、**Metrics** → **Pipeline Automation** に移動します。

![Navigate to Pipeline Automation](../../images/pipeline_automation_nav.png?width=40vw)

**2.** ページ上部の行で **Pipeline Management** を選択します。

**3.** **Pipeline Management** ページで、**Choose a metric** ボタンをクリックします。

![Select Pipeline Management](../../images/pipeline_management_tab.png?width=40vw)

**4.** **Choose a metric** ポップアップで、Ingest Processor Pipeline で作成したメトリクス名（例: `k8s_audit_2`）を入力し、**Choose** をクリックします。

![Enter Metric Name](../../images/choose_metric_search.png?width=40vw)

**5.** **Ingestion** セクションで、**Raw MTS** の横にある **Edit** をクリックします。

![Edit Raw MTS](../../images/edit_ingest_pipeline.png?width=40vw)

{{% notice title="情報" style="info" icon="info" %}}
このページに表示されているメトリクスパイプラインを確認してください。現在、**Raw MTS** と **Real-time MTS** のカウントは同じです。これは、集約ルールやルーティングルールをまだ作成していないため、送信したすべての Raw MTS がリアルタイムで保存され利用可能になっているためです。次のステップでルールを追加すると、これらの値が適用している最適化を反映してどのように変化するかを確認できます。
{{% /notice %}}

**6.** **Update raw data routing** モーダルで、**Dropped** を選択します。これにより、受信したメトリクスデータは Splunk Observability Cloud に保存される前に破棄されます。特定の MTS を復元する必要がある場合は、ルーティング例外ルールを使用してリアルタイムに再ルーティングできます。**Update** をクリックし、次に **Enable** をクリックして更新を有効にします。

![Drop Raw Data Routing](../../images/drop_raw_data_routing.png?width=40vw)

**7.** **Added by rule** セクションで、**+ Add** をクリックして新しい集約ルールを作成します。

![Add Aggregation Rule](../../images/add_aggregation_rule.png?width=40vw)

**8.** **Create aggregation rule** モーダルで、名前に `Drop unique auditID` と入力します。

**9.** **Select dimensions** セクションで、ドロップダウンの値を **Keep** から **Drop** に変更し、検索バーを使用して **auditID** を選択します。

{{% notice title="注意" style="info" icon="info" %}}
集約されたメトリクスに新しいメトリクス名が作成されることに注目してください。この新しいメトリクスは有用なディメンションをすべて保持しますが、一意の `auditID` は含まれなくなります。次のセクションでビジュアライゼーションを作成する際に、この集約されたメトリクスを使用します。
{{% /notice %}}

**10.** **Data volume** セクションを確認します。ここには集約されていない **Raw MTS** と **Aggregated MTS** が表示されます。`auditID` ディメンションを削除することで得られる MTS の正確な削減量を確認できます。これが取り戻している利用量であり、インジェストエンドポイントでは何も変更していません。

**11.** **Create** をクリックします。

![Create Aggregation Rule](../../images/create_aggregation_rule.png?width=40vw)

{{% notice title="注意" style="info" %}}
これで、メトリクスを新しい低カーディナリティメトリクスに集約し、一意の `auditID` ディメンションを含む生メトリクスを削除しました。これらすべてを Splunk Observability Cloud の UI から行い、Ingest Processor Pipeline やデータを送信しているシステムを変更することなく実行しました。

次のステップでは、集約されたメトリクスを使用してビジュアライゼーションを作成します。
{{% /notice %}}

{{% /notice %}}
