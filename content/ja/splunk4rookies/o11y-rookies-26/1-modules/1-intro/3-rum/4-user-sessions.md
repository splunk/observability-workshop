---
title: 4. User Sessions
weight: 4
---

RUM における **User Session** は、ユーザーが Web アプリケーションに到着してから離脱または非アクティブになるまでの、単一ユーザーによる一連のインタラクションを表します。各セッションでは、すべてのページビュー、ユーザー操作（クリック、スクロール、フォーム送信）、ネットワークリクエスト、エラー、およびパフォーマンスメトリクスのタイムラインが記録されます。

セッションは一意の Session ID で識別され、ブラウザの種類、デバイス、地理的な場所、カスタムタグなどのメタデータを含みます。これにより、特定のユーザーが体験したまさにその内容をリプレイして分析でき、問題のトラブルシューティング、ユーザー行動の理解、パフォーマンスのボトルネックの特定に非常に役立ちます。

{{% exercise title="最も長いセッションを調査する" %}}

* **User Sessions** テーブルで、**Duration** が最も長い（15 秒以上）**Session ID** をクリックします。RUM Session ビューに遷移します。
* **PlaceOrder** スパンの長さに注目してください。これは注文を完了するのにかかった時間です。良くない状態です!

![RUM Session](../images/rum-waterfall-place-order.png)

* **PlaceOrder** スパンの上または下に表示される **Fetch** **(1)** を探します。
  * 形式は `POST https://labob...y.com/cart/checkout` のようなものになります。
* 青色の **APM** **(2)** にカーソルを合わせると、数秒後にポップアップが表示されます。
* 上記のスクリーンショットのように、**paymentservice** と **checkoutservice** がエラー状態になっていることが確認できます。
* **Workflow Name** の下にある `front-end:/cart/checkout` **(3)** をクリックすると、**APM Service Map** が表示されます。ここでバックエンドのサービスとその依存関係を調査し、問題の根本原因を特定します。

![RUM Session](../images/rum-waterfall.png)

{{% /exercise %}}
