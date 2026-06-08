---
title: Service Centric View
linkTitle: 4. Service Centric View
weight: 4
---

Splunk APM は **Service Centric Views** を提供しており、エンジニアはサービスのパフォーマンスを一元化されたビューで深く理解できます。すべてのサービスにわたって、エンジニアはサービスの基盤インフラストラクチャからエラーやボトルネックを迅速に特定し、新しいデプロイメントによるパフォーマンス低下を正確に把握し、すべてのサードパーティ依存関係の健全性を可視化できます。

`api-gateway` のこのダッシュボードを表示するには、左側のメニューから **APM → Overview** をクリックし、「Navigate to a service, business transaction, or trace」フィールドをクリックして、ドロップダウンリストから `api-gateway` サービスを選択します。これにより、Service Centric View ダッシュボードが表示されます

![service_maps](../../images/service-view.png)

このビューは計装された各サービスで利用可能であり、**Service metrics**、**Error breakdown**、**Runtime metrics (Java)**、および **Infrastructure metrics** の概要を提供します。
