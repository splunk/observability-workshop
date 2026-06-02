---
title: Kubernetes クラスターメトリクスの確認
linkTitle: 3. クラスターメトリクスの確認
weight: 4
time: 10 minutes
---

インストールが完了したら、**Splunk Observability Cloud** にログインし、Kubernetes クラスターからメトリクスが流れ込んでいることを確認します。

左側のメニューから **Infrastructure** をクリックし、**Kubernetes** を選択して、**Kubernetes nodes** タイルを選択します。

![NavigatorList](../images/navigatorlist.png)

**Kubernetes nodes** の概要画面に入ったら、**Time** フィルターを **-1h** から直近 15 分 **(-15m)** に変更して最新のデータに焦点を当て、**Table** を選択してメトリクスをレポートしているすべてのノードを一覧表示します。

次に、**Refine by:** パネルで **Cluster name** を選択し、リストからご自身のクラスターを選択します。

{{% notice title="ヒント" style="info" icon="lightbulb" %}}
ご自身のクラスターを特定するには、セットアップ時に実行したシェルスクリプトの出力にある `INSTANCE` の値を使用します。この一意の識別子により、リスト内の他のノードの中からワークショップ用のクラスターを見つけることができます。
{{% /notice %}}

これにより、リストにはご自身のクラスターのノードのみが表示されるようにフィルターされます。

![K8s Nodes](../images/k8s-nodes.png)

**K8s node logs** ビューに切り替えて、ノードからのログを確認します。

![Logs](../images/k8s-peek-at-logs.png)
