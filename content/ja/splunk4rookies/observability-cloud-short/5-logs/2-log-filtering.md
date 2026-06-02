---
title: 2. Log Filtering
weight: 2
---

{{% exercise title="エラーログにフィルタリング" %}}

* ログ内のエラーメッセージのみに焦点を当てる必要があります。
* **Group By** **(1)** ドロップダウンボックスをクリックし、フィルターを使って **severity** を見つけます。
* 選択したら {{% button style="blue" %}}Apply{{% /button %}} ボタンをクリックします（チャートの凡例が debug、error、info を表示するように変化することに注目してください）。

![legend](../images/severity-logs.png)

* エラーログのみを選択するには、凡例の error **(2)** という文字をクリックし、続いて **Add to filter** を選択します。その後、ページ上部の {{% button style="blue" %}}Run Search{{% /button %}} をクリックします。

![Error Logs](../images/log-observer-errors.png)

{{% /exercise %}}

次に、ログエントリの詳細を見ていきます。
