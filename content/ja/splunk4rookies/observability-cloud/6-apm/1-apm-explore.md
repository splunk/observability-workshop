---
title: 1. APM探索
weight: 1
---

APMサービスマップは、APMで計装された（インストルメンテーション）サービスと推測されるサービスの間の依存関係と接続を表示します。このマップは、時間範囲、環境、ワークフロー、サービス、タグフィルターでの選択に基づいて動的に生成されます。

RUMウォーターフォールでAPMリンクをクリックすると、そのワークフロー名（`frontend:/cart/checkout`）に関連するサービスを表示するために、サービスマップビューに自動的にフィルターが追加されました。

ワークフローに関連するサービスは**Service Map**で確認できます。サイドペインの**Business Workflow**の下には、選択したワークフローのチャートが表示されています。**Service Map**とビジネスワークフローチャートは同期しています。**Service Map**でサービスを選択すると、**Business Workflow**ペインのチャートが更新され、選択したサービスのメトリクスが表示されます。

{{% notice title="演習" style="green" icon="running" %}}

- サービスマップで**paymentservice**をクリックします。

{{% /notice %}}

![APM探索](../images/apm-business-workflow.png)

Splunk APMはまた、リアルタイムで発生している問題を確認し、問題がサービス、特定のエンドポイント、または基盤となるインフラストラクチャに関連しているかどうかを迅速に判断するのに役立つ組み込みの **Service Centric View(サービス中心ビュー)** も提供しています。より詳しく見てみましょう。

{{% notice title="演習" style="green" icon="running" %}}

- 右側のペインで、青色の**paymentservice**をクリックします。

{{% /notice %}}

![APMサービス](../images/apm-service.png)
