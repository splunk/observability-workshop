---
title: Ingest Pipelineの更新
linkTitle: 4.1 Ingest Pipelineの更新
weight: 2
---

{{% notice title="演習: Ingest Pipelineの更新" style="green" icon="running" %}}

**1.** 前のステップで作成したIngest Pipelineの設定ページに戻ります。

![Ingest Pipeline](../../images/ingest_pipeline.png?width=40vw)

**2.** 生のKubernetes監査ログからメトリクスにディメンションを追加するために、パイプライン用に作成したSPL2クエリの `logs_to_metrics` 部分を以下の内容に置き換えます。

{{% notice title="注意" style="primary" icon="lightbulb" %}}
**メトリクス名フィールド（ `name="k8s_audit_UNIQUE_FIELD"` ）を、元のパイプラインで指定した名前に必ず更新してください**
{{% /notice %}}

```text
| logs_to_metrics name="k8s_audit_UNIQUE_FIELD" metrictype="counter" value=1 time=_time dimensions={"level": _raw.level, "response_status": _raw.responseStatus.code, "namespace": _raw.objectRef.namespace, "resource": _raw.objectRef.resource, "user": _raw.user.username, "action": _raw.verb, "auditID": _raw.auditID}
```

{{% notice title="注意" style="info" icon="info" %}}
SPL2クエリの `dimensions` フィールドを使用すると、生イベントからSplunk Observability Cloudに送信されるメトリクスにディメンションを追加できます。この場合、イベントのレスポンスステータス、名前空間、Kubernetesリソース、ユーザー、および動詞（実行されたアクション）を追加しています。これらのディメンションを使用して、より詳細なダッシュボードやアラートを作成できます。

サービス間で共通のタグを追加することを検討してください。これにより、Splunk Observability Cloudでコンテキストプロパゲーションや関連コンテンツを活用できます。
{{% /notice %}}

更新後のパイプラインは以下のようになります。

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

**3.** 右上の **Preview** ボタン ![Preview Button](../../images/preview.png?height=20px&classes=inline) をクリックするか、CTRL+Enter（Macの場合はCMD+Enter）を押します。 **Previewing $pipeline** ドロップダウンから **$metrics_destination** を選択します。Splunk Observability Cloudに送信されるメトリクスのプレビューが表示されることを確認します。

![Ingest Pipeline Dimensions](../../images/ingest_pipeline_dimensions.png?width=40vw)

**4.** プレビューテーブルのディメンション列にディメンションが表示されていることを確認します。テーブル内をクリックすると、ディメンションオブジェクト全体を表示できます。

![Ingest Pipeline Dimensions Review](../../images/ingest_pipeline_dimensions_field.png?width=40vw)

**5.** 右上の **Save pipeline** ボタン ![Save Pipeline Button](../../images/save_pipeline_btn.png?height=20px&classes=inline) をクリックします。「You are editing an active pipeline」モーダルで **Save** をクリックします。

![Save Updated Pipeline](../../images/save_updated_pipeline.png?width=30vw)

{{% notice title="注意" style="info" %}}
このパイプラインはすでにアクティブであるため、変更は直ちに反映されます。メトリクスは、追加したディメンションを使用して複数のメトリクスタイムシリーズに分割されます。

次のステップでは、Kubernetes監査イベントのさまざまなディメンションを使用してビジュアライゼーションを作成します。
{{% /notice %}}

{{% /notice %}}
