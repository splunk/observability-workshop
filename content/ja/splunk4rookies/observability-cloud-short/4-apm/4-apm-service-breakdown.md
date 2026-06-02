---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="バージョンごとにサービスを分解する" %}}

* Service Map で **paymentservice** を選択します。
* 右側のペインで {{% button style="grey"  %}}Breakdown{{% /button %}} をクリックします。
* リストから `version` を選択します。
{{< tabs >}}
{{% tab title="質問" %}}
**表示されている内容から何が結論付けられますか?**
{{% /tab %}}
{{% tab title="回答" %}}
**`v350.9` ではエラーが発生していませんが、`v350.10` には明らかに問題があります。**
{{% /tab %}}
{{< /tabs >}}

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Span タグ" style="info" %}}
span タグを使用してサービスを分解する機能は非常に強力です。これにより、顧客別、バージョン別、リージョン別などにサービスのパフォーマンスを確認できます。この演習では、**paymentservice** の `v350.10` が問題を引き起こしていることを特定しました。
{{% /notice %}}

* 次に、何が起きているかを確認するためにトレースをドリルダウンする必要があります。**paymentservice** 内の `v350.10` の赤い円 **(1)** をクリックし、右側のペインで **Traces** **(2)** タブをクリックします。

{{% /exercise %}}
