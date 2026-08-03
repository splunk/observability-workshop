---
title: ユーザーセッション
linkTitle: 1. ユーザーセッション
weight: 1
time: 5 minutes
---

Splunk RUMでは、**セッション** はアプリ上でのユーザーアクティビティの連続した期間です（最大4時間、非アクティブ状態またはアプリが閉じられると終了します）。RUMセッションはファネルや機能採用の時系列などの分析に活用されます。

**Session details** では、メタデータ、リプレイイベント、およびSpanのウォーターフォール（ロード、リクエスト、カスタムイベント、Web Vitals、エラー）が表示されます。詳細は[Key concepts in Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/key-concepts-in-splunk-rum)を参照してください。

{{% exercise title="開いているユーザーセッションを探索する" %}}

すでに開いているユーザーセッションを使用するか、新しいセッションを開きます。

* **Session details** で、サマリーを確認します: **Session ID**、開始時間、**duration**、クライアント/OS。

* **Session Events** で、いくつかのイベントをクリックし、イベントリストとリプレイが同期していることを確認します。
* ユーザーが **Place order** を行ったイベント（または最も長いページ）を選択します。Spanリストで以下の例を見つけます:
  * **document load** または **page** Span
  * **fetch/XHR**（ネットワークリクエスト）Span
  * **custom event** Span（**PlaceOrder** など）
  * **error** または遅いSpan

* 1つのSpanをクリックし、**Parsed** と **Raw** を切り替えます:
  * **Parsed** — 素早く確認するためのキュレーションされたタグと値。
  * **Raw** — そのSpanの完全な詳細。

![RUM user session details](../images/rum-waterfall-place-order.png)

{{< tabs >}}
{{% tab title="質問" %}}

ファネルや集計チャートだけでは確認できない、セッション詳細から学べることは何ですか？

{{% /tab %}}
{{% tab title="回答" %}}

**1つのユーザーセッション** の正確なシーケンスとタイミング: どのページとイベントが実行されたか、どのリクエストやカスタムイベントが遅かったか失敗したか、どのSpanがバックエンドのTraceに紐づいているか。さらに、より深い分析や他のチームとの共有のために、Span上のすべてのフィールドとタグを確認できます。

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

RUMセッションがどのようにロールアップされ、アプリケーションの健全性とユーザーエクスペリエンスの理解に役立つかを見ていきましょう。
