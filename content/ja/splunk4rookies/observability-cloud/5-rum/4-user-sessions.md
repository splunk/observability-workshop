---
title: 4. User Sessions
weight: 4
---
{{% exercise title="APMへのジャンプオフポイントを見つける" %}}

* 右上の **X** をクリックして RUM Session Replay を閉じます。
* スパンの長さに注目してください。これは注文完了までにかかった時間です。良くないですね！
* ページを下にスクロールすると、**Tags** メタデータ（Tag Spotlight で使用されます）が表示されます。タグの後には、ロードされたページオブジェクト（HTML、CSS、画像、JavaScript など）を示すウォーターフォールが表示されます。
* ページをさらにスクロールして、青い **APM** リンク（URL の末尾が `/cart/checkout` のもの）が出てくるまで進み、そこにマウスオーバーします。

{{% /exercise %}}

![RUM Session](../images/rum-waterfall.png)

これにより、APM Performance Summary が表示されます。このようなエンドツーエンド（RUM から APM）のビューは、問題のトラブルシューティングに非常に役立ちます。

{{% exercise title="RUM から APM へジャンプする" %}}

* 上のスクリーンショットのように、**paymentservice** と **checkoutservice** がエラー状態になっていることがわかります。
* **Workflow Name** の下にある `front-end:/cart/checkout` をクリックすると、**APM Service Map** が表示されます。

{{% /exercise %}}

![RUM to APM](../images/rum-to-apm.png)
