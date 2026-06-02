---
title: 1. APM Explore
weight: 1
---

APM Service Map は、APM で計装されたサービスおよび推測されたサービス間の依存関係と接続を表示します。マップは、時間範囲、環境、ワークフロー、サービス、タグフィルターで選択した内容に基づいて動的に生成されます。

RUM ウォーターフォールで APM リンクをクリックした際、その **WorkFlow Name** (`frontend:/cart/checkout`) に関係するサービスを表示するために、Service Map ビューにフィルターが自動的に追加されました。

ワークフローに関係するサービスは **Service Map** で確認できます。サイドペインの **Business Workflow** には、選択したワークフローに関するチャートが表示されます。**Service Map** と **Business Workflow** のチャートは同期しています。**Service Map** でサービスを選択すると、**Business Workflow** ペインのチャートが更新され、選択したサービスのメトリクスが表示されます。

{{% exercise title="Inspect paymentservice on the map" %}}

* Service Map で **paymentservice** をクリックします。

{{% /exercise %}}

![APM Explore](../images/apm-business-workflow.png)

Splunk APM はさらに、組み込みの **Service Centric Views** を提供しており、リアルタイムで発生している問題を確認し、その問題がサービス、特定のエンドポイント、または基盤となるインフラストラクチャのいずれに関連しているのかを迅速に判断できます。詳しく見ていきましょう。

{{% exercise title="Open the paymentservice view" %}}

* 右側のペインで、青色の **paymentservice** をクリックします。

{{% /exercise %}}

![APM Service](../images/apm-service.png)
