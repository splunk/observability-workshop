---
title: 1. APM Service Map
weight: 1
---

APM Service Map は、APM で計装されたサービスおよび推論されたサービス間の依存関係と接続を表示します。マップは、時間範囲、environment、ビジネストランザクション、サービス、tag フィルターでの選択に基づいて動的に生成されます。

RUM ウォーターフォールで APM のリンクをクリックすると、その **Transaction**（`frontend:/cart/checkout`）に関係するサービスを表示するために、Service Map ビューにフィルターが自動的に追加されました。

**Service Map** で、ワークフローに関係するサービスを確認できます。サイドペインには、選択したトランザクションのチャートが表示されます。**Service Map** でサービスを選択すると、サイドペインのチャートが更新され、選択したサービスのメトリクスが表示されます。

{{% exercise title="マップ上で paymentservice を確認する" %}}

* Service Map で **paymentservice** をクリックして選択します。

![APM Explore](../images/apm-business-workflow.png)

{{< tabs >}}
{{% tab title="Question" %}}
**`paymentservice` を選択した状態で、サイドペインの Service Requests & Errors チャートから何が読み取れますか？** **(1)**
{{% /tab %}}
{{% tab title="Answer" %}}
**Errors の割合が非常に高くなっています。**
{{% /tab %}}
{{< /tabs >}}

* Splunk APM には、リアルタイムで発生している問題を可視化し、その問題がサービス、特定のエンドポイント、または基盤となるインフラストラクチャーのいずれに関連しているのかを素早く判断できるよう、**Service Centric Views** が組み込みで用意されています。詳しく見ていきましょう。
* 右側のペインで、青字の **paymentservice** をクリックします **(2)**。

{{% /exercise %}}
