---
title: 3. Synthetics to APM
weight: 3
---

以下のような画面が表示されているはずです。

![Place Order](../images/run-results-place-order.png)

{{% notice title="演習" style="green" icon="running" %}}

* ウォーターフォールで **POST checkout** で始まるエントリを見つけてください。
* エントリの前にある **>** ボタンをクリックしてメタデータセクションを展開します。収集されたメタデータを確認し、**Server-Timing** ヘッダーに注目してください。このヘッダーにより、テスト実行をバックエンドトレースと関連付けることができます。
* ウォーターフォールの **POST checkout** 行にある青い {{% icon icon="link" %}} **APM** リンクをクリックしてください。
{{% /notice %}}

![APM trace](../images/apm-trace.png)

{{% notice title="演習" style="green" icon="running" %}}

* **paymentservice** **(1)** に1つ以上のエラーが表示されていることを確認してください。
* 同じエラーであることを確認するには、**Logs** **(2)** の関連コンテンツをクリックしてください。
* 先ほどの演習と同様に、エラーのみをフィルタリングしてください。
* エラーログを表示して、無効なトークンによる支払い失敗であることを確認してください。

{{% /notice %}}
