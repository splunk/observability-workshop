---
title: 4. APMサービスブレイクダウン
weight: 4
---

{{% notice title="演習" style="green" icon="running" %}}

- サービスマップで**paymentservice**を選択します。
- 右側のペインで{{% button style="grey"  %}}Breakdown{{% /button %}}をクリックします。
- リストから`tenant.level`を選択します。
- サービスマップに戻り、**gold**をクリックします。
- {{% button style="grey"  %}}Breakdown{{% /button %}}をクリックして`version`を選択します。これはサービスバージョンを表示するタグです。
- これを**silver**と**bronze**についても繰り返します。

{{< tabs >}}
{{% tab title="質問" %}}
**表示されている内容からどのような結論が導き出せますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**すべての`tenant.level`が`v350.10`の影響を受けています**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

これで**paymentservice**が**gold**、**silver**、**bronze**の 3 つのサービスに分解されているのが確認できます。各テナントは 2 つのサービスに分解されており、それぞれのバージョン（`v350.10`と`v350.9`）に対応しています。

![APMサービスブレイクダウン](../images/apm-service-breakdown.png)

{{% notice title="スパンタグ" style="info" %}}

スパンタグを使用してサービスを分解することは非常に強力な機能です。これにより、異なる顧客、異なるバージョン、異なる地域などに対して、サービスがどのようにパフォーマンスを発揮しているかを確認できます。この演習では、**paymentservice**の`v350.10`がすべての顧客に問題を引き起こしていることを特定しました。

{{% /notice %}}

次に、何が起きているかを確認するためにトレースを詳しく調べる必要があります。
