---
title: 4. APM Service Breakdown
weight: 4
---

{{% notice title="Exercise" style="green" icon="running" %}}

* 右側のペインで {{% button style="grey"  %}}Breakdown{{% /button %}} をクリックします。
* リストから `tenant.level` を選択します。これは顧客のステータスを表すタグであり、顧客のステータスに関連するトレンドを見るのに役立ちます。
* Service Map で **gold** をクリックして選択します。
* さらに {{% button style="grey"  %}}Breakdown{{% /button %}} をクリックし、`version` を選択します。これはサービスのバージョンを示すタグです。
* **silver** と **bronze** についても同様の手順を繰り返します。
{{< tabs >}}
{{% tab title="質問" %}}
**確認できた内容から、どんな結論を得ることができますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**すべてのテナントがバージョン `v350.10` による影響を受けている**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

**paymentservice** が **gold**、**silver**、**bronze** の3つのサービスに分けて表示されていることが分かるでしょう。各テナントはバージョン (`v350.10` と `v350.9`) ごとのサービスに分けられています。

![APM サービスのBreakdown](../images/apm-service-breakdown.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* 3つの赤い円を囲む外側のメインボックスをクリックします。ボックスがハイライト表示されます。

{{% /notice %}}

{{% notice title="スパンのタグ" style="info" %}}
スパンに付与されるタグに基づいてサービスの分析は非常に強力な機能です。これにより、異なる顧客、異なるバージョン、異なる地域などに対するサービスのパフォーマンスを確認できます。この演習では、**paymentservice** の `v350.10` がすべての顧客に問題を引き起こしていることが判明しました。
{{% /notice %}}

次に、トレースを詳細に調査して問題の原因を見つける必要があります。
