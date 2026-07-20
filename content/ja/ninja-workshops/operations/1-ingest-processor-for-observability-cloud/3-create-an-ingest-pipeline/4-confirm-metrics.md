---
title: Observability Cloudでメトリクスを確認する
linkTitle: 3.4 Observability Cloudでメトリクスを確認する
weight: 5
---

Ingest Pipelineを設定してKubernetes Audit Logsをメトリクスに変換し、Splunk Observability Cloudに送信するようになったので、メトリクスが利用可能になっているはずです。メトリクスが収集されていることを確認するために、以下の手順を実行します。

{{% notice title="演習: Splunk Observability Cloudでメトリクスを確認する" style="green" icon="running" %}}

**1.** ワークショップ用に招待された **Splunk Observability Cloud** の組織にログインします。右上の **+** アイコン → **Chart** をクリックして新しいチャートを作成します。

![Create New Chart](../../images/create_new_chart.png?width=40vw)

**2.** 新しく作成したチャートの **Plot Editor** で、**Ingest Pipeline** の設定時に使用したメトリクス名を入力します。

![Review Metric](../../images/review_metric.png?width=40vw)

{{% notice title="情報" style="info" %}}
Ingest Pipelineで作成したメトリクスが表示されます。このタブは次のセクションで再度使用するため、開いたままにしておいてください。

次のステップでは、Ingest Pipelineを更新してメトリクスにディメンションを追加し、アラートやトラブルシューティングのための追加コンテキストを提供します。
{{% /notice %}}

{{% /notice %}}
