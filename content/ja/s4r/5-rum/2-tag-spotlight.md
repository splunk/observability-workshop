---
title: 2. Tag Spotlight
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

* **Custom Events** タブが選択されていることを確認してください。
* **Custom Event Latency** チャートを見てください。ここで表示されるメトリクスは、アプリケーションのレイテンシを示しています。横に表示されている比較メトリクスは、1時間前と比較したレイテンシを示しています（これは上部のフィルターバーで選択されています）。

* チャートタイトルの下にある **see all** リンクをクリックします。

{{% /notice %}}

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

このダッシュボードビューでは、RUM データに関連付けられたすべてのタグが表示されます。タグは、データを識別するために使用されるキーと値のペアです。この場合、タグは OpenTelemetry の計装によって自動的に生成されます。これらのタグはデータをフィルタリングし、チャートやテーブルを作成するために使用されます。Tag Spotlight ビューを使用することで、ユーザーセッションに関するドリルダウンができます。

{{% notice title="Exercise" style="green" icon="running" %}}

* タイムフレームを **Last 1 hour** に変更します。
* **Add Filters** をクリックし、**OS Version** を選択し、**!=** をクリックして **Synthetics** および **RUMLoadGen** を選択し、{{% button style="blue" %}}Apply Filter{{% /button %}} ボタンをクリックします。
* **Custom Event Name** チャートを見つけ、リストで **PlaceOrder** を見つけてクリックし、**Add to filter** を選択します。
* グラフ上の大きなスパイクに注意してください。
* **User Sessions** タブをクリックします。
* 表の上で **Duration** 見出しを2回クリックして、セッションを持続時間の降順でソートします。
* テーブルの上にある{{% icon icon="cog" %}}をクリックし、**Sf Geo City** を追加の列のリストから選択して、{{% button style="blue" %}}Save{{% /button %}} をクリックします。

{{% /notice %}}

これで、最長の持続時間で降順に並べられ、サイトで買い物をしているすべてのユーザーの都市を含むユーザーセッションテーブルができました。さらにデータを絞り込むために、OSバージョン、ブラウザバージョンなどを適用できます。

![RUM Tag Spotlight](../images/rum-user-sessions.png)
