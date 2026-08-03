---
title: Tag Spotlight
linkTitle: 4. Tag Spotlight
weight: 4
---

{{% exercise title="遅い PlaceOrder セッションをフィルタリングする" %}}

* このダッシュボードには、RUMデータに関連付けられたすべてのタグが表示されます。タグはRUM計装によって自動生成されるキーと値のペアです。タグはデータのフィルタリングやチャートおよびテーブルの作成に使用されます。Tag Spotlightビューでは、個々のユーザーセッションにドリルダウンできます。

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* 時間枠を **Last 1 hour** に変更します **(1)**。
<!--* Click **Add Filters**, select **OS Version**, click **!=** and select **Synthetics** and **RUM.LoadGen** then click the {{% button style="blue" %}}Apply Filter{{% /button %}} button **(2)**.-->
* **Operation** チャートを見つけ、リスト内の **PlaceOrder** を探してクリックし、 **Add to filter** を選択します **(2)**。
* **User Sessions** タブをクリックします **(3)**。
* **Duration** 見出しを2回クリックして、セッションを期間の長い順（最長が上）にソートします **(4)**。

* これで、最長期間（降順）でソートされたユーザーセッションテーブルが表示され、サイトで買い物をしていたユーザーが確認できます。OSバージョンやブラウザバージョンなど、さらにフィルターを適用してデータを絞り込むこともできます。

![RUM Tag Spotlight with user sessions](../images/rum-user-sessions.png)

{{% /exercise %}}
