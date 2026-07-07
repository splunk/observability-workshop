---
title: Ingest Pipeline の作成
linkTitle: 3.3 Ingest Pipeline の作成
weight: 4
---

このセクションでは、Kubernetes Audit Logs をメトリクスに変換し、Splunk Observability Cloud のワークショップ組織に送信する Ingest Pipeline を作成します。

{{% notice title="演習: Ingest Pipeline の作成" style="green" icon="running" %}}

**1.** Splunk Show イベントで提供された接続情報を使用して、**Ingest Processor SCS Tenant** を開きます。

![Launch Splunk Cloud Platform](../../images/data_management_home.png?width=40vw)

{{% notice title="Note" style="primary" icon="lightbulb" %}}

**Ingest Processor SCS Tenant** を開いた際にウェルカムページが表示された場合は、**Splunk Cloud Platform** の下にある **Launch** をクリックして、Ingest Pipeline を設定する Data Management ページに移動してください。

![Launch Splunk Cloud Platform](../../images/launch_scp.png)

{{% /notice %}}

**2.** Splunk Data Management コンソールから **Pipelines** → **New pipeline** → **Ingest Processor pipeline** を選択します。

![New Ingest Processor Pipeline](../../images/new_pipeline.png?width=40vw)

**3.** Ingest Processor 設定ページの **Get started** ステップで **Blank Pipeline** を選択し、**Next** をクリックします。

![Blank Ingest Processor Pipeline](../../images/blank_pipeline.png?width=40vw)

**4.** Ingest Processor 設定ページの **Define your pipeline's partition** ステップで **Partition by sourcetype** を選択します。**= equals** Operator を選択し、値として `kube:apiserver:audit:USER_ID`（USER_ID は割り当てられたユーザー ID に置き換えてください）を入力します。**Apply** をクリックします。

![Add Partition](../../images/add_partition.png?width=40vw)

**5.** **Next** をクリックします。

**6.** Ingest Processor 設定ページの **Add sample data** ステップで **Capture new snapshot** を選択します。Snapshot name に `k8s_audit_USER_ID`（USER_ID は割り当てられたユーザー ID に置き換えてください）を入力し、**Capture** をクリックします。

![Capture Snapshot](../../images/capture_snapshot.png?width=40vw)

**7.** 新しく作成したスナップショット（`k8s_audit_USER_ID`）が選択されていることを確認し、**Next** をクリックします。

![Configure Snapshot Sourcetype](../../images/capture_snapshot_sourcetype.png?width=20vw)

**8.** Ingest Processor 設定ページの **Select a destination for $destination** ステップで **splunk_indexer** を選択します。**Specify how you want your events to be routed to an index** の下で **Default** を選択します。**Done** をクリックします。

![Event Routing](../../images/event_routing.png?width=20vw)

**9.** **Pipeline search field** でデフォルトの検索を以下の内容に置き換えます。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**メトリクス名の `UNIQUE_FIELD` を、Observability Cloud でメトリクスを識別するために使用する一意の値（イニシャルなど）に置き換えてください。**
{{% /notice %}}

```text
/*A valid SPL2 statement for a pipeline must start with "$pipeline", and include "from $source" and "into $destination".*/
/* Import logs_to_metrics */
import logs_to_metrics from /splunk/ingest/commands
$pipeline =
| from $source
| thru [
        //define the metric name, type, and value for the Kubernetes Events
        //
        // REPLACE UNIQUE_FIELD WITH YOUR INITIALS
        //
        | logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time
        | into $metrics_destination
    ]
| eval index = "kube_logs"
| into $destination;
```

{{% notice title="SPL2 が初めてですか？" style="info" icon="lightbulb" %}}

この SPL2 クエリの処理内容を説明します

* まず、Kubernetes イベントをメトリクスに変換するために使用する組み込みの `logs_to_metrics` コマンドをインポートしています。
* ソースデータを使用しています。右側に表示されているように、`kube:apiserver:audit` sourcetype からのすべてのイベントが対象です。
* 次に、`thru` コマンドを使用して、ソースデータセットを後続のコマンド（この場合は `logs_to_metrics`）に書き込みます。
* メトリクス名（`k8s_audit`）、メトリクスタイプ（`counter`）、値、タイムスタンプがすべてメトリクスに提供されています。イベントが発生した回数をカウントするため、値として 1 を使用しています。
* 次に、`$metrics_destintation` コマンドの into を使用してメトリクスの宛先を選択します。これは Splunk Observability Cloud 組織です。
* 最後に、生のログイベントを別の宛先（この場合は別のインデックス）に送信して、後でアクセスする必要がある場合に備えて保持します。

{{% /notice %}}

**10.** SPL2 ステートメントを更新した後、右側の Pipeline details の `Actions` セクションの下にある `$metrics_destination` をクリックして、メトリクスの宛先を設定します。

![Preview Pipeline](../../images/pipeline_metrics_destination.png?width=40vw)

**11.** 宛先として `show_o11y_org` を選択し、`Apply` をクリックします。Kubernetes イベントログから作成されたメトリクスが、選択した **Splunk Observability Cloud** 組織に送信されるようになります。

![Preview Pipeline](../../images/pipeline_metrics_destination_apply.png?width=40vw)

**12.** 右上の **Preview** ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（Mac の場合は CMD+Enter）を押します。**Previewing $pipeline** ドロップダウンから **$metrics_destination** を選択します。Splunk Observability Cloud に送信されるメトリクスのプレビューが表示されていることを確認します。

![Preview Pipeline](../../images/preview_pipeline.png?width=40vw)

**13.** 右上の **Save pipeline** ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。パイプライン名として `Kubernetes Audit Logs2Metrics USER_ID` を入力し、**Save** をクリックします。

![Save Pipeline Dialog](../../images/save_pipeline_dialog.png?width=40vw)

**14.** 保存をクリックすると、新しく作成したパイプラインを適用するかどうか確認されます。**Yes, apply** をクリックします。

![Apply Pipeline Dialog](../../images/apply_pipeline_dialog.png?width=40vw)

{{% notice title="Note" style="info" %}}
Ingest Pipeline が Splunk Observability Cloud にメトリクスを送信しているはずです。次のセクションで再度使用するため、このタブは開いたままにしておいてください。

次のステップでは、Splunk Observability Cloud で作成したメトリクスを表示して、パイプラインが正常に動作していることを確認します。
{{% /notice %}}

{{% /notice %}}
