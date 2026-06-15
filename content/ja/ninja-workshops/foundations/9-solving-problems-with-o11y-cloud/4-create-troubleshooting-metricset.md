---
title: Troubleshooting MetricSet の作成
linkTitle: 4. Troubleshooting MetricSet の作成
weight: 4
time: 5 minutes
---

## タグのインデックス化

**Tag Spotlight** などの **Splunk Observability Cloud** の高度な機能を使用するには、まず1つ以上のタグをインデックス化する必要があります。

これを行うには、**Settings** -> **APM & RUM MetricSets** に移動し、**APM** タブが選択されていることを確認します。  
次に、**Add MetricSet Configuration** ドロップダウンをクリックし、**Add Custom MetricSet** を選択します。

以下の詳細を入力して `credit.score.category` タグをインデックス化しましょう（**注意**: ワークショップの参加者全員が同じオーガニゼーションを使用しているため、このステップはインストラクターが代わりに実行します）

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして続行します。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** 列のチェックマークをクリックします。

## Troubleshooting MetricSet と Monitoring MetricSet の比較

このタグをインデックス化するために、**Troubleshooting MetricSet** と呼ばれるものを作成したことにお気づきかもしれません。Troubleshooting MetricSet（TMS）は、**Tag Spotlight** などの機能を使用してこのタグに関する問題をトラブルシューティングできるため、このように名付けられています。

また、今回選択しなかった **Monitoring MetricSet**（MMS）というオプションがあることにもお気づきかもしれません。Monitoring MetricSet はトラブルシューティングを超えて、タグをアラートやダッシュボードに使用できるようにします。このワークショップではこの機能を探索しませんが、ぜひご自身で試してみることをお勧めする強力な機能です。
