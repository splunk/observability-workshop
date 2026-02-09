---
title: 4. Log View Chart
weight: 4
---

ログで使用できる次のチャートタイプは **Log View** チャートタイプです。このチャートでは、事前定義されたフィルターに基づいてログメッセージを確認できます。

前の Log Timeline チャートと同様に、このチャートのバージョンを Customer Health Service Dashboard に追加します：

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* 前の演習の後、まだ **Log Observer** にいることを確認してください。
* フィルターは前の演習と同じで、タイムピッカーを **Last 15 minutes** に設定し、severity=error、`sf_service=wire-transfer-service`、`sf_environment=[WORKSHOPNAME]` でフィルタリングします。
* ヘッダーに必要なフィールドのみが表示されていることを確認してください。
* 再度 **Save** をクリックし、次に **Save to Dashboard** をクリックします。
* これにより、再びチャート作成ダイアログが表示されます。
* **Chart name** には **Log View** を使用します。
* 今回は {{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックして、前の演習で作成した Dashboard を検索します。検索ボックスにイニシャルを入力して検索を開始できます **(1)**。
  ![search dashboard](../images/search-dashboard.png)
* ダッシュボード名をクリックしてハイライトし **(2)**、{{% button style="blue" %}}OK{{% /button %}} をクリックします **(3)**。
* これにより、チャート作成ダイアログに戻ります。
* **Chart Type** として **Log View** が選択されていることを確認してください。
  ![log view](../images/log-view.png?classes=left&width=30vw)
* ダッシュボードを表示するには、{{% button style="blue" %}}Save and go to dashboard{{% /button %}} をクリックします。
* 結果は以下のダッシュボードと同様になるはずです：
  ![Custom Dashboard](../images/log-observer-custom-dashboard.png)
* この演習の最後のステップとして、ダッシュボードをワークショップチームページに追加しましょう。これにより、ワークショップの後半で簡単に見つけることができます。
* ページ上部で、ダッシュボード名の左側にある ***...*** をクリックします。
  ![linking](../images/linking.png)
* ドロップダウンから **Link to teams** を選択します。
* 次の **Link to teams** ダイアログボックスで、インストラクターから提供された Workshop チームを見つけて、{{% button style="blue" %}}Done{{% /button %}} をクリックします。

{{% /notice %}}

