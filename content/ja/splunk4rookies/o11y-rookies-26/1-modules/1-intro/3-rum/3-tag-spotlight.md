---
title: 3. Tag Spotlight
weight: 3
---

{{% exercise title="PlaceOrderの遅いセッションをフィルタリングする" %}}

* このダッシュボードには、RUMデータに関連するすべてのタグが表示されます。タグはRUM計装によって自動生成されるキーと値のペアです。タグはデータのフィルタリングやチャート、テーブルの作成に使用されます。Tag Spotlightビューでは、個々のユーザーセッションにドリルダウンできます。

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

* 時間範囲を **Last 1 hour** に変更します **(1)**。

* **Custom Workflow Name** チャートを見つけ、リスト内の **PlaceOrder** を探します **(2)**。それをクリックし、ポップアップウィンドウで **Add to filter** を選択して **(3)** ページにフィルタを適用します。
* **User Sessions** タブをクリックします **(4)**。
* **Duration** の見出しを2回クリックして、セッションを期間順（最長が上）にソートします **(5)**。

* これで、最長期間（降順）でソートされたUser Sessionsテーブルが表示され、サイトで買い物をしているユーザーが確認できます。OSバージョン、ブラウザバージョンなどのフィルタを追加して、データをさらに絞り込むこともできます。

![RUM Tag Spotlight](../images/rum-user-sessions.png)

{{% /exercise %}}
