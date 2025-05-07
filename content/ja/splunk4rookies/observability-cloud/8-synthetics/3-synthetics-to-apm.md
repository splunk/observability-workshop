---
title: 3. SyntheticsからAPMへ
weight: 3
---

今、以下のような表示が見えているはずです。

![注文する](../images/run-results-place-order.png)

{{% notice title="演習" style="green" icon="running" %}}

- ウォーターフォールで**POST checkout**で始まるエントリを見つけます。
- その前にある **>** ボタンをクリックして、メタデータセクションを展開します。収集されたメタデータを観察し、**Server-Timing**ヘッダーに注目してください。このヘッダーにより、テスト実行をバックエンドトレースに関連付けることができます。
- ウォーターフォールの**POST checkout**行にある青い{{% icon icon="link" %}} **APM**リンクをクリックします。
  {{% /notice %}}

![APMトレース](../images/apm-trace.png)

{{% notice title="演習" style="green" icon="running" %}}

- **paymentservice**に対して 1 つ以上のエラーが表示されていることを確認します（**1**）。
- 同じエラーであることを確認するには、**ログ**の関連コンテンツをクリックします（**2**）。
- 前回の演習を繰り返して、エラーのみにフィルタリングします。
- エラーログを表示して、無効なトークンによる支払い失敗を確認します。

{{% /notice %}}
