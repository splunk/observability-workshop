---
title: 3. Tag Spotlight
weight: 3
---

{{% exercise title="遅いPlaceOrderセッションのフィルタリング" %}}

* このダッシュボードには、RUMデータに関連するすべてのタグが表示されます。タグはRUM計装によって自動生成されるキーと値のペアです。タグはデータのフィルタリングやチャート、テーブルの作成に使用されます。Tag Spotlightビューでは、個々のユーザーセッションにドリルダウンできます。

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* 時間枠を **Last 1 hour** **(1)** に変更します。

* **Custom Workflow Name** チャートを見つけ、リスト内の **PlaceOrder** **(2)** を探してクリックし、 **Add to filter** **(2)** を選択します。
* **User Sessions** タブ **(3)** をクリックします。
* **Duration** 見出しを2回クリックして、セッションを期間の長い順（降順）に並べ替えます **(4)**。

* これで、期間の長い順（降順）に並べ替えられたUser Sessionsテーブルが表示され、サイトで買い物をしていたユーザーが確認できます。OSバージョン、ブラウザバージョンなどのフィルターを追加して、データをさらに絞り込むこともできます。

![RUM Tag Spotlight](../images/rum-user-sessions.png)

{{% /exercise %}}
