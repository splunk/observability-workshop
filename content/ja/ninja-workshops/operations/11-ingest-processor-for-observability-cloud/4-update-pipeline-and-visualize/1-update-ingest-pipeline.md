---
title: Ingest Pipeline の更新
linkTitle: 4.1 Ingest Pipeline の更新
weight: 2
---

{{% notice title="演習: Ingest Pipeline の更新" style="green" icon="running" %}}

**1.** 前のステップで作成した Ingest Pipeline の設定ページに戻ります。

![Ingest Pipeline](../../images/ingest_pipeline.png?width=40vw)

**2.** 生の Kubernetes 監査ログからメトリクスにディメンションを追加するために、パイプライン用に作成した SPL2 クエリの `logs_to_metrics` 部分を以下の内容に置き換えます

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**メトリクス名フィールド（`name="k8s_audit_UNIQUE_FIELD"`）を、元のパイプラインで指定した名前に必ず更新してください**
{{% /notice %}}

```text
| logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time dimensions={"level": _raw.level, "response_status": _raw.responseStatus.code, "namespace": _raw.objectRef.namespace, "resource": _raw.objectRef.resource, "user": _raw.user.username, "action": _raw.verb, "auditID": _raw.auditID}
```

{{% notice title="Note" style="info" icon="info" %}}
SPL2 クエリの `dimensions` フィールドを使用することで、生のイベントから Splunk Observability Cloud に送信されるメトリクスにディメンションを追加できます。この例では、イベントのレスポンスステータス、名前空間、Kubernetes リソース、ユーザー、および動詞（実行されたアクション）を追加しています。これらのディメンションを使用して、より詳細なダッシュボードやアラートを作成できます。

サービス間で共通のタグを追加することを検討してください。これにより、Splunk Observability Cloud のコンテキスト伝播と関連コンテンツを活用できます。
{{% /notice %}}

更新後のパイプラインは以下のようになります

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
        | logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time dimensions={"level": _raw.level, "response_status": _raw.responseStatus.code, "namespace": _raw.objectRef.namespace, "resource": _raw.objectRef.resource, "user": _raw.user.username, "action": _raw.verb, "auditID": _raw.auditID}
        | into $metrics_destination
    ]
| eval index = "kube_logs"
| into $destination;
```

**3.** 右上隅にある **Preview** ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（Mac の場合は CMD+Enter）を押します。**Previewing $pipeline** ドロップダウンから **$metrics_destination** を選択します。Splunk Observability Cloud に送信されるメトリクスのプレビューが表示されていることを確認します。

![Ingest Pipeline Dimensions](../../images/ingest_pipeline_dimensions.png?width=40vw)

**4.** プレビューテーブルの dimensions 列にディメンションが表示されていることを確認します。テーブルのセルをクリックすると、dimensions オブジェクト全体を表示できます。

![Ingest Pipeline Dimensions Review](../../images/ingest_pipeline_dimensions_field.png?width=40vw)

**5.** 右上隅にある **Save pipeline** ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。「You are editing an active pipeline」モーダルで **Save** をクリックします。

![Save Updated Pipeline](../../images/save_updated_pipeline.png?width=30vw)

{{% notice title="Note" style="info" %}}
このパイプラインはすでにアクティブであるため、変更は即座に反映されます。メトリクスは、追加したディメンションを使用して複数のメトリクスタイムシリーズに分割されます。

次のステップでは、Kubernetes 監査イベントのさまざまなディメンションを使用してビジュアライゼーションを作成します。
{{% /notice %}}

{{% /notice %}}
