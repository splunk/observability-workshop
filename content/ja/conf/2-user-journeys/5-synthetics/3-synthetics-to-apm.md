---
title: 3. SyntheticsからAPM
weight: 3
---

{{% exercise title="SyntheticsからAPMへのジャンプ" %}}

* ウォーターフォールで **POST checkout** から始まるエントリを見つけます。表示されない場合は、**Run results** ページに戻り、別の失敗した実行結果を選択します。

![Place Order](../images/run-results-place-order.png)

* **>** **(1)** をクリックしてメタデータセクションを開きます。収集されたメタデータを確認し、**Response Headers** の下にある **server-timing** ヘッダーに注目します。このヘッダーにより、テスト実行をバックエンドのトレースと関連付けることができます。
* ウォーターフォールの **POST checkout** 行にある青い {{% icon icon="link" %}} **APM** **(2)** リンクをクリックします。

![APM trace](../images/apm-trace.png)

* **paymentservice** **(1)** に1つ以上のエラーが表示されていることを確認します。
* 同じエラーであることを確認するために、**Logs** **(2)** の関連コンテンツをクリックします。
* 先ほどの演習を繰り返し、エラーのみにフィルタリングします。
* エラーログを表示して、無効なトークンによる支払い失敗を確認します。

{{% /exercise %}}
