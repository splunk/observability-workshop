---
title: Ingest Pipeline の更新
linkTitle: 4.1 Ingest Pipeline の更新
weight: 2
---

{{% notice title="演習: Ingest Pipeline の更新" style="green" icon="running" %}}

**1.** 前のステップで作成した Ingest Pipeline の設定ページに戻ります。

![Ingest Pipeline](../../images/ingest_pipeline.png?width=40vw)

**2.** 生の Kubernetes Audit ログからメトリクスにディメンションを追加するには、パイプライン用に作成した SPL2 クエリの `logs_to_metrics` 部分を以下に置き換えて更新します：

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**メトリクス名フィールド（`name="k8s_audit_UNIQUE_FIELD"`）を、元のパイプラインで指定した名前に更新してください。**
{{% /notice %}}

```text
| logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time dimensions={"level": _raw.level, "response_status": _raw.responseStatus.code, "namespace": _raw.objectRef.namespace, "resource": _raw.objectRef.resource, "user": _raw.user.username, "action": _raw.verb}
```

{{% notice title="Note" style="info" icon="info" %}}
SPL2 クエリの `dimensions` フィールドを使用して、生のイベントからのディメンションを Splunk Observability Cloud に送信されるメトリクスに追加できます。この場合、イベントのレスポンスステータス、名前空間、Kubernetes リソース、ユーザー、および verb（実行されたアクション）を追加しています。これらのディメンションを使用して、より詳細なダッシュボードとアラートを作成できます。

Splunk Observability Cloud でコンテキスト伝播と関連コンテンツを活用できるように、サービス全体で共通のタグを追加することを検討してください。
{{% /notice %}}

更新されたパイプラインは以下のようになります：

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

**3.** 右上隅の **Preview** ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（Mac では CMD+Enter）を押します。**Previewing $pipeline** ドロップダウンから **$metrics_destination** を選択します。Splunk Observability Cloud に送信されるメトリクスのプレビューが表示されていることを確認します。

![Ingest Pipeline Dimensions](../../images/ingest_pipeline_dimensions.png?width=40vw)

**4.** プレビューテーブルの dimensions 列にディメンションが表示されていることを確認します。テーブルをクリックすると、dimensions オブジェクト全体を表示できます。

![Ingest Pipeline Dimensions Review](../../images/ingest_pipeline_dimensions_field.png?width=40vw)

**5.** 右上隅の **Save pipeline** ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。「You are editing an active pipeline」モーダルで **Save** をクリックします。

![Save Updated Pipeline](../../images/save_updated_pipeline.png?width=30vw)

{{% notice title="Note" style="info" %}}
このパイプラインはすでにアクティブであるため、行った変更はすぐに有効になります。追加したディメンションを使用して、メトリクスは複数のメトリクス時系列に分割されるはずです。

次のステップでは、Kubernetes Audit イベントからの異なるディメンションを使用して可視化を作成します。
{{% /notice %}}

{{% /notice %}}
