---
title: Troubleshooting MetricSet を作成する
linkTitle: 4. Troubleshooting MetricSet を作成する
weight: 4
time: 5 minutes
---

## タグのインデックス作成

**Tag Spotlight** などの **Splunk Observability Cloud** の高度な機能を使用するには、まず1つ以上のタグをインデックスする必要があります。

これを行うには、**Settings** -> **MetricSets** に移動し、**APM** タブが選択されていることを確認します。次に **+ Add Custom MetricSet** ボタンをクリックします。

以下の詳細を入力して `credit.score.category` タグをインデックスしましょう（**注意**：ワークショップの参加者全員が同じ組織を使用しているため、このステップはインストラクターが代わりに行います）：

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして続行します。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** 列のチェックマークをクリックします。

## Troubleshooting MetricSet と Monitoring MetricSet の違い

このタグをインデックスするために、**Troubleshooting MetricSet** と呼ばれるものを作成したことにお気づきかもしれません。Troubleshooting MetricSet（TMS）は、**Tag Spotlight** などの機能を使用してこのタグに関する問題をトラブルシューティングできるため、このように名付けられています。

また、選択しなかった **Monitoring MetricSet**（MMS）という別のオプションがあることにもお気づきかもしれません。Monitoring MetricSetはトラブルシューティングを超えて、タグをアラートやダッシュボードに使用できます。このワークショップではこの機能については詳しく説明しませんが、ぜひご自身で探索することをお勧めする強力な機能です。
