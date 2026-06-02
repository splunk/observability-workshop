---
title: 2. Tag Spotlight
weight: 2
---

{{% exercise title="Custom Event レイテンシチャートを開く" %}}

* **Custom Workflows** タブを選択し、表示されていることを確認してください。
* **Custom Workflow Duration** チャートを確認してください。ここに表示されているメトリクスはアプリケーションのレイテンシを示しています。横に表示されている比較メトリクスは、1時間前（上部のフィルタバーで選択されている時間）と比較したレイテンシを示しています。

* チャートタイトルの下にある **see all** リンクをクリックしてください。

{{% /exercise %}}

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

このダッシュボードビューには、RUM データに関連付けられたすべてのタグが表示されます。タグはデータを識別するために使用されるキーと値のペアです。今回の場合、タグは OpenTelemetry の計装によって自動的に生成されます。タグはデータをフィルタリングし、チャートやテーブルを作成するために使用されます。Tag Spotlight ビューを使うと、ユーザーセッションをドリルダウンできます。

{{% exercise title="遅い PlaceOrder トランザクションへのフィルタリング" %}}

* 時間範囲を **Last 1 hour** に変更してください。
* **Add Filters** をクリックし、**OS Version** を選択して **!=** をクリックし、**Synthetics** と **RUMLoadGen** を選択してから、{{% button style="blue" %}}Apply Filter{{% /button %}} ボタンをクリックしてください。
* **Custom Event Name** チャートを見つけ、リストから **PlaceOrder** を見つけてクリックし、**Add to filter** を選択してください。
* 上部のグラフに大きなスパイクが現れていることに注目してください。
* **User Sessions** タブをクリックしてください。
* **Duration** の見出しを2回クリックして、セッションを継続時間順（長いものが上）に並べ替えてください。
* テーブルの上にある {{% icon icon="cog" %}} をクリックし、追加列のリストから **Sf Geo City** を選択して {{% button style="blue" %}}Save{{% /button %}} をクリックしてください。

{{% /exercise %}}

これで、継続時間の長い順に並べ替えられ、サイトで買い物をしているすべてのユーザーの都市を含むユーザーセッションテーブルが表示されました。OS のバージョンやブラウザのバージョンなど、さらにフィルターを適用してデータを絞り込むこともできます。

![RUM Tag Spotlight](../images/rum-user-sessions.png)
