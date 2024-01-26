---
title: 4. Log View Chart
weight: 4
---

次に、ログと共に使用できる次のチャートタイプは **Log View** チャートタイプです。このチャートを使用すると、事前定義されたフィルタに基づいてログメッセージを表示できます。

前の Log Timeline チャートと同様に、このチャートのバージョンを Customer Health Service Dashboard に追加します：

{{% notice title="情報" style="green" title="演習" icon="running" %}}

* 前の演習後にまだ **Log Observer** にいることを確認してください。
* フィルタは前の演習と同じである必要があり、タイムピッカーが **Last 15 minutes** に設定され、 severity=error、`sf_service=paymentservice` および `sf_environment=[WORKSHOPNAME]` でフィルタリングされています。
* ウォンテッドなフィールドのみがあるヘッダーを確認してください。
* 再び **Save** をクリックしてから **Save to Dashboard** をクリックします。
* これにより、チャート作成ダイアログが提供されます。
* **Chart name** に **Log View** を使用します。
* 今回は {{% button style="blue" %}}Select Dashboard{{% /button %}} をクリックし、前回の演習で作成したダッシュボードを検索します。検索ボックスにイニシャルを入力して始めることができます（**1**）。
  ![search dashboard](../images/search-dashboard.png)
* ダッシュボード名をクリックしてハイライト表示し（**2**）、 {{% button style="blue" %}}OK{{% /button %}} をクリックします（**3**）。
* これで、チャート作成ダイアログに戻ります。
* **Chart Type** として **Log View** が選択されていることを確認してください。
  ![log view](../images/log-view.png?classes=left&width=30vw)
* ダッシュボードを見るには {{% button style="blue" %}}Save and go to dashboard{{% /button %}} をクリックします。
* 結果は以下のダッシュボードと似ているはずです：
  ![Custom Dashboard](../images/log-observer-custom-dashboard.png)
* この演習の最後のステップとして、ダッシュボードをワークショップのチームページに追加しましょう。これにより、ワークショップ中に後で簡単に見つけることができます。
* ページの上部で、ダッシュボード名の左にある ***...*** をクリックします（**1**）。
  ![linking](../images/linking.png)
* ドロップダウンから **Link to teams** を選択します（**2**）。
* 次に表示される **Link to teams** ダイアログボックスで、インストラクターが提供したワークショップのチームを見つけ、 {{% button style="blue" %}}Done{{% /button %}} をクリックします。

{{% /notice %}}

次のセッションでは、Splunk Synthetics を見て、ウェブベースのアプリケーションのテストを自動化する方法を確認します。
