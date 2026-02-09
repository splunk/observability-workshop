---
title: 3. Log Timeline Chart
weight: 3
---

Log Observer で特定のビューを作成したら、そのビューをダッシュボードで使用できると非常に便利です。これにより、将来の問題の検出や解決にかかる時間を短縮することができます。このワークショップでは、これらのチャートを使用するカスタムダッシュボードの例を作成します。

**Log Timeline** チャートの作成方法を見ていきましょう。Log Timeline チャートは、ログメッセージを時系列で可視化するために使用されます。ログメッセージの頻度を確認し、パターンを特定するのに最適な方法です。また、環境全体でのログメッセージの分布を確認するのにも最適です。これらのチャートはカスタムダッシュボードに保存できます。

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

まず、必要なカラムのみに情報を絞り込みます:

* **Logs table** の上にある Configure Table {{% icon icon="cog" %}} アイコンをクリックして **Table Settings** を開き、`_raw` のチェックを外し、`k8s.pod.name`、`message`、`version` のフィールドが選択されていることを確認します。
  ![Log Table Settings](../images/log-observer-table.png)
* タイムピッカーから固定時間を削除し、**Last 15 minutes** に設定します。
* すべてのトレースで機能するように、フィルターから `trace_id` を削除し、`sf_service=paymentservice` と `sf_environment=[WORKSHOPNAME]` のフィールドを追加します。
* **Save** をクリックし、**Save to Dashboard** を選択します。
  ![save it](../images/save-query.png)
* 表示されるチャート作成ダイアログボックスで、**Chart name** に `Log Timeline` と入力します。
* {{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックし、Dashboard Selection ダイアログボックスで {{% button style="blue" %}}New dashboard{{% /button %}} をクリックします。
* **New dashboard** ダイアログボックスで、新しいダッシュボードの名前を入力します（説明は入力不要です）。次の形式を使用してください: `Initials - Service Health Dashboard`。入力したら {{% button style="blue" %}}Save{{% /button %}} をクリックします。
* リストで新しいダッシュボードがハイライトされていることを確認し **(1)**、{{% button style="blue" %}}OK{{% /button %}} **(2)** をクリックします。
  ![Save dashboard](../images/dashboard-save.png)
* **Chart Type** として **Log Timeline** が選択されていることを確認します。
  ![log timeline](../images/log-timeline.png?classes=left&width=25vw)
* {{% button %}}Save{{% /button %}} ボタンをクリックします（この時点では **Save and goto dashboard** はクリック**しないでください**）。

{{% /notice %}}

次に、**Log View** チャートを作成します。
