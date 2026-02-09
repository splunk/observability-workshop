---
title: 4. Log View チャート
weight: 4
---

ログで使用できる次のチャートタイプは **Log View** チャートタイプです。このチャートを使用すると、事前定義されたフィルターに基づいてログメッセージを確認できます。

前回の Log Timeline チャートと同様に、このチャートのバージョンを Customer Health Service Dashboard に追加します：

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* 前の演習の後、まだ **Log Observer** にいることを確認してください。
* フィルターは前の演習と同じで、タイムピッカーは **Last 15 minutes** に設定し、severity=error、`sf_service=paymentservice`、`sf_environment=[WORKSHOPNAME]` でフィルタリングします。
* ヘッダーに必要なフィールドのみが表示されていることを確認してください。
* 再度 **Save** をクリックし、次に **Save to Dashboard** をクリックします。
* これにより、チャート作成ダイアログが再び表示されます。
* **Chart name** には **Log View** を使用します。
* 今回は {{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックし、前の演習で作成したダッシュボードを検索します。検索ボックスにイニシャルを入力することから始められます **(1)**。
  ![search dashboard](../images/search-dashboard.png)
* ダッシュボード名をクリックしてハイライト表示し **(2)**、{{% button style="blue" %}}OK{{% /button %}} をクリックします **(3)**。
* これにより、チャート作成ダイアログに戻ります。
* **Chart Type** として **Log View** が選択されていることを確認してください。
  ![log view](../images/log-view.png?classes=left&width=30vw)
* ダッシュボードを表示するには、{{% button style="blue" %}}Save and go to dashboard{{% /button %}} をクリックします。
* 結果は以下のダッシュボードと同様になるはずです：
  ![Custom Dashboard](../images/log-observer-custom-dashboard.png)
* この演習の最後のステップとして、ダッシュボードをワークショップチームページに追加しましょう。これにより、ワークショップの後半で簡単に見つけることができます。
* ページ上部の右上にある縦の3点メニュー **⋮** をクリックし、**Dashboard Group Actions** > **Link to teams** を選択します。
  ![linking](../images/linking.png)
* 次の **Link to teams** ダイアログボックスで、インストラクターから提供されたワークショップチームを見つけて、{{% button style="blue" %}}Done{{% /button %}} をクリックします。

{{% /notice %}}

次のセッションでは、Splunk Synthetics を見て、Webベースのアプリケーションのテストを自動化する方法を確認します。
