---
title: 3. APM Tag Spotlight
weight: 3
---

{{% exercise title="Tag Spotlight で不具合のあるバージョンを見つける" %}}

* **Tag Spotlight** に入ったら、**Show tags with no values** トグルがオフになっていることを確認します。

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

* このビューには、インデックスされたタグ（Endpoint、Environment、Version、または tenant.level のようなカスタムタグなど）をそれぞれ表す一連のカードが表示されます。各カード内では、タグ値の分布に加えて、リクエスト数、エラー数、根本原因エラー、レイテンシーパーセンタイル（P50、P90、P99）などの主要な指標を確認できます。

{{< tabs >}}
{{% tab title="Question" %}}
**問題が何であるかを示すタグを公開しているカードはどれですか？**
{{% /tab %}}
{{% tab title="Answer" %}}
***version* カードです。`v350.10` に対するリクエスト数がエラー数と一致しており、つまり 100% です。**
{{% /tab %}}
{{< /tabs >}}

* 問題を示すタグを特定できたので、エラーに関するさらに詳しい情報を見つけられるか確認しましょう。
* ページ上部の **paymentservice** の上にある **APM** リンクをクリックして、**APM Overview** に戻ります。
* **APM Overview** で、右ペインの **Service Map** をクリックします。
{{% /exercise %}}
