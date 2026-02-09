---
title: 1. ログフィルタリング
weight: 1
---

**Log Observer (LO)** は、さまざまな方法で使用できます。クイックツアーでは、LO の**ノーコードインターフェース**を使用してログ内の特定のエントリを検索しました。しかし、このセクションでは、**Related Content** リンクを使用して APM のトレースから LO に到達したことを前提としています。

この方法の利点は、RUM と APM 間のリンクと同様に、以前のアクションのコンテキスト内でログを確認できることです。この場合、コンテキストはトレースと一致する時間範囲 **(1)** と、**trace_id** に設定されたフィルター **(2)** です。

![Trace Logs](../images/log-observer-trace-logs.png)

このビューには、エンドユーザーが Online Boutique を操作することで開始されたバックエンドトランザクションに参加した**すべて**のアプリケーションまたはサービスからの**すべて**のログ行が含まれます。

Online Boutique のような小規模なアプリケーションでも、検出されるログの量が膨大になり、調査中のインシデントに関連する特定のログ行を見つけることが難しくなる場合があります。

{{% notice title="Exercise" style="green" icon="running" %}}

ログ内のエラーメッセージのみに焦点を当てる必要があります：

* **Group By** ドロップダウンボックスをクリックし、フィルターを使用して **Severity** を見つけます。
* 選択したら、{{% button style="blue" %}}Apply{{% /button %}} ボタンをクリックします（チャートの凡例が debug、error、info を表示するように変わることに注目してください）。
  ![legend](../images/severity-logs.png)
* エラーログのみを選択するには、凡例内の error **(1)** という単語をクリックし、続いて **Add to filter** を選択します。次に {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。
* 複数のサービスにエラー行がある場合は、サービス名 `sf_service=paymentservice` をフィルターに追加することもできますが、今回の場合は必要ありません。
  ![Error Logs](../images/log-observer-errors.png)

{{% /notice %}}

次に、ログエントリの詳細を確認します。
