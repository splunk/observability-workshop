---
title: Ingest Pipelineの更新
linkTitle: 4.1 Ingest Pipelineの更新
weight: 2
---

{{% notice title="演習: Ingest Pipelineの更新" style="green" icon="running" %}}

**1.** 前のステップで作成したIngest Pipelineの設定ページに戻ります。

![Ingest Pipeline](../../images/ingest_pipeline.png?width=40vw)

**2.** Kubernetes監査ログの生データからメトリックにディメンションを追加するため、パイプライン用に作成したSPL2クエリの`logs_to_metrics`部分を以下の内容に置き換えて更新します。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**メトリック名フィールド（`name="k8s_audit_UNIQUE_FIELD"`）は、元のパイプラインで指定した名前に必ず更新してください**
{{% /notice %}}

```text
| logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time dimensions={"level": _raw.level, "response_status": _raw.responseStatus.code, "namespace": _raw.objectRef.namespace, "resource": _raw.objectRef.resource, "user": _raw.user.username, "action": _raw.verb}
```

{{% notice title="Note" style="info" icon="info" %}}
SPL2クエリ内の`dimensions`フィールドを使用すると、生イベントからSplunk Observability Cloudへ送信されるメトリックにディメンションを追加できます。今回の例では、イベントのレスポンスステータス、ネームスペース、Kubernetesリソース、ユーザー、verb（実行されたアクション）を追加しています。これらのディメンションを使用することで、より粒度の高いダッシュボードやアラートを作成できます。

サービス間で共通するタグを追加することで、Splunk Observability Cloudのコンテキスト伝播や関連コンテンツ機能を活用することを検討してください。
{{% /notice %}}

更新後のパイプラインは以下のようになるはずです。

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
        | logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time dimensions={"level": _raw.level, "response_status": _raw.responseStatus.code, "namespace": _raw.objectRef.namespace, "resource": _raw.objectRef.resource, "user": _raw.user.username, "action": _raw.verb}
        | into $metrics_destination
    ]
| eval index = "kube_logs"
| into $destination;
```

**3.** 右上にある**Preview**ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（MacではCMD+Enter）を押します。**Previewing $pipeline**のドロップダウンから**$metrics_destination**を選択します。Splunk Observability Cloudへ送信されるメトリックのプレビューが表示されていることを確認します。

![Ingest Pipeline Dimensions](../../images/ingest_pipeline_dimensions.png?width=40vw)

**4.** プレビューテーブルのdimensions列にディメンションが表示されていることを確認します。テーブル内をクリックすると、ディメンションオブジェクト全体を表示できます。

![Ingest Pipeline Dimensions Review](../../images/ingest_pipeline_dimensions_field.png?width=40vw)

**5.** 右上にある**Save pipeline**ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。「You are editing an active pipeline」モーダルで**Save**をクリックします。

![Save Updated Pipeline](../../images/save_updated_pipeline.png?width=30vw)

{{% notice title="Note" style="info" %}}
このパイプラインはすでにアクティブな状態のため、変更内容は即座に反映されます。これにより、追加したディメンションを使用してメトリックが複数のメトリック時系列に分割されるようになります。

次のステップでは、Kubernetes監査イベントの異なるディメンションを使用して可視化を作成します。
{{% /notice %}}

{{% /notice %}}
