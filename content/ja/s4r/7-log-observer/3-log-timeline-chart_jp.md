---
title: 3. Log Timeline Chart
weight: 3
---

特定の表示が Log Observer にあると、将来的に問題を検出または解決する時間を短縮するのに役立ちます。ワークショップの一環として、これらのチャートを使用するカスタムダッシュボードの例を作成します。

まず、**Log Timeline** チャートの作成を見てみましょう。Log Timeline チャートは、時間の経過とともにログメッセージを視覚化するために使用されます。これはログメッセージの頻度を確認し、パターンを識別する素晴らしい方法です。また、環境全体でのログメッセージの分布を確認する素晴らしい方法です。これらのチャートはカスタムダッシュボードに保存できます。

{{% notice title="情報" style="green" title="演習" icon="running" %}}

まず、興味がある列のみに情報量を削減します：

* **Logs table** 上の **Configure Table** {{% icon icon="cog" %}} アイコンをクリックして **Table Settings** を開き、 `_raw` にチェックを入れず、次のフィールドが選択されていることを確認します `k8s.pod_name`, `message`, `version`。
  ![Log Table Settings](../images/log-observer-table.png)
* タイムピッカーから固定時間を削除し、 **Last 15 minutes** に設定します。
* これをすべてのトレースで機能させるために、フィルタから `trace_id` を削除し、 `sf_service=paymentservice` および `sf_environment=[WORKSHOPNAME]` フィールドを追加します。
* **Save** をクリックし、**Save to Dashboard** を選択します。
  ![save it](../images/save-query.png)
* 表示されるチャート作成ダイアログボックスで、**Chart name** に `Log Timeline` を使用します。
* {{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックし、ダッシュボード選択ダイアログボックスで {{% button style="blue" %}}New dashboard{{% /button %}} をクリックします。
* **New dashboard** ダイアログボックスで、新しいダッシュボードの名前を入力します（説明は入力する必要はありません）。次の形式を使用します： `Initials - Service Health Dashboard` と入力し、 {{% button style="blue" %}}Save{{% /button %}} をクリックします。
* 新しいダッシュボードがリストでハイライト表示されていることを確認し（**1**）、 {{% button style="blue" %}}OK{{% /button %}} をクリックします（**2**）。
  ![Save dashboard](../images/dashboard-save.png)
* **Chart Type** として **Log Timeline** が選択されていることを確認します。
  ![log timeline](../images/log-timeline.png?classes=left&width=25vw)
* {{% button %}}Save{{% /button %}} ボタンをクリックします（この時点で **Save and goto dashboard** をクリックしないでください）。

{{% /notice %}}

次に、**Log View** チャートを作成します。
