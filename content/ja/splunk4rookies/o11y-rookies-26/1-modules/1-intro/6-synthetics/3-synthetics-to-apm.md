---
title: 3. Synthetics から APM へ
weight: 3
---

{{% exercise title="Synthetics から APM へジャンプ" %}}

* ウォーターフォールで **POST checkout** で始まるエントリを探します。表示されない場合は、**Run results** ページに戻って、別の失敗した実行結果を選択してください。

![Place Order](../images/run-results-place-order.png)

* **>** **(1)** をクリックしてメタデータセクションを開きます。収集されているメタデータを確認し、**Response Headers** の下にある **server-timing** ヘッダーに注目してください。このヘッダーによって、テスト実行をバックエンドのトレースと関連付けることができます。
* ウォーターフォールの **POST checkout** 行にある青色の {{% icon icon="link" %}} **APM** **(2)** リンクをクリックします。

![APM trace](../images/apm-trace.png)

* **paymentservice** **(1)** に1つ以上のエラーが表示されていることを確認します。
* 同じエラーであることを確認するために、**Logs** **(2)** の関連コンテンツをクリックします。
* 先ほどの演習を繰り返して、エラーのみに絞り込みます。
* エラーログを表示して、無効なトークンによる支払い失敗を確認します。

{{% /exercise %}}
