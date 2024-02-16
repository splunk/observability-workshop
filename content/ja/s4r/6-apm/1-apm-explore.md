---
title: 1. APM Explore
weight: 1
---

APM サービスマップは、APM で計装されたサービス、および、存在が推測されるサービス間の依存関係とつながりを表示します。このマップは、時間範囲、環境、ワークフロー、サービス、およびタグのフィルタで選択した内容に基づいて動的に生成されます。

RUM ウォーターフォールで APM リンクをクリックすると、サービスマップビューに自動的にフィルタが追加され、その **Workflow Name**（`frontend:/cart/checkout`）に関与したサービスが表示されます。

**Service Map** でワークフローに関係するサービスが表示されます。画面右側の **Business Workflow** の下には、選択したワークフローのチャートが表示されます。**Service Map** と **Business Workflow** のチャートは同期されています。**Service Map** 内であるサービスを選択すると、**Business Workflow** ペインのチャートが更新され、選択したサービスのメトリクスが表示されます。

![APM Business Workflow](../images/apm-business-workflow.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice** を Service Map でクリックしてください。

{{% /notice %}}

![APM Explore](../images/apm-explore.png)

Splunk APM は、発生している問題をリアルタイムに確認し、特定のサービス、特定のエンドポイント、またはこれらを支えるインフラストラクチャに関連しているかどうかを迅速に判断するために利用できる、メトリクスをチャートとして可視化する一連の組み込みダッシュボードを提供しています。これを詳しく見てみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice** パネルの右上にある **View Dashboard** をクリックしてください。

{{% /notice %}}
