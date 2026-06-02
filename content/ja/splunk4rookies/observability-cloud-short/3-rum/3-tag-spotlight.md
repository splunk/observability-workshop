---
title: 3. Tag Spotlight
weight: 3
---

{{% exercise title="低速な PlaceOrder セッションをフィルター" %}}

* このダッシュボードでは、RUM データに関連付けられたすべてのタグ（RUM のインストルメンテーションによって自動生成される key-value ペア）が表示されます。タグはデータのフィルタリングや、チャートおよびテーブルの作成に使用されます。Tag Spotlight ビューを使用すると、個々のユーザーセッションを掘り下げて確認できます。

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* タイムフレームを **Last 1 hour** に変更します **(1)**。
<!--* Click **Add Filters**, select **OS Version**, click **!=** and select **Synthetics** and **RUM.LoadGen** then click the {{% button style="blue" %}}Apply Filter{{% /button %}} button **(2)**.-->
* **Operation** チャートを見つけ、リストから **PlaceOrder** を探してクリックし、**Add to filter** を選択します **(2)**。
* **User Sessions** タブをクリックします **(3)**。
* **Duration** の見出しを 2 回クリックして、セッションを duration 順（長いものが上）にソートします **(4)**。

* これで、サイトでショッピングをしているユーザーが、duration の長い順（降順）にソートされた User Session テーブルが表示されました。OS バージョンやブラウザバージョンなど、さらにフィルターを適用してデータを絞り込むこともできます。

![RUM Tag Spotlight](../images/rum-user-sessions.png)

{{% /exercise %}}
