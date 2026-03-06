---
title: 4. ユーザーセッション
weight: 4
---

{{% notice title="演習" style="green" icon="running" %}}

- 右上隅の**X**をクリックして、RUMセッションリプレイを閉じます。
- スパンの長さに注目してください。これは注文を完了するのにかかった時間で、良くありません！
- ページを下にスクロールすると、**タグ**メタデータ（Tag Spotlightで使用されるもの）が表示されます。タグの後に、ウォーターフォールが表示され、読み込まれたページオブジェクト（HTML、CSS、画像、JavaScriptなど）が表示されます。
- ページを下にスクロールし続けて、青い**APM**リンク（URLの末尾に `/cart/checkout` があるもの）まで移動し、その上にカーソルを置きます。

{{% /notice %}}

![RUMセッション](../images/rum-waterfall.png)

これによりAPMパフォーマンスサマリーが表示されます。このエンドツーエンド（RUMからAPM）のビューは、問題のトラブルシューティングを行う際に非常に便利です。

{{% notice title="演習" style="green" icon="running" %}}

- 上のスクリーンショットのように、**paymentservice**と**checkoutservice**がエラー状態にあることがわかります。
- **ワークフロー名**の下にある `front-end:/cart/checkout` をクリックすると、**APM サービスマップ**が表示されます。

{{% /notice %}}

![RUMからAPMへ](../images/rum-to-apm.png)
