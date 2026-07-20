---
title: 高カーディナリティディメンションの集約と削除
linkTitle: 4.2 高カーディナリティディメンションの集約と削除
weight: 3
---

パイプラインにディメンションを追加したので、メトリクスをチャートに表示して、これらのディメンションをグループ化やフィルタリングにどのように使用できるかを確認します。次に、Metrics Pipeline Managementを使用してメトリクスを集約し、ノイズの多い `auditID` ディメンションを削除することで、Ingest Processor Pipelineに変更を加えることなくカーディナリティを削減します。

{{% notice title="演習: 新しいディメンションの確認" style="green" icon="running" %}}

**1.** 前のセクションで作成したチャートを閉じた場合は、右上の **+** アイコン → **Chart** をクリックして新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** で、**Ingest Processor Pipeline** で作成したメトリクス名（`k8s_audit_UNIQUE_FIELD`）をメトリクス名フィールドに入力します。

**3.** パイプラインを更新してディメンションを含めたことにより、メトリクスが1つから多数に変化したことに注目してください。`auditID` ディメンションはすべてのKubernetes監査イベントで一意であるため、すべてのメトリクスデータポイントが独自のMTSを作成するようになります。これはカーディナリティの爆発であり、メトリクスは技術的にはより詳細になりますが、これらの単発の時系列はすべて、チャートやアラートに実際に使用できる価値を提供することなく、利用量を膨らませます。

![Metric Timeseries](../../images/metric_timeseries.png?width=40vw)

{{% notice title="注意" style="info" icon="info" %}}
これは実際の環境でよくある状況です。チームが便利な識別子をディメンションとして追加すると、MTS数が予想よりもはるかに速く増加します。次の演習では、Metrics Pipeline Managementを使用して、Ingest Processor Pipelineやデータを送信するシステムに手を加えることなく、Splunk Observability Cloud UIからカーディナリティを制御下に戻します。
{{% /notice %}}

{{% /notice %}}

{{% notice title="演習: auditIDディメンションの集約と削除" style="green" icon="running" %}}

ここでは **Metrics Pipeline Management** を使用して、一意の `auditID` ディメンションを含まない新しい低カーディナリティメトリクスにメトリクスをロールアップする集約ルールを作成します。その後、不要になった高カーディナリティの生メトリクスを削除します。

**1.** Splunk Observability Cloudで、**Metrics** → **Pipeline Automation** に移動します。

![Navigate to Pipeline Automation](../../images/pipeline_automation_nav.png?width=40vw)

**2.** ページ上部の行にある **Pipeline Management** を選択します。

**3.** **Pipeline Management** ページで、**Choose a metric** ボタンをクリックします。

![Select Pipeline Management](../../images/pipeline_management_tab.png?width=40vw)

**4.** **Choose a metric** ポップアップで、Ingest Processor Pipelineで作成したメトリクス名（例: `k8s_audit_2`）を入力し、**Choose** をクリックします。

![Enter Metric Name](../../images/choose_metric_search.png?width=40vw)

**5.** **Ingestion** セクションで、**Raw MTS** の横にある **Edit** をクリックします。

![Edit Raw MTS](../../images/edit_ingest_pipeline.png?width=40vw)

{{% notice title="情報" style="info" icon="info" %}}
このページに表示されているメトリクスパイプラインを確認してください。現在、**Raw MTS** と **Real-time MTS** のカウントは同じです。これは、集約ルールやルーティングルールをまだ作成していないため、送信したすべての生MTSがリアルタイムで保存・利用可能になっているためです。次のステップでルールを追加する際に、適用している最適化を反映してこれらの値がどのように変化するかを観察してください。
{{% /notice %}}

**6.** **Update raw data routing** モーダルで、**Dropped** を選択します。これにより、受信したメトリクスデータはSplunk Observability Cloudに保存される前に破棄されます。特定のMTSを復元する必要がある場合は、ルーティング例外ルールを使用してリアルタイムに再ルーティングできます。**Update** をクリックし、次に **Enable** をクリックして更新を有効にします。

![Drop Raw Data Routing](../../images/drop_raw_data_routing.png?width=40vw)

**7.** **Added by rule** セクションで、**+ Add** をクリックして新しい集約ルールを作成します。

![Add Aggregation Rule](../../images/add_aggregation_rule.png?width=40vw)

**8.** **Create aggregation rule** モーダルで、名前に `Drop unique auditID` と入力します。

**9.** **Select dimensions** セクションで、ドロップダウンの値を **Keep** から **Drop** に変更し、検索バーを使用して **auditID** を選択します。

{{% notice title="注意" style="info" icon="info" %}}
集約されたメトリクスに新しいメトリクス名が作成されることに注目してください。この新しいメトリクスは有用なディメンションをすべて保持しますが、一意の `auditID` は含まれなくなります。次のセクションでビジュアライゼーションを作成する際に、この集約メトリクスを使用します。
{{% /notice %}}

**10.** **Data volume** セクションを確認します。ここには集約されていない **Raw MTS** と **Aggregated MTS** が表示されます。`auditID` ディメンションを削除することで得られるMTSの正確な削減量を確認できます。これが、インジェストエンドポイントで何も変更することなく回収できる利用量です。

**11.** **Create** をクリックします。

![Create Aggregation Rule](../../images/create_aggregation_rule.png?width=40vw)

{{% notice title="注意" style="info" %}}
これで、メトリクスを新しい低カーディナリティメトリクスに集約し、一意の `auditID` ディメンションを含む生メトリクスを削除しました。これらはすべて、Ingest Processor Pipelineやデータを送信するシステムに変更を加えることなく、Splunk Observability Cloud UIから実行しました。

次のステップでは、集約されたメトリクスを使用してビジュアライゼーションを作成します。
{{% /notice %}}

{{% /notice %}}
