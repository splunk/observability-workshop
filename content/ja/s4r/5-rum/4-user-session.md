---
title: 4. User Sessions
weight: 4
---
{{% notice title="Exercise" style="green" icon="running" %}}

* RUM Session Replay 右上の **X** をクリックして閉じます。前回の演習で **PlaceOrder** にフィルターを設定していました。この演習でも選択されているはずです。以下のスクリーンショット（**1**）に示されています。
* スパンの長さに注意してください。これは注文を完了するのにかかった時間です。良くありません！
* ページを下にスクロールすると、**Tags** メタデータ（Tag Spotlight で使用される）が表示されます。タグの後には、読み込まれたページオブジェクトが表示されます（HTML、CSS、画像、JavaScriptなど）。
* ページを下にスクロールして、青い **APM** リンク（URLの末尾に `/cart/checkout` が含まれているもの）にカーソルを合わせます。

{{% /notice %}}

![RUM Session](../images/rum-waterfall.png)

これにより、APM パフォーマンスサマリーが表示されます。これはトラブルシューティング時に非常に役立つエンドツーエンド（RUM から APM への）ビューです。

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice**（**2**）と **checkoutservice**（**3**）がエラー状態であることがスクリーンショットで確認できます。
* **Workflow Name** の下にある `front-end:/cart/checkout` をクリックすると、**APM Service Map** が表示されます。

{{% /notice %}}

![RUM to APM](../images/rum-to-apm.png)
