---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="バージョンごとにサービスを分解する" %}}

* Service Map で **paymentservice** を選択します。
* 右側のペインで {{% button style="grey"  %}}Breakdown{{% /button %}} をクリックします。
* リストから `version` を選択します。
{{< tabs >}}
{{% tab title="Question" %}}
**ここから何がわかりますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**`v350.9` ではエラーが発生していませんが、`v350.10` には明らかに問題があることがわかります。**
{{% /tab %}}
{{< /tabs >}}

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Span Tags" style="info" %}}
Span タグを使ってサービスを分解することは非常に強力な機能です。これにより、顧客ごと、バージョンごと、リージョンごとなど、さまざまな切り口でサービスのパフォーマンスを確認できます。この演習では、**paymentservice** の `v350.10` が問題を引き起こしていることが特定できました。
{{% /notice %}}

* 次に、何が起きているのかを確認するためにトレースをドリルダウンしていきます。**paymentservice** の `v350.10` の赤い円 **(1)** をクリックし、右側のペインの **Traces** **(2)** タブをクリックします。

{{% /exercise %}}
