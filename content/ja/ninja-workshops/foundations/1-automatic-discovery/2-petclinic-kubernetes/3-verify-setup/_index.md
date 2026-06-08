---
title: Kubernetes クラスターメトリクスの確認
linkTitle: 3. クラスターメトリクスの確認
weight: 4
time: 10 minutes
---

インストールが完了したら、**Splunk Observability Cloud** にログインして、Kubernetes クラスターからメトリクスが送信されていることを確認できます。

左側のメニューから **Infrastructure** をクリックし、**Kubernetes overview** を選択します。少なくとも1つのフィルターを適用するよう求められます。**k8s.cluster.name** フィールドの内部をクリックし、`<INSTANCE>-k3s-cluster`（`<INSTANCE>` は先ほどメモした値に置き換えてください）を選択します。**Apply Filters** をクリックします。

![K8s Filter Dialog](../images/k8s-filter-dialog.png)

**Kubernetes overview** に入ったら、**Nodes (3)** カードのタイトルを選択して、メトリクスを報告しているクラスター内のすべてのノードを一覧表示します。

![K8s Overview](../images/k8s-overview.png)

次に、**Kubernetes entities** パネルで、最も多くの Pod をホストしているノードを選択します。ノード名は `k3d-<INSTANCE>-cluster-server-0` またはそれに類似した名前になります。

![K8s Node List](../images/k8s-node-list.png)

ノードパネルで **Logs** タブを選択して、該当ノードのログを確認します。

![K8s Node Logs](../images/k8s-node-logs.png)
