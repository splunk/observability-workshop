---
title: 3. Log Timeline Chart
weight: 3
---

Log Observer である決まったビューを持っておくと、あるダッシュボードの中でそのビューを活用し、将来的に問題の検出と解決にかかる時間を削減することに寄与するでしょう。ワークショップの一環として、これらのチャートを使用するカスタムダッシュボードの例を作成します。

まず、**Log Timeline** チャートの作成を見てみましょう。Log Timeline チャートは、時間の経過とともにログメッセージを表示するために使用されます。これはログメッセージの頻度を確認し、パターンを識別するのに適した表現方法です。また、環境全体でのログメッセージの出力傾向を確認するのにも適しています。これらのチャートはカスタムダッシュボードに保存できます。

{{% notice title="情報" style="green" title="Exercise" icon="running" %}}

まず、表示するログの列を必要なものに絞り込みます。

* **Logs table** 上の **Configure Table** {{% icon icon="cog" %}} アイコンをクリックして **Table Settings** を開きます。 `_raw` のチェックを外し、`k8s.pod_name`, `message`, `version` のフィールドが選択されていることを確認します。
  ![Log Table Settings](../images/log-observer-table.png)
* 時間枠として固定の時間が入っている設定を外し、 **Last 15 minutes** を設定します。
* すべてのトレースに対してログ参照ができるように、フィルタ設定から `trace_id` を削除し、 `sf_service=paymentservice` および `sf_environment=[WORKSHOPNAME]` フィールドを追加します。
* **Save** をクリックし、**Save to Dashboard** を選択します。
  ![save it](../images/save-query.png)
* チャート作成に関するダイアログが表示されます。**Chart name** に `Log Timeline` を入力します。
* 次に、{{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックします。ダッシュボード選択のダイアログでは {{% button style="blue" %}}New dashboard{{% /button %}} をクリックします。
* **New dashboard** ダイアログで、新しいダッシュボードの名前を入力します（Description 欄は入力不要です）。名前には以下を使用します： `<受講者の方のイニシャル> - Service Health Dashboard` と入力し、 {{% button style="blue" %}}Save{{% /button %}} をクリックします。
* 新しいダッシュボードがリストでハイライト表示されていることを確認し（**1**）、 {{% button style="blue" %}}OK{{% /button %}} をクリックします（**2**）。
  ![Save dashboard](../images/dashboard-save.png)
* **Chart Type** として **Log Timeline** が選択されていることを確認します。
  ![log timeline](../images/log-timeline.png?classes=left&width=25vw)
* 最後に {{% button %}}Save{{% /button %}} ボタンをクリックします（この時点で **Save and goto dashboard** をクリックしないでください）。

{{% /notice %}}

次に、**Log View** チャートを作成します。
