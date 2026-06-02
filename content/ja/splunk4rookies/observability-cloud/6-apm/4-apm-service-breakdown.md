---
title: 4. APM Service Breakdown
weight: 4
---

{{% exercise title="テナントレベルで分解する" %}}

* Service Map で **paymentservice** を選択します。
* 右側のペインで {{% button style="grey"  %}}Breakdown{{% /button %}} をクリックします。
* リストから `tenant.level` を選択します。
* Service Map に戻り、**gold** をクリックします。
* {{% button style="grey"  %}}Breakdown{{% /button %}} をクリックし、`version` を選択します。これはサービスのバージョンを表すタグです。
* **silver** と **bronze** に対しても同じ操作を繰り返します。
{{< tabs >}}
{{% tab title="質問" %}}
**今見えているものから何が結論できますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**すべての `tenant.level` が `v350.10` の影響を受けています**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

これで **paymentservice** が **gold**、**silver**、**bronze** の3つのサービスに分解されたのが確認できます。各テナントはさらにバージョンごと（`v350.10` と `v350.9`）に2つのサービスに分解されます。

![APM Service Breakdown](../images/apm-service-breakdown.png)

{{% notice title="Span タグ" style="info" %}}
span タグを使ってサービスを分解する機能は非常に強力です。これにより、顧客ごと、バージョンごと、リージョンごとなど、さまざまな観点でサービスのパフォーマンスを確認できます。この演習では、**paymentservice** の `v350.10` がすべての顧客に問題を引き起こしていることが判明しました。
{{% /notice %}}

次に、何が起こっているのかを確認するためにトレースをドリルダウンしていきます。
