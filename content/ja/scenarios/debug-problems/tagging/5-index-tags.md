---
title: タグのインデックス化
linkTitle: 5. Index Tags
weight: 5
time: 5 minutes
---

## タグのインデックス化

**Tag Spotlight** などの **Splunk Observability Cloud** の高度な機能を使用するには、まず1つ以上のタグをインデックス化する必要があります。

これを行うには、**Settings** -> **APM & RUM MetricSets** に移動します。**APM** タブが選択されていることを確認してください（**RUM** ではありません）。**Add MetricSet Configuration** ボタンをクリックし、**Add Custom MetricSet** を選択します。

以下の詳細を入力して `credit.score.category` タグをインデックス化しましょう（**注意**: ワークショップの参加者全員が同じ組織を使用しているため、このステップはインストラクターが代わりに実施します）:

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

**Start Analysis** をクリックして続行します。

分析が実行されている間、タグは **Pending MetricSets** のリストに表示されます。

![Pending MetricSets](../images/pending_metric_set.png)

分析が完了したら、**Actions** 列のチェックマークをクリックします。

![MetricSet Configuraiton Applied](../images/metricset_config_applied.png)

## インデックス化するタグの選び方

なぜ `credit.score.category` タグをインデックス化し、他のタグはインデックス化しなかったのでしょうか？

これを理解するために、タグの主なユースケースを確認しましょう:

* フィルタリング
* グルーピング

### フィルタリング

フィルタリングのユースケースでは、**Splunk Observability Cloud** の **Trace Analyzer** 機能を使用して、特定のタグ値に一致するトレースをフィルタリングできます。

先ほど、クレジットスコアが `7` で始まるトレースをフィルタリングした例を見ました。

また、顧客がサービスの遅さについて問い合わせてきた場合、**Trace Analyzer** を使用して、その特定の顧客番号を持つすべてのトレースを見つけることができます。

フィルタリングのユースケースで使用されるタグは、一般的に高カーディナリティです。つまり、数千から数十万のユニークな値が存在する可能性があります。実際、**Splunk Observability Cloud** は事実上無限のユニークなタグ値を処理できます！これらのタグを使用したフィルタリングにより、目的のトレースを迅速に見つけることができます。

**Trace Analyzer** でフィルタリングに使用するために、タグをインデックス化する必要はないことに注意してください。

### グルーピング

グルーピングのユースケースでは、**Trace Analyzer** を使用して、特定のタグでトレースをグループ化できます。

さらに、**Splunk Observability Cloud** の強力な **Tag Spotlight** 機能を使用して、収集したタグの傾向を表面化することもできます。これについてはすぐに実際の動作を見ていきます。

グルーピングのユースケースで使用されるタグは、低〜中カーディナリティで、数百のユニークな値を持つべきです。

カスタムタグを **Tag Spotlight** で使用するには、まずインデックス化する必要があります。

`credit.score.category` タグをインデックス化することにしたのは、グルーピングに役立つ少数の異なる値を持っているためです。一方、顧客番号やクレジットスコアのタグは数百から数千のユニークな値を持ち、グルーピングよりもフィルタリングのユースケースに適しています。

## Troubleshooting MetricSet と Monitoring MetricSet

このタグをインデックス化するために、**Troubleshooting MetricSet** と呼ばれるものを作成したことにお気づきかもしれません。Troubleshooting MetricSet（TMS）は、**Tag Spotlight** などの機能を使用してこのタグに関する問題をトラブルシューティングできるため、このように名付けられています。

また、今回選択しなかった **Monitoring MetricSet**（MMS）というオプションがあることにもお気づきかもしれません。Monitoring MetricSet はトラブルシューティングを超えて、タグをアラートやダッシュボードに使用できるようにします。この概念については、ワークショップの後半で探っていきます。
