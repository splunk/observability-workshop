---
title: 1. APM Explore
weight: 1
---

APMサービスマップは、APMのインストゥルメンテーションおよび推測されたサービス間の依存関係と接続を表示します。このマップは、時間範囲、環境、ワークフロー、サービス、およびタグのフィルタで選択した内容に基づいて動的に生成されます。

RUMウォーターフォールでAPMリンクをクリックすると、サービスマップビューに自動的にフィルタが追加され、その**WorkFlow Name**（`frontend:/cart/checkout`）に関与したサービスが表示されます。

**サービスマップ**でワークフローに関与するサービスが表示されます。サイドペインの**ビジネスワークフロー**の下には、選択したワークフローのチャートが表示されます。**サービスマップ**と**ビジネスワークフロー**のチャートは同期されています。**サービスマップ**でサービスを選択すると、**ビジネスワークフロー**ペインのチャートが更新され、選択したサービスのメトリクスが表示されます。

![APM Business Workflow](../images/apm-business-workflow.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice**をサービスマップでクリックしてください。

{{% /notice %}}

![APM Explore](../images/apm-explore.png)

Splunk APMは、リアルタイムで発生している問題を確認し、問題がサービス、特定のエンドポイント、または基盤インフラストラクチャに関連しているかどうかを迅速に判断するための、視覚化されたメトリクスとチャートを提供する一連の組み込みダッシュボードもあります。これを詳しく見てみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice**パネルの右上にある**View Dashboard**をクリックしてください。

{{% /notice %}}
