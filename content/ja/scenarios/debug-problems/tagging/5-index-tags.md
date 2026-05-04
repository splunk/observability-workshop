---
title: タグのインデックス化
linkTitle: 5. タグのインデックス化
weight: 5
time: 5 minutes
---

## タグのインデックス化

**Tag Spotlight** などの **Splunk Observability Cloud** の高度な機能を使用するには、まず1つ以上のタグをインデックス化する必要があります。

これを行うには、**Settings** -> **APM & RUM MetricSets** に移動します。**APM** タブが選択されていることを確認してください（**RUM** ではありません）。**Add MetricSet Configuration** ボタンをクリックし、**Add Custom MetricSet** を選択します。

以下の詳細を入力して `credit.score.category` タグをインデックス化しましょう（**注意**: ワークショップの参加者全員が同じ組織を使用しているため、このステップはインストラクターが代わりに行います）。

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして続行します。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** 列のチェックマークをクリックします。

![MetricSet Configuraiton Applied](../images/metricset_config_applied.png)

## インデックス化するタグの選び方

なぜ `credit.score.category` タグを選んでインデックス化し、他のタグはインデックス化しなかったのでしょうか？

これを理解するために、タグの主なユースケースを確認しましょう。

* フィルタリング
* グルーピング

### フィルタリング

フィルタリングのユースケースでは、**Splunk Observability Cloud** の **Trace Analyzer** 機能を使用して、特定のタグ値に一致するトレースをフィルタリングできます。

先ほど、credit score が `7` で始まるトレースをフィルタリングした例を見ました。

また、顧客からサービスの遅さについて問い合わせがあった場合、**Trace Analyzer** を使用してその顧客番号を含むすべてのトレースを特定できます。

フィルタリングのユースケースで使用されるタグは、一般的にカーディナリティが高く、数千から数十万のユニークな値が存在する可能性があります。実際、**Splunk Observability Cloud** は事実上無限のユニークなタグ値を処理できます！これらのタグを使用したフィルタリングにより、目的のトレースを素早く特定できます。

**Trace Analyzer** でフィルタリングに使用するために、タグをインデックス化する必要はないことに注意してください。

### グルーピング

グルーピングのユースケースでは、**Trace Analyzer** を使用してトレースを特定のタグでグループ化できます。

さらに、**Splunk Observability Cloud** の強力な **Tag Spotlight** 機能を使用して、収集したタグのトレンドを可視化することもできます。この機能はまもなく実際に確認します。

グルーピングのユースケースで使用されるタグは、カーディナリティが低〜中程度で、数百のユニークな値を持つべきです。

カスタムタグを **Tag Spotlight** で使用するには、まずインデックス化する必要があります。

`credit.score.category` タグをインデックス化することにしたのは、グルーピングに有用な少数の異なる値を持っているためです。一方、customer number や credit score のタグは数百から数千のユニークな値を持ち、グルーピングよりもフィルタリングのユースケースにより適しています。

## Troubleshooting MetricSet と Monitoring MetricSet

このタグをインデックス化するために、**Troubleshooting MetricSet** と呼ばれるものを作成したことにお気づきかもしれません。Troubleshooting MetricSet（TMS）と呼ばれるのは、**Tag Spotlight** などの機能を使用してこのタグに関する問題をトラブルシュートできるためです。

また、選択しなかったもう1つのオプションとして **Monitoring MetricSet**（MMS）があることにもお気づきかもしれません。Monitoring MetricSet はトラブルシューティングを超えて、タグをアラートやダッシュボードに使用できるようにします。この概念については、ワークショップの後半で詳しく見ていきます。
