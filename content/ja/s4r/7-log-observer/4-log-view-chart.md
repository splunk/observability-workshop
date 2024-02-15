---
title: 4. Log View Chart
weight: 4
---

次に、ログに関するチャートタイプである **Log View** チャートタイプを見ていきます。このチャートを使用すると、事前に定義しておいたフィルタに基づいてログメッセージを表示できます。

前の Log Timeline チャートと同様に、Log View のチャートを Customer Health Service Dashboard に追加します。

{{% notice title="情報" style="green" title="Exercise" icon="running" %}}

* 前の演習完了後、**Log Observer** 画面が表示されていることを確認してください。
* フィルタ設定は前の演習と同じです。表示する時間枠を **Last 15 minutes** に設定し、`severity=error`、`sf_service=paymentservice` および `sf_environment=[WORKSHOPNAME]` でフィルタリングしているはずです。
* Log Views のヘッダーについても、前の演習で設定したフィールドのみが選択されていることを確認してください。
* 再び **Save** をクリックしてから **Save to Dashboard** をクリックします。
* これにより、改めて、チャート作成ダイアログが提供されます。
* **Chart name** に **Log View** を入力します。
* 今回は {{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックし、前回の演習で作成したダッシュボードを検索します。検索ボックスにご自身のイニシャルを入力することで見つけることができるでしょう。（**1**）。
  ![search dashboard](../images/search-dashboard.png)
* ダッシュボード名をクリックしてハイライト表示し（**2**）、 {{% button style="blue" %}}OK{{% /button %}} をクリックします（**3**）。
* これで、チャート作成ダイアログに戻ります。
* **Chart Type** として **Log View** が選択されていることを確認してください。
  ![log view](../images/log-view.png?classes=left&width=30vw)
* 次に、{{% button style="blue" %}}Save and go to dashboard{{% /button %}} をクリックしてダッシュボードを表示します。
* 結果的に、以下のようなダッシュボードが表示されるはずです。
  ![Custom Dashboard](../images/log-observer-custom-dashboard.png)
* この演習の最後のステップとして、ダッシュボードをワークショップのチームページに追加しましょう。ワークショップ中に後からダッシュボードを探すのが簡単になるはずです。
* ページの上部で、ダッシュボード名の左にある ***...*** をクリックします（**1**）。
  ![linking](../images/linking.png)
* ドロップダウンから **Link to teams** を選択します（**2**）。
* 次に表示される **Link to teams** ダイアログで、インストラクターが提供したワークショップのチームを見つけ、 {{% button style="blue" %}}Done{{% /button %}} をクリックします。

{{% /notice %}}

次のセッションでは、Splunk Synthetics を見て、Web ベースのアプリケーションのテストを自動化する方法を見ていきます。
