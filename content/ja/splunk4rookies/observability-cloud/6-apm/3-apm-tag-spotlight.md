---
title: 3. APM Tag Spotlight
weight: 3
---

{{% exercise title="paymentservice の Tag Spotlight を開く" %}}

* **paymentservice** のタグを表示するには、**paymentservice** をクリックし、画面右側の機能ペインにある **Tag Spotlight** をクリックします（画面解像度によってはスクロールが必要な場合があります）。* **Tag Spotlight** に入ったら、**Show tags with no values** トグルがオフになっていることを確認します。

{{% /exercise %}}

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

**Tag Spotlight** のビューは、チャートとカードの両方について設定可能です。ビューはデフォルトで **Requests & Errors** に設定されています。

カードに表示するタグメトリクスを設定することもできます。以下を任意に組み合わせて選択できます。

* Requests
* Errors
* Root cause errors
* P50 Latency
* P90 Latency
* P99 Latency

また、**Show tags with no values** トグルがオフになっていることも確認してください。

{{% exercise title="Tag Spotlight で問題のあるバージョンを特定する" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**問題を特定できるタグを示しているのはどのカードでしょうか？**
{{% /tab %}}
{{% tab title="Answer" %}}
***version* カードです。`v350.10` に対するリクエスト数とエラー数が一致しており、すなわちエラー率が 100% となっています**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

問題を引き起こしている **paymentservice** のバージョンを特定できたので、エラーに関するより詳しい情報が得られないか確認してみましょう。Service Map に戻るため、ページ上部の **← Tag Spotlight** をクリックします。
