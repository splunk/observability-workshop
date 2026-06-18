---
title: 1. APM Explore
weight: 1
---

Splunk Observability Cloud の APM セクションをクリックすると、エラー率の高いサービスや、サービスとワークフローの R.E.D. メトリクスなど、APM データの概要が表示されます。

APM Service Map は、APM でインストルメントされたサービスと推論されたサービス間の依存関係と接続を表示します。マップは、時間範囲、環境、ワークフロー、サービス、タグフィルターでの選択に基づいて動的に生成されます。

**Service Map** をクリックすると、APM ユーザーワークフローに関連するサービスを確認できます。**Service Map** でサービスを選択すると、**Business Workflow** サイドペインのチャートが更新され、選択したサービスのメトリクスが表示されます。**Service Map** とすべてのインジケーターは、タイムピッカーおよび表示されるチャートデータと同期しています。

{{% notice title="Exercise" style="green" icon="running" %}}

* Service Map で **wire-transfer-service** をクリックします。

{{% /notice %}}

![APM Explore](../images/apm-business-workflow.png)

Splunk APM には、リアルタイムで発生している問題を確認し、問題がサービス、特定のエンドポイント、または基盤インフラストラクチャに関連しているかどうかを迅速に判断するための組み込みの **Service Centric Views** も提供されています。詳しく見てみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* 右側のペインで、青色の **wire-transfer-service** をクリックします。

{{% /notice %}}

![APM Service](../images/apm-service.png)
