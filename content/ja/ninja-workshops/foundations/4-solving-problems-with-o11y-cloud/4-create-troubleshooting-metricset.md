---
title: Troubleshooting MetricSet を作成する
linkTitle: 4. Create a Troubleshooting MetricSet
weight: 4
time: 5 minutes
---

## タグのインデックス化

**Splunk Observability Cloud** で **Tag Spotlight** などの高度な機能を使用するには、まず1つ以上のタグをインデックス化する必要があります。

そのためには、**Settings** -> **APM & RUM MetricSets** に移動し、**APM** タブが選択されていることを確認します。
次に、**Add MetricSet Configuration** ドロップダウンをクリックし、**Add Custom MetricSet** を選択します。

次の詳細を入力して `credit.score.category` タグをインデックス化します（**注意**: ワークショップに参加する全員が同じ組織を使用しているため、このステップはインストラクターが代行します）。

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして次に進みます。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** カラムのチェックマークをクリックします。

## Troubleshooting MetricSet と Monitoring MetricSet の違い

このタグをインデックス化するために、**Troubleshooting MetricSet** と呼ばれるものを作成したことに気付いたかもしれません。Troubleshooting MetricSet（TMS）は、**Tag Spotlight** などの機能を使用してこのタグに関する問題のトラブルシューティングを行えるため、このように名付けられています。

選択しなかったもう1つのオプションとして、**Monitoring MetricSet**（MMS）と呼ばれるものがあることにも気付いたかもしれません。Monitoring MetricSet はトラブルシューティングを超えた機能を提供し、タグをアラートやダッシュボードに利用できるようにします。このワークショップでは扱いませんが、強力な機能ですので、ぜひ各自で試してみてください。
