---
title: 手がかりを追う
linkTitle:  2. 原因を特定する
weight: 2
archetype: chapter
time: 7 minutes
description: 
---

{{% exercise title="RUMで調査する" %}}

注文確認エラーメッセージが表示されたユーザーセッションで、リプレイの右上にある {{% button %}}Troubleshoot in RUM{{% /button %}} をクリックします。RUMユーザーセッション詳細の長い **PlaceOrder** カスタムイベントに移動します。

![PlaceOrderとAPMリンクを含むRUMセッションウォーターフォール](../images/rum-waterfall-place-order.png)

{{< tabs >}}
{{% tab title="質問" %}}

1. Order Confirmationの問題の原因として考えられるものは何ですか？どのように判断できますか？
1. この問題をさらに調査したい場合、どうしますか？

{{% /tab %}}
{{% tab title="回答" %}}

1. バックエンドAPIへの近くのPOSTリクエストが非常に長く、500エラーを返しています。
1. このアプリはRUMとAPMの両方で計装されているため、関連するリクエスト間で関連コンテンツが表示されます。長いPOSTリクエストのAPMリンクにカーソルを合わせると、paymentサービスで根本原因の可能性がある問題がフラグ付けされていることがわかります。ここからAPMでビジネスオペレーションを開いてこの問題の影響範囲を確認したり、特定のTraceを開いてSpanの詳細や関連ログを確認したりできます。

{{% /tab %}}
{{< /tabs >}}

ウォークスルー:

1. 長いPOSTリクエストの `APM` リンクにカーソルを合わせます。しばらくすると、関連するバックエンドサービスとエラー状態のサービスがポップアップで表示されます。
1. *（オプション）* `Business Operation` リンクを新しいタブで開き、 **APM Service Map** を表示して、checkoutがダウンストリームサービス（例: **payment** サービス）にどのように接続されているかを確認します。
1. *（オプション）* **Trace ID** リンクを新しいタブで開き、この特定のTrace、そのSpan、タグの詳細、および関連ログを確認します。

![RUM内のAPMからの関連コンテンツ](../images/apm-hover.png)

{{% notice title="RUM + APM" style="primary" icon="lightbulb" %}}ブラウザからバックエンドサービスまでのトレーシングにより、誤ったサービスを追いかける時間を削減し、MTTxを短縮できます。{{% /notice %}}

{{% /exercise %}}
