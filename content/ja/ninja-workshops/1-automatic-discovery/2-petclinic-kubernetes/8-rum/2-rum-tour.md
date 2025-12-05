---
title: RUM trace Waterfall view & linking to APM
linkTitle: 2. Follow RUM Traces
weight: 2
---
TAG Spotlight ビューでは、RUM データに関連付けられたすべてのタグ (tags) が表示されます。タグは、データを識別するために使用されるキーバリューペア (key-value pairs) です。この場合、タグは OpenTelemetry インストルメンテーションによって自動的に生成されます。タグは、データをフィルタリングし、チャートやテーブルを作成するために使用されます。Tag Spotlight ビューでは、動作の傾向を検出し、ユーザーセッション (user session) にドリルダウンできます。

![RUM TAG](../../images/rum-tag-spotlight.png)

User Sessions **(1)** をクリックすると、タイムウィンドウ (time window) 中に発生したユーザーセッションのリストが表示されます。

セッションの 1 つを見たいので、*Duration* **(2)** をクリックして期間でソートし、長いものの 1 つのリンク **(3)** をクリックしてください:

![User sessions](../../images/rum-user-sessions.png)
