---
title: Confirm Metrics in Observability Cloud
linkTitle: 3.4 Confirm Metrics in Observability Cloud
weight: 5
---

Kubernetes Audit Logs をメトリクスに変換して Splunk Observability Cloud に送信するための Ingest Pipeline を構成しましたので、メトリクスが利用可能になっているはずです。メトリクスが収集されていることを確認するには、次の手順を実行してください。

{{% notice title="Exercise: Confirm Metrics in Splunk Observability Cloud" style="green" icon="running" %}}

**1.** ワークショップに招待された **Splunk Observability Cloud** organization にログインします。右上隅で **+** アイコン → **Chart** をクリックして、新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** に、**Ingest Pipeline** の構成時に使用したメトリクス名を入力します。

![Review Metric](../../images/review_metric.png?width=40vw)

{{% notice title="Info" style="info" %}}
Ingest Pipeline で作成したメトリクスが表示されているはずです。次のセクションでも使用しますので、このタブは開いたままにしてください。

次のステップでは、ingest pipeline を更新してメトリクスにディメンションを追加し、アラートやトラブルシューティングのための追加のコンテキストを得られるようにします。
{{% /notice %}}

{{% /notice %}}
