---
title: Splunk RUM と APM バックエンドサービスの相関
linkTitle: RUM と APMの相関
weight: 7
isCJKLanguage: true
---

* RUM UIでRUM Sessionの情報を続けます
* APM & Log Observer UI で相関する APM トレースとログを確認します

---

## 1. バックエンドサービスの問題を発見

![RUM-JS](../../images/RUM-JS-Error.png) をクリックして、Spanビューを閉じます。
次に下にスクロールし、 **POST /cart/checkout** の行を見つけます。

![RUM-APM-Click](../../images/RUM-APM-Click.png)

青色の ![RUM-APM-BLUE](../../images/RUM-APM.png) リンクをクリックすると、エンドユーザが行ったチェックアウト操作の一部であるバックエンドサービスに関する情報を示すダイアログがポップアップ表示されます。

![RUM-APM-Trace](../../images/RUM-Trace.png)

このポップアップでは複数のセクションが用意されており、バックエンドサービスの挙動を素早く把握することができます。例えば、Performance Summaryセクションでは、バックエンドの呼び出し中にどこに時間が費やされたかを知ることができます。

![RUM-APM-Trace-perf](../../images/RUM-Trace-Performance.png)

上記の例では77.9%以上が外部サービスに費やされていることがわかります。

ダイアログの一番下までスクロールすると、下図のような「トレースとサービス」セクションが表示されます。

![RUM-APM-Trace-services](../../images/RUM-Trace-Services.png)

**Checkout** サービスと **Payment** サービスが、両方とも濃い赤色で表示されています。薄い赤はエラーを受け取ったことを意味し、濃い赤はそのサービスから発生したエラーを意味します。


![RUM-APM-Trace-services-detail](../../images/RUM-Trace-Services-Detail.png)

つまり、すでにバックエンドのサービスに問題があることは明白なのです。

調査してみましょう！

## 2.  Backendサービスまでのトレースをたどる

Trace Idリンクをクリックすることができます。

![RUM-APM-Trace-link](../../images/RUM-Trace-url.png)

これにより、バックエンドサービスへの呼び出しで何が起こったかを詳細に示すウォーターフォールAPMビューが表示されます。
右側には、Trace IDと、前に見たように、Performance Summuryが表示されています。
ウォーターフォールでは、フロントエンドからの呼び出しの一部である様々なバックエンドサービスを特定することができます。


ご覧のように、 **Checkout** サービスと **Payment** サービスの前に赤いエラーインジケータ  ![RUM-APM-error-flag](../../images/APM_Error_Flag.png) が見えます。

![RUM-APM-waterfall](../../images/RUM-APM-Waterfall.png)

**paymentservice: grpc.hipstershop.PaymentService/Charge** の行の後にある ![RUM-APM-error-flag](../../images/APM_Error_Flag.png) をクリックしてください。

![RUM-payment-click](../../images/payment-click.png)

Spanの詳細ページが表示され、このサービスコールの詳細情報が表示されます。
**401** エラーコード、つまり *Invalid Request* が返されたことが確認できます。

## 3.  関連するログを確認

Splunk Observability Cloudは、トレースメトリクスとログを自動的に関連付けるため、ページ下部の関連コンテンツバーに、このトレースに対応するログが表示されます。

![RUM-payment-related-content](../../images/log-corelation.png)

Logのリンクをクリックすると、ログが表示されます。

ログが表示されたら、ページの上部にあるフィルターにクリック元のTrace IDがセットされ、このトレースに関連するログが表示されていることに注意してください。
次にPaymentサービスのエラーを示す行の1つを選択すると右側にログメッセージが表示されます。

ここにPaymentサービスが失敗した理由が明確に示されています。サービスに対して無効なトークンを使用しているのです。 

***Failed payment processing through ButtercupPayments: Invalid API Token (test-20e26e90-356b-432e-a2c6-956fc03f5609)**

![RUM-logs](../../images/RUM-LogObserver.png)

## 4. まとめ

このワークショップではRUMをWebサイトに追加する方法を確認しました。
RUMメトリクスを使用してWebサイトのパフォーマンスを調査しました。
Tag Profileを使用して、自分のセッションを検索し、セッションウォーターフォールを使用して、2つの問題を特定しました。

* JavaScriptのエラーにより、価格の計算が 0 になっていました。
* 支払いバックエンドサービスに問題があり支払いに失敗することがありました。

RUMのトレースとバックエンドAPMのトレースおよびログを関連付ける機能を使用して、支払い失敗の原因を発見しました。
