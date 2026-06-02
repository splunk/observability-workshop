---
title: 4. User Sessions
weight: 4
---

RUM における **User Session** とは、ユーザーが Web アプリケーションに到着してから離脱、または非アクティブになるまでの一連の操作全体を表します。各セッションでは、すべてのページビュー、ユーザー操作（クリック、スクロール、フォーム送信）、ネットワークリクエスト、エラー、パフォーマンスメトリクスのタイムラインがキャプチャされます。

セッションは一意の Session ID で識別され、ブラウザの種類、デバイス、地理的位置、カスタムタグといったメタデータが付与されます。これにより、特定のユーザーが体験した内容をそのままリプレイして分析できるため、問題のトラブルシューティング、ユーザー行動の理解、パフォーマンスボトルネックの特定に非常に役立ちます。

{{% exercise title="Investigate the longest session" %}}

* **User Sessions** テーブルで、**Duration** が最も長い（15 秒以上の）**Session ID** をクリックします。RUM Session ビューが開きます。
* スパン **PlaceOrder** の長さに注目してください。これは注文完了までにかかった時間です。良くない状態です！

![RUM Session](../images/rum-waterfall-place-order.png)

* **PlaceOrder** スパンの上または下にある **Fetch** **(1)** を探します。
  * `POST https://labob...y.com/cart/checkout` のような表示になっています。
* 青い **APM** **(2)** にカーソルを合わせると、数秒後にポップアップが表示されます。
* 上のスクリーンショットのように、**paymentservice** と **checkoutservice** がエラー状態になっていることが確認できます。
* **Workflow Name** の下にある `front-end:/cart/checkout` **(3)** をクリックすると、**APM Service Map** が表示されます。ここでバックエンドサービスとその依存関係を調査し、問題の根本原因を特定します。

![RUM Session](../images/rum-waterfall.png)

{{% /exercise %}}
