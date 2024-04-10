---
title: 3. APM Tag Spotlight
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice** のタグを表示するには、**paymentservice** をクリックし、右側のメニューパネルで **Tag Spotlight** をクリックします（画面解像度によってはスクロールが必要な場合があります）。
* **Tag Spotlight** に移動したら、**Show tags with no values** のトグルスイッチがオフになっていることを確認してください。

{{% /notice %}}

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

**Tag Spotlight** には、2つの表示モードがあります。デフォルトは **Request/Errors** で、もう1つは **Latency** です。

Request/Error チャートでは、リクエストの合計数、エラーの合計数、および根本原因のエラーが表示されます。Latency チャートでは、p50、p90、および p99 のレイテンシが表示されます。これらの値は、Splunk APM がインデックス化された各スパンタグに対して生成する Troubleshooting MetricSets（TMS）に基づいています。これらは RED メトリクス（リクエスト、エラー、および所要時間）として知られています。

{{% notice title="Exercise" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="質問" %}}
**どのチャートが問題を特定するタグでしょうか？**
{{% /tab %}}
{{% tab title="回答" %}}
***version* チャートです。`v350.10` に対するリクエストの数はエラーの数と一致しています。**
{{% /tab %}}
{{< /tabs >}}

* これで、問題を引き起こしている **paymentservice** のバージョンを特定したので、エラーに関する詳細情報を見つけることができるかどうかを確認してみましょう。ページの上部にある **← Tag Spotlight** をクリックして Service Map に戻ります。

{{% /notice %}}
