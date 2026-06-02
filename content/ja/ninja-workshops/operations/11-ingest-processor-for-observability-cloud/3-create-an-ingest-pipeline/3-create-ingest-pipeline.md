---
title: Create an Ingest Pipeline
linkTitle: 3.3 Create an Ingest Pipeline
weight: 4
---

このセクションでは、Kubernetes Audit Logs をメトリクスに変換し、Splunk Observability Cloud のワークショップ組織に送信する Ingest Pipeline を作成します。

{{% notice title="演習: Ingest Pipeline の作成" style="green" icon="running" %}}

**1.** Splunk Show イベントで提供された接続情報を使用して、**Ingest Processor SCS Tenant** を開きます。

![Launch Splunk Cloud Platform](../../images/data_management_home.png?width=40vw)

{{% notice title="Note" style="primary" icon="lightbulb" %}}

**Ingest Processor SCS Tenant** を開いた際に Welcome ページが表示された場合は、**Splunk Cloud Platform** の下にある **Launch** をクリックすると、Ingest Pipeline を構成する Data Management ページに移動します。

![Launch Splunk Cloud Platform](../../images/launch_scp.png)

{{% /notice %}}

**2.** Splunk Data Management コンソールから **Pipelines** → **New pipeline** → **Ingest Processor pipeline** を選択します。

![New Ingest Processor Pipeline](../../images/new_pipeline.png?width=40vw)

**3.** Ingest Processor 構成ページの **Get started** ステップで **Blank Pipeline** を選択し、**Next** をクリックします。

![Blank Ingest Processor Pipeline](../../images/blank_pipeline.png?width=40vw)

**4.** Ingest Processor 構成ページの **Define your pipeline’s partition** ステップで **Partition by sourcetype** を選択します。Operator として **= equals** を選択し、値に `kube:apiserver:audit:USER_ID` を入力します（USER_ID は割り当てられたユーザー ID に置き換えてください）。**Apply** をクリックします。

![Add Partition](../../images/add_partition.png?width=40vw)

**5.** **Next** をクリックします。

**6.** Ingest Processor 構成ページの **Add sample data** ステップで **Capture new snapshot** を選択します。Snapshot 名に `k8s_audit_USER_ID` を入力し（USER_ID は割り当てられたユーザー ID に置き換えてください）、**Capture** をクリックします。

![Capture Snapshot](../../images/capture_snapshot.png?width=40vw)

**7.** 新しく作成した snapshot（`k8s_audit_USER_ID`）が選択されていることを確認し、**Next** をクリックします。

![Configure Snapshot Sourcetype](../../images/capture_snapshot_sourcetype.png?width=20vw)

**8.** Ingest Processor 構成ページの **Select a metrics destination** ステップで **show_o11y_org** を選択します。**Next** をクリックします。

![Metrics Destination](../../images/metrics_destination.png?width=20vw)

**9.** Ingest Processor 構成ページの **Select a data destination** ステップで **splunk_indexer** を選択します。**Specify how you want your events to be routed to an index** で **Default** を選択します。**Done** をクリックします。

![Event Routing](../../images/event_routing.png?width=20vw)

**10.** **Pipeline search field** で、デフォルトのサーチを以下の内容に置き換えます。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**メトリクス名の `UNIQUE_FIELD` を、Observability Cloud で自分のメトリクスを識別するために使用する一意の値（イニシャルなど）に置き換えてください。**
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

{{% notice title="SPL2 が初めての方へ" style="info" icon="lightbulb" %}}

この SPL2 クエリで実行している内容の詳細は以下のとおりです。

* 最初に、Kubernetes イベントをメトリクスに変換するために使用する組み込みの `logs_to_metrics` コマンドを import しています。
* ソースデータを使用しており、右側で確認できるように `kube:apiserver:audit` sourcetype のすべてのイベントが対象となります。
* 次に、`thru` コマンドを使用して、ソースデータセットを後続のコマンド（この場合は `logs_to_metrics`）に書き込みます。
* メトリクス名（`k8s_audit`）、メトリクスタイプ（`counter`）、値、タイムスタンプがすべてメトリクスに対して指定されていることが確認できます。イベントの発生回数をカウントしたいので、このメトリクスには値 1 を使用しています。
* 次に、`into $metrics_destintation` コマンドを使用してメトリクスの送信先（Splunk Observability Cloud 組織）を指定します。
* 最後に、生のログイベントを別の送信先（この場合は別のインデックス）に送信できるため、必要に応じてアクセスできるよう保持されます。

{{% /notice %}}

**11.** 右上の **Preview** ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（Mac の場合は CMD+Enter）を押します。**Previewing $pipeline** ドロップダウンから **$metrics_destination** を選択します。Splunk Observability Cloud に送信されるメトリクスのプレビューが表示されることを確認します。

![Preview Pipeline](../../images/preview_pipeline.png?width=40vw)

**12.** 右上の **Save pipeline** ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。pipeline 名に `Kubernetes Audit Logs2Metrics USER_ID` を入力し、**Save** をクリックします。

![Save Pipeline Dialog](../../images/save_pipeline_dialog.png?width=40vw)

**13.** Save をクリックすると、新しく作成した pipeline を適用するか確認されます。**Yes, apply** をクリックします。

![Apply Pipeline Dialog](../../images/apply_pipeline_dialog.png?width=40vw)

{{% notice title="Note" style="info" %}}
Ingest Pipeline は Splunk Observability Cloud にメトリクスを送信しているはずです。次のセクションでも使用するため、このタブは開いたままにしておいてください。

次のステップでは、Splunk Observability Cloud で作成したメトリクスを表示して、pipeline が動作していることを確認します。
{{% /notice %}}

{{% /notice %}}
