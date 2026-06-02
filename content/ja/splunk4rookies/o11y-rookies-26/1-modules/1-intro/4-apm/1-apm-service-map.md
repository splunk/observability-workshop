---
title: 1. APM Service Map
weight: 1
---

APM Service Map は、APM で計装されたサービスと推論されたサービス間の依存関係と接続を表示します。マップは、time range、environment、workflow、service、tag の各フィルターでの選択に基づいて動的に生成されます。

RUM ウォーターフォールの APM リンクをクリックした際、その **WorkFlow Name** (`frontend:/cart/checkout`) に関与したサービスを表示するためのフィルターが、Service Map ビューに自動的に追加されました。

ワークフローに関与するサービスは **Service Map** で確認できます。サイドペインには、選択されたワークフローのチャートが表示されます。**Service Map** でサービスを選択すると、サイドペインのチャートが更新され、選択したサービスのメトリクスが表示されます。

{{% exercise title="Inspect paymentservice on the map" %}}

* Service Map で **paymentservice** をクリックして選択します。

![APM Explore](../images/apm-business-workflow.png)

{{< tabs >}}
{{% tab title="Question" %}}
**`paymentservice` を選択した状態で、サイドペインの Service Requests & Errors チャートから何が分かりますか？** **(1)**
{{% /tab %}}
{{% tab title="Answer" %}}
**Errors の割合が非常に高くなっています。**
{{% /tab %}}
{{< /tabs >}}

* Splunk APM には、リアルタイムで発生している問題を可視化し、その問題がサービス、特定のエンドポイント、または基盤となるインフラストラクチャのいずれに関連しているのかを素早く判断するのに役立つ、組み込みの **Service Centric Views** も用意されています。詳しく見ていきましょう。
* 右側のペインで、青色の **paymentservice** **(2)** をクリックします。

{{% /exercise %}}
