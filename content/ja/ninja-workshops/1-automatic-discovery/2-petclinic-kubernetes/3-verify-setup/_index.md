---
title: Kubernetes クラスターメトリクスの確認
linkTitle: 3. クラスターメトリクスの確認
weight: 4
time: 10 minutes
---

インストールが完了したら、**Splunk Observability Cloud** にログインして、Kubernetes クラスターからメトリクスが流れてきていることを確認できます。

左側のメニューから **Infrastructure** をクリックし、**Kubernetes** を選択してから、**Kubernetes nodes** タイルを選択します。

![NavigatorList](../images/navigatorlist.png)

**Kubernetes nodes** の概要画面に入ったら、**Time** フィルタを **-1h** から過去15分 **(-15m)** に変更して最新のデータに焦点を当て、次に **Table** を選択してメトリクスを報告しているすべてのノードをリスト表示します。

次に、**Refine by:** パネルで **Cluster name** を選択し、リストからご自身のクラスターを選択します。

{{% notice title="Tip" style="info" icon="lightbulb" %}}
特定のクラスターを識別するには、セットアップ中に実行したシェルスクリプト出力の `INSTANCE` 値を使用してください。この一意の識別子により、リスト内の他のノードの中からワークショップクラスターを見つけることができます。
{{% /notice %}}

これにより、ご自身のクラスターのノードのみを表示するようにリストがフィルタリングされます。

![K8s Nodes](../images/k8s-nodes.png)

**K8s node logs** ビューに切り替えて、ノードからのログを確認します。

![Logs](../images/k8s-peek-at-logs.png)
