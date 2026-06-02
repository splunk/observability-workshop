---
title: 3. Synthetics から APM へ
weight: 3
---

{{% exercise title="Synthetics から APM へジャンプする" %}}

* ウォーターフォール内で **POST checkout** で始まるエントリを見つけます。表示されていない場合は、**Run results** ページに戻り、別の失敗した実行結果を選択してください。

![Place Order](../images/run-results-place-order.png)

* **>** **(1)** をクリックしてメタデータセクションを開きます。収集されているメタデータを確認し、**Response Headers** の下にある **server-timing** ヘッダーに注目してください。このヘッダーによって、テスト実行をバックエンドのトレースに関連付けることができます。
* ウォーターフォールの **POST checkout** 行にある青色の {{% icon icon="link" %}} **APM** **(2)** リンクをクリックします。

![APM trace](../images/apm-trace.png)

* **paymentservice** **(1)** に対して 1 つ以上のエラーが表示されていることを確認します。
* 同じエラーであることを確認するために、**Logs** **(2)** の関連コンテンツをクリックします。
* 先ほどのエクササイズを繰り返して、エラーのみにフィルタリングします。
* エラーログを表示して、無効なトークンによって支払いが失敗したことを確認します。

{{% /exercise %}}
