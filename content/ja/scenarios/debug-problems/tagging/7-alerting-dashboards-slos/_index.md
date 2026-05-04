---
title: タグを使ったモニタリング
linkTitle: 7. タグを使ったモニタリング
weight: 7
time: 15 minutes
---


先ほど、`credit.score.category` タグに **Troubleshooting Metric Set** を作成しました。これにより、**Tag Spotlight** でそのタグを使用して、一部のユーザーが悪いエクスペリエンスを受けた理由を説明するパターンを特定できました。

このセクションでは、関連する概念である **Monitoring MetricSets** について見ていきます。

## Monitoring MetricSets とは？

**Monitoring MetricSets** はトラブルシューティングを超えて、タグをアラート、ダッシュボード、SLO に使用できるようにします。

## Monitoring MetricSet の作成

（**注意**: *以下の手順はワークショップのインストラクターが代わりに行いますが、手順を確認してください*）

**Settings** -> **APM & RUM MetricSets** に移動し、`credit.score.category` の MetricSet の横にある編集ボタン（鉛筆アイコン）をクリックします。

![edit APM MetricSet](../images/edit_apm_metricset.png)

**Also create Monitoring MetricSet** の横にあるチェックボックスをオンにして、**Start Analysis** をクリックします。

![Monitoring MetricSet](../images/monitoring_metricset.png)

`credit.score.category` タグが再び **Pending MetricSet** として表示されます。しばらくするとチェックマークが表示されます。このチェックマークをクリックして **Pending MetricSet** を有効にします。

![pending APM MetricSet](../images/update_pending_apm_metricset.png)

## Monitoring MetricSets の使用

このメカニズムは、タグから新しいディメンションを作成し、その新しいディメンションの値に基づいてメトリクスをフィルタリングできるようにします。**重要**: オリジナルとコピーを区別するために、タグ名のドットは新しいディメンションではアンダースコアに置き換えられます。そのため、メトリクスのディメンション名は `credit.score.category` ではなく `credit_score_category` となります。

次に、この **Monitoring MetricSet** をどのように活用できるか見ていきましょう。
