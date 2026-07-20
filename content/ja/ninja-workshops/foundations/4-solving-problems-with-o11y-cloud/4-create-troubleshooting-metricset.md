---
title: Troubleshooting MetricSetの作成
linkTitle: 4. Troubleshooting MetricSetの作成
weight: 4
time: 5 minutes
---

## タグのインデックス化

**Tag Spotlight** などの **Splunk Observability Cloud** の高度な機能を使用するには、まず1つ以上のタグをインデックス化する必要があります。

**Settings** -> **APM & RUM MetricSets** に移動し、**APM** タブが選択されていることを確認します。
次に **Add MetricSet Configuration** ドロップダウンをクリックし、**Add Custom MetricSet** を選択します。

以下の詳細を入力して `credit.score.category` タグをインデックス化します（**注意**: ワークショップの参加者全員が同じ組織を使用しているため、このステップはインストラクターが代わりに行います）

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして続行します。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** 列のチェックマークをクリックします。

## Troubleshooting MetricSetとMonitoring MetricSet

このタグをインデックス化するために、**Troubleshooting MetricSet** と呼ばれるものを作成したことにお気づきかもしれません。Troubleshooting MetricSet（TMS）は、**Tag Spotlight** などの機能を使用してこのタグに関する問題をトラブルシューティングできるため、このように名付けられています。

また、今回選択しなかった **Monitoring MetricSet**（MMS）という別のオプションがあることにもお気づきかもしれません。Monitoring MetricSetはトラブルシューティングを超えて、タグをアラートやダッシュボードに使用できるようにします。このワークショップではこの機能を扱いませんが、ぜひご自身で試してみてください。
