---
title: 1. Log Filtering
weight: 1
---

**Log Observer (LO)** は、さまざまな方法で利用できます。クイックツアーでは、LO の **no-code interface** を使ってログ内の特定のエントリを検索しました。一方このセクションでは、APM のトレースから **Related Content** リンクを使って LO に移動した状態を想定しています。

この方法の利点は、RUM と APM の連携の場合と同様に、これまでの操作のコンテキストの中でログを参照できる点にあります。今回のコンテキストは、トレースと一致する時間枠 **(1)** と、**trace_id** に設定されたフィルター **(2)** です。

![Trace Logs](../images/log-observer-trace-logs.png)

このビューには、エンドユーザーが Online Boutique を操作したことで開始されたバックエンドトランザクションに関与した、**すべての** アプリケーションやサービスから出力された **すべての** ログ行が含まれます。

Online Boutique のような小規模なアプリケーションであっても、表示されるログの量は非常に多くなり、調査対象となっている実際のインシデントに関係する特定のログ行を見つけるのが難しくなることがあります。

{{% exercise title="Filter to error logs" %}}

ログのうち、エラーメッセージのみに絞り込む必要があります。

* **Group By** のドロップダウンボックスをクリックし、フィルターを使って **Severity** を見つけます。
* 選択したら {{% button style="blue" %}}Apply{{% /button %}} ボタンをクリックします（チャートの凡例が debug、error、info を表示するように変わることに注目してください）。
  ![legend](../images/severity-logs.png)
* エラーログのみを選択するには、凡例の error という文字 **(1)** をクリックし、**Add to filter** を選択します。その後 {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。
* 複数のサービスにエラー行がある場合は、フィルターにサービス名 `sf_service=paymentservice` を追加することもできますが、今回のケースでは必要ありません。
  ![Error Logs](../images/log-observer-errors.png)

{{% /exercise %}}

次に、ログエントリの詳細を確認していきます。
