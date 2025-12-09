---
title: Service Centric View
linkTitle: 4. Service Centric View
weight: 4
---

Splunk APMは、エンジニア (engineer) に1つの集中ビュー (view) でサービスパフォーマンス (performance) の深い理解を提供する**Service Centric Views**を提供します。すべてのサービスにわたって、エンジニアはサービスの基盤となるインフラストラクチャ (infrastructure) からのエラー (error) やボトルネック (bottleneck) を迅速に特定し、新しいデプロイ (deploy) によるパフォーマンス低下を特定し、すべてのサードパーティ依存関係の健全性を可視化できます。

`api-gateway`のこのダッシュボード (dashboard) を表示するには、左側のメニューから**APM**をクリックし、リストの`api-gateway`サービスをクリックします。これにより、Service Centric Viewダッシュボードが表示されます：

![service_maps](../../images/service-view.png)

インストルメント (instrument) された各サービスで利用可能なこのビューは、**Service metrics**、**Error breakdown**、**Runtime metrics (Java)**、**Infrastructure metrics**の概要を提供します。
