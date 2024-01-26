---
title: 4. APM サービスの分解
weight: 4
---

{{% notice title="演習" style="green" icon="running" %}}

* 右側のペインで {{% button style="grey"  %}}分解{{% /button %}} をクリックします。
* リストから `tenant.level` を選択します。これは顧客のステータスを露出するタグであり、顧客のステータスに関連するトレンドを見るのに役立ちます。
* Service Map で **gold** をクリックして選択します。
* {{% button style="grey"  %}}分解{{% /button %}} をクリックし、`version` を選択します。これはサービスのバージョンを示すタグです。
* **silver** と **bronze** についても同様の手順を繰り返します。
{{< tabs >}}
{{% tab title="質問" %}}
**見ているものから何を結論付けることができますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**すべてのテナントが `v350.10` に影響を受けている**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

これで **paymentservice** が **gold**、**silver**、**bronze** の三つのサービスに分解されます。各テナントは二つのサービスに分かれ、それぞれのバージョン (`v350.10` と `v350.9`) が対応しています。

![APM サービスの分解](../images/apm-service-breakdown.png)

{{% notice title="演習" style="green" icon="running" %}}

* 3 つの赤い円を囲む外側のメインボックスをクリックします。ボックスがハイライト表示されます。

{{% /notice %}}

{{% notice title="スパンのタグ" style="info" %}}
サービスを分解するためにスパンのタグを使用すると、異なる顧客、異なるバージョン、異なる地域などに対するサービスのパフォーマンスを確認できます。この演習では、**paymentservice** の `v350.10` がすべての顧客に問題を引き起こしていることが判明しました。
{{% /notice %}}

次に、トレースを詳細に調査して問題の原因を見つける必要があります。
