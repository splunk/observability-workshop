---
title: 4. ユーザーセッション
weight: 4
---

RUMにおける **User Session** は、Webアプリケーションに対する単一ユーザーの完全なインタラクションを表します。ユーザーが到着した瞬間から離脱するか非アクティブになるまでが対象です。各セッションには、すべてのページビュー、ユーザーインタラクション（クリック、スクロール、フォーム送信）、ネットワークリクエスト、エラー、パフォーマンスメトリクスのタイムラインが記録されます。

セッションは一意のSession IDで識別され、ブラウザの種類、デバイス、地理的位置、カスタムタグなどのメタデータが含まれます。これにより、特定のユーザーが体験した内容を再生・分析でき、問題のトラブルシューティング、ユーザー行動の理解、パフォーマンスボトルネックの特定に非常に役立ちます。

{{% exercise title="最長セッションの調査" %}}

* **User Sessions** テーブルで、最も長い **Duration**（8秒以上）の **Session ID** をクリックします。RUM Sessionビューに移動します。
* **PlaceOrder** Spanの長さに注目してください。これは注文完了にかかった時間です。良くないですね！

![RUM Session](../images/rum-waterfall-place-order.png)

* **PlaceOrder** Spanの上または下にある **Fetch** **(1)** を探します。
  * `POST https://labob...y.com/cart/checkout` のような表示になっています。
* 青い **APM** **(2)** にカーソルを合わせると、数秒後にポップアップが表示されます。
* 上のスクリーンショットのように、**paymentservice** と **checkoutservice** がエラー状態であることが確認できます。
* **Workflow Name** の下にある `front-end:/cart/checkout` **(3)** をクリックすると、**APM Service Map** が表示されます。ここでバックエンドサービスとその依存関係を調査し、問題の根本原因を特定します。

![RUM Session](../images/rum-waterfall.png)

{{% /exercise %}}
