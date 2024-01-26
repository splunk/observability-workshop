---
title: 3. Synthetics to APM
weight: 3
---

これで、以下の画像のようなビューが得られるはずです。

![Place Order](../images/run-results-place-order.png)

{{% notice title="実習" style="green" icon="running" %}}

* ウォーターフォールで **POST checkout** で始まるエントリを見つけます。
* その前にある **>** ボタンをクリックして、メタデータセクションを展開します。収集されているメタデータを観察し、**Server-Timing** ヘッダーをメモします。このヘッダーにより、テストランをバックエンドのトレースに関連付けることができます。
* ウォーターフォールの **POST checkout** 行の前にある青い {{% icon icon="link" %}} **APM** リンクをクリックします。
{{% /notice %}}

![APM trace](../images/apm-trace.png)

{{% notice title="実習" style="green" icon="running" %}}

* **paymentservice** に1つ以上のエラーが表示されることを確認してください（**1**）。
* 同じエラーであることを確認するには、**Logs**の関連コンテンツをクリックします（**2**）。
* 以前の演習と同様に、エラーのみに絞り込むための手順を繰り返します。
* エラーログを表示して、無効なトークンによる支払いの失敗を確認します。

{{% /notice %}}
