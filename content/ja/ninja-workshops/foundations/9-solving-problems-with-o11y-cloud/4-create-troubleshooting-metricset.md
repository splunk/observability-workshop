---
title: Troubleshooting MetricSet を作成する
linkTitle: 4. Troubleshooting MetricSet を作成する
weight: 4
time: 5 minutes
---

## タグのインデックス化

**Splunk Observability Cloud** の **Tag Spotlight** などの高度な機能を使用するには、まず 1 つ以上のタグをインデックス化する必要があります。

これを行うには、**Settings** -> **APM & RUM MetricSets** に移動し、**APM** タブが選択されていることを確認します。
次に、**Add MetricSet Configuration** ドロップダウンをクリックし、**Add Custom MetricSet** を選択します。

`credit.score.category` タグをインデックス化するために、以下の詳細を入力します（**注意**：ワークショップ参加者全員が同じ組織を使用しているため、この手順はインストラクターが代わりに実施します）：

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして次に進みます。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** 列のチェックマークをクリックします。

## Troubleshooting MetricSet と Monitoring MetricSet の違い

このタグをインデックス化するために、**Troubleshooting MetricSet** と呼ばれるものを作成したことにお気づきかもしれません。Troubleshooting MetricSet（TMS）という名前が付けられているのは、**Tag Spotlight** などの機能を使用してこのタグに関する問題をトラブルシューティングできるためです。

また、選択しなかったもう 1 つのオプションとして **Monitoring MetricSet**（MMS）があることにもお気づきかもしれません。Monitoring MetricSets はトラブルシューティングを超えて、アラートやダッシュボードでタグを使用できるようにします。本ワークショップではこの機能を扱いませんが、強力な機能ですので、ぜひご自身で試してみてください。
