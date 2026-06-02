---
title: 3. Tag Spotlight
weight: 3
---

{{% exercise title="低速な PlaceOrder セッションへのフィルター適用" %}}

* このダッシュボードでは、RUM データに関連付けられたすべてのタグが表示されます。これらは RUM インストルメンテーションによって自動生成されたキーと値のペアです。タグはデータのフィルタリングや、チャートおよびテーブルの作成に使用されます。Tag Spotlight ビューでは、個々のユーザーセッションへドリルダウンできます。

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* 時間範囲を **Last 1 hour** に変更します **(1)**。
<!--* Click **Add Filters**, select **OS Version**, click **!=** and select **Synthetics** and **RUM.LoadGen** then click the {{% button style="blue" %}}Apply Filter{{% /button %}} button **(2)**.-->
* **Operation** チャートを見つけ、リスト内の **PlaceOrder** をクリックして、**Add to filter** を選択します **(2)**。
* **User Sessions** タブをクリックします **(3)**。
* **Duration** の見出しを 2 回クリックして、セッションを期間順 (最長が上) に並べ替えます **(4)**。

* これで、最長の期間で降順ソートされたユーザーセッションテーブルが表示され、サイトで買い物をしていたユーザーが確認できます。OS バージョンやブラウザバージョンなど、さらにフィルターを適用してデータを絞り込むこともできます。

![RUM Tag Spotlight](../images/rum-user-sessions.png)

{{% /exercise %}}
