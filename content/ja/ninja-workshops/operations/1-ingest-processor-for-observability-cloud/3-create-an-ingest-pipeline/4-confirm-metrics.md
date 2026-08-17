---
title: Observability Cloud でのメトリクス確認
linkTitle: 3.4 Observability Cloud でのメトリクス確認
weight: 5
---

Kubernetes Auditログをメトリクスに変換してSplunk Observability Cloudに送信するIngest Pipelineが設定されたので、メトリクスが利用可能になっているはずです。メトリクスが収集されていることを確認するには、以下の手順を完了してください：

{{% notice title="演習: Splunk Observability Cloudでのメトリクス確認" style="green" icon="running" %}}

**1.** ワークショップ用に招待された **Splunk Observability Cloud** 組織にログインします。右上隅の **+** アイコン → **Chart** をクリックして、新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** で、**Ingest Pipeline** の設定時に使用したメトリクス名を入力します。

![Review Metric](../../images/review_metric.png?width=40vw)

{{% notice title="Info" style="info" %}}
Ingest Pipelineで作成したメトリクスが表示されるはずです。次のセクションで再び使用するため、このタブを開いたままにしておいてください。

次のステップでは、Ingest Pipelineを更新してメトリクスにディメンションを追加し、アラートとトラブルシューティングのための追加コンテキストを得られるようにします。
{{% /notice %}}

{{% /notice %}}
