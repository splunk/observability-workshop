---
title: Ingest Pipeline の作成
linkTitle: 3.3 Ingest Pipeline の作成
weight: 4
---

このセクションでは、Kubernetes AuditログをSplunk Observability Cloudワークショップ組織に送信されるメトリクスに変換するIngest Pipelineを作成します。

{{% notice title="演習: Ingest Pipelineの作成" style="green" icon="running" %}}

**1.** Splunk Showイベントで提供された接続情報を使用して、**Ingest Processor SCS Tenant** を開きます。

![Launch Splunk Cloud Platform](../../images/data_management_home.png?width=40vw)

{{% notice title="Note" style="primary" icon="lightbulb" %}}

**Ingest Processor SCS Tenant** を開いた際、ウェルカムページに移動した場合は、**Splunk Cloud Platform** の下にある **Launch** をクリックして、Ingest Pipelineを設定するData Managementページに移動してください。

![Launch Splunk Cloud Platform](../../images/launch_scp.png)

{{% /notice %}}

**2.** Splunk Data Managementコンソールから **Pipelines** → **New pipeline** → **Ingest Processor pipeline** を選択します。

![New Ingest Processor Pipeline](../../images/new_pipeline.png?width=40vw)

**3.** Ingest Processor設定ページの **Get started** ステップで、**Blank Pipeline** を選択し、**Next** をクリックします。

![Blank Ingest Processor Pipeline](../../images/blank_pipeline.png?width=40vw)

**4.** Ingest Processor設定ページの **Define your pipeline's partition** ステップで、**Partition by sourcetype** を選択します。**= equals** Operatorを選択し、値として `kube:apiserver:audit:USER_ID` を入力します（USER_IDを割り当てられたUser IDに置き換えてください）。**Apply** をクリックします。

![Add Partition](../../images/add_partition.png?width=40vw)

**5.** **Next** をクリックします。

**6.** Ingest Processor設定ページの **Add sample data** ステップで、**Capture new snapshot** を選択します。Snapshot nameに `k8s_audit_USER_ID` と入力し（USER_IDを割り当てられたUser IDに置き換えてください）、**Capture** をクリックします。

![Capture Snapshot](../../images/capture_snapshot.png?width=40vw)

**7.** 新しく作成したスナップショット（`k8s_audit_USER_ID`）が選択されていることを確認し、**Next** をクリックします。

![Configure Snapshot Sourcetype](../../images/capture_snapshot_sourcetype.png?width=20vw)

**8.** Ingest Processor設定ページの **Select a metrics destination** ステップで、**show_o11y_org** を選択します。**Next** をクリックします。

![Metrics Destination](../../images/metrics_destination.png?width=20vw)

**9.** Ingest Processor設定ページの **Select a data destination** ステップで、**splunk_indexer** を選択します。**Specify how you want your events to be routed to an index** の下で、**Default** を選択します。**Done** をクリックします。

![Event Routing](../../images/event_routing.png?width=20vw)

**10.** **Pipeline search field** で、デフォルトの検索を以下に置き換えます。

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

{{% notice title="SPL2が初めてですか？" style="info" icon="lightbulb" %}}

SPL2クエリが行っていることの内訳は以下の通りです：

* まず、Kubernetesイベントをメトリクスに変換するために使用される組み込みの `logs_to_metrics` コマンドをインポートしています。
* 右側に表示されている、`kube:apiserver:audit` sourcetypeからの任意のイベントであるソースデータを使用しています。
* 次に、`thru` コマンドを使用して、ソースデータセットを次のコマンド（この場合は `logs_to_metrics`）に書き込みます。
* メトリクス名（`k8s_audit`）、メトリクスタイプ（`counter`）、値、タイムスタンプがすべてメトリクスに提供されていることがわかります。イベントが発生した回数をカウントしたいため、このメトリクスには値として1を使用しています。
* 次に、into `$metrics_destintation` コマンドを使用してメトリクスの宛先を選択します。これはSplunk Observability Cloud組織です。
* 最後に、生のログイベントを別の宛先（この場合は別のインデックス）に送信できるため、アクセスが必要になった場合に保持されます。

{{% /notice %}}

**11.** 右上隅の **Preview** ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（MacではCMD+Enter）を押します。**Previewing $pipeline** ドロップダウンから **$metrics_destination** を選択します。Splunk Observability Cloudに送信されるメトリクスのプレビューが表示されていることを確認します。

![Preview Pipeline](../../images/preview_pipeline.png?width=40vw)

**12.** 右上隅の **Save pipeline** ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。パイプライン名に `Kubernetes Audit Logs2Metrics USER_ID` と入力し、**Save** をクリックします。

![Save Pipeline Dialog](../../images/save_pipeline_dialog.png?width=40vw)

**13.** 保存をクリックすると、新しく作成したパイプラインを適用するかどうか尋ねられます。**Yes, apply** をクリックします。

![Apply Pipeline Dialog](../../images/apply_pipeline_dialog.png?width=40vw)

{{% notice title="Note" style="info" %}}
Ingest Pipelineは現在Splunk Observability Cloudにメトリクスを送信しているはずです。次のセクションで再び使用するため、このタブを開いたままにしておいてください。

次のステップでは、Splunk Observability Cloudで作成したメトリクスを表示して、パイプラインが動作していることを確認します。
{{% /notice %}}

{{% /notice %}}
