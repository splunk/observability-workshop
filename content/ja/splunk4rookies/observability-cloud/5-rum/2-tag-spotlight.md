---
title: 2. Tag Spotlight
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

- **Custom Events**タブを選択して、そのタブにいることを確認します。
- **Custom Event Latency**チャートを見てください。ここに表示されているメトリクスはアプリケーションのレイテンシーを示しています。横の比較メトリクスは、1時間前（上部のフィルターバーで選択されています）と比較したレイテンシーを示しています。

- チャートタイトルの下にある**すべて表示**リンクをクリックします。

{{% /notice %}}

![RUM Tag Spotlight](../images/rum-tag-spotlight.png)

このダッシュボードビューでは、RUMデータに関連付けられたすべてのタグが表示されます。タグはデータを識別するために使用されるキーと値のペアです。この場合、タグはOpenTelemetry計装によって自動的に生成されます。タグはデータをフィルタリングし、チャートやテーブルを作成するために使用されます。Tag Spotlightビューでは、ユーザーセッションを詳しく調べることができます。

{{% notice title="演習" style="green" icon="running" %}}

- 時間枠を**過去 1 時間**に変更します。
- **Add filters**をクリックし、**OS Version**を選択し、**!=**をクリックして**Synthetics**と**RUMLoadGen**を選択し、{{% button style="blue" %}}フィルターを適用{{% /button %}}ボタンをクリックします。
- **Custom Events Name**チャートを見つけ、リスト内の**PlaceOrder**を見つけてクリックし、**Add to filter**を選択します。
- 上部のグラフに大きなスパイクがあることに注目してください。
- **User Session**タブをクリックします。
- **Duration**の見出しを2回クリックして、セッションを期間で並べ替えます（最も長いものが上部に表示されます）。
- テーブルの上にある{{% icon icon="cog" %}}をクリックし、追加の列のリストから**Sf Geo City**を選択し、{{% button style="blue" %}}保存{{% /button %}}をクリックします。

{{% /notice %}}

これで、最も長い期間の降順でソートされたユーザーセッションテーブルができました。このテーブルには、サイトでショッピングしたすべてのユーザーの都市も含まれています。OSバージョン、ブラウザバージョンなど、さらにフィルターを適用してデータを絞り込むこともできます。

![RUMTag Spotlight](../images/rum-user-sessions.png)
