---
title: 3. APM Tag Spotlight
weight: 3
---

{{% exercise title="Tag Spotlight で問題のあるバージョンを見つける" %}}

* **Tag Spotlight** に入ったら、**Show tags with no values** トグルがオフになっていることを確認します。

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

* このビューには一連のカードが表示され、それぞれがインデックス化されたタグ（Endpoint、Environment、Version、または tenant.level のようなカスタムタグなど）を表しています。各カードでは、タグ値の分布に加えて、リクエスト数、エラー数、ルート原因エラー、レイテンシパーセンタイル（P50、P90、P99）などの主要メトリクスを確認できます。

{{< tabs >}}
{{% tab title="質問" %}}
**問題が何であるかを特定するタグを示しているカードはどれでしょうか?**
{{% /tab %}}
{{% tab title="回答" %}}
***version* カードです。`v350.10` に対するリクエスト数とエラー数が一致しており、つまり 100% です**
{{% /tab %}}
{{< /tabs >}}

* 問題を示すタグが特定できたので、エラーに関するさらなる情報を見つけられるか確認しましょう。
* ページ上部の **paymentservice** の上にある **APM** リンクをクリックして、**APM Overview** に戻ります。
* **APM Overview** で、右側のペインにある **Service Map** をクリックします。
{{% /exercise %}}
