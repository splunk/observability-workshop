---
title: 3. Synthetics to APM
weight: 3
---

さきほどの演習を通じて、以下のような画面が表示されているはずです。

![Place Order](../images/run-results-place-order.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* ウォーターフォールの中から **POST checkout** で始まるエントリを見つけます。
* その前にある **>** ボタンをクリックして、メタデータセクションを展開します。収集されているメタデータを観察してみてください。また、**Server-Timing** ヘッダーに着目してみましょう。このヘッダーにより、テスト実行の情報とバックエンドのトレースを関連付けることができます。
* ウォーターフォールの中の **POST checkout** 行の前にある青い {{% icon icon="link" %}} **APM** リンクをクリックします。
{{% /notice %}}

![APM trace](../images/apm-trace.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice** に1つ以上のエラーが表示されることを確認してください（**1**）。
* 同じエラーであることを確認するには、**Logs** の Related Contents をクリックします（**2**）。
* 以前の演習と同様に、エラーのみに絞り込むための手順を繰り返します。
* エラーログを表示して、無効なトークンによって支払い処理が失敗したことを検証しましょう。

{{% /notice %}}
