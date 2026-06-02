---
title: 3. Synthetics to APM
weight: 3
---

これで、以下のような画面が表示されているはずです。

![Place Order](../images/run-results-place-order.png)

{{% exercise title="Synthetics から APM へジャンプする" %}}

* ウォーターフォールの中から、**POST checkout** で始まるエントリを見つけます。
* その前にある **>** ボタンをクリックして、メタデータセクションを展開します。収集されているメタデータを確認し、**Server-Timing** ヘッダーに注目してください。このヘッダーによって、テスト実行をバックエンドのトレースと関連付けることができます。
* ウォーターフォールの **POST checkout** の行にある青い {{% icon icon="link" %}} **APM** リンクをクリックします。
{{% /exercise %}}

![APM trace](../images/apm-trace.png)

{{% exercise title="APM で失敗した支払いを確認する" %}}

* **paymentservice** **(1)** に 1 件以上のエラーが表示されていることを確認します。
* 同じエラーであることを確認するため、**Logs** **(2)** の関連コンテンツをクリックします。
* 先ほどの演習を繰り返し、エラーのみに絞り込みます。
* エラーログを表示し、無効なトークンが原因で支払いが失敗したことを確認します。

{{% /exercise %}}
