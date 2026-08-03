---
title: 手がかりをたどる
linkTitle:  2. 原因の特定
weight: 2
archetype: chapter
time: 7 minutes
description: 
---

{{% exercise title="RUM で調査する" %}}

注文確認エラーメッセージが表示されたユーザーセッションで、リプレイの右上にある {{% button %}}Troubleshoot in RUM{{% /button %}} をクリックします。RUM ユーザーセッション詳細の長い **PlaceOrder** カスタムイベントに移動します。

![PlaceOrder と APM リンクを含む RUM セッションウォーターフォール](../images/rum-waterfall-place-order.png)

{{< tabs >}}
{{% tab title="質問" %}}

1. Order Confirmationの問題の原因として考えられるものは何ですか？どのように判断できますか？
1. この問題をさらに調査したい場合、どうしますか？

{{% /tab %}}
{{% tab title="回答" %}}

1. バックエンドAPIへの近くのPOSTリクエストが非常に長く、500エラーを返しています。
1. このアプリはRUMとAPMの両方で計装されているため、関連するリクエスト間で関連コンテンツが取得できます。長いPOSTリクエストのAPMリンクにカーソルを合わせると、paymentサービスに根本原因の可能性がある問題がフラグされていることがわかります。ここから、APMでPlace Orderビジネスオペレーションを開いてこの問題の影響範囲を確認したり、特定のトレースを開いてSpanの詳細や関連ログを確認したりできます。

{{% /tab %}}
{{< /tabs >}}

ウォークスルー:

1. 長いPOSTリクエストの `APM` リンクにカーソルを合わせます。しばらくすると、関連するバックエンドサービスとエラー状態のサービスがポップアップに表示されます。
1. *（オプション）* `PlaceOrder` Business Operationリンクを新しいタブで開き、**APM Service Map** を表示して、checkoutがダウンストリームサービス（例: **payment** サービス）にどのように接続されているかを確認します。
1. *（オプション）* **Trace ID** リンクを新しいタブで開き、この特定のトレース、Span、タグの詳細、および関連ログを確認します。

![RUM 内の APM からの関連コンテンツ](../images/apm-hover.png)

{{% notice title="RUM + APM" style="primary" icon="lightbulb" %}}ブラウザからバックエンドサービスまでのトレーシングにより、誤ったサービスを追跡する時間を削減し、MTTxを短縮できます。{{% /notice %}}

{{% /exercise %}}
