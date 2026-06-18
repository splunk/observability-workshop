---
title: Infrastructure Exercise - Part 2
linkTitle: Part 2
weight: 2
time: 10 minutes
---

これは Infrastructure Monitoring 演習のパート 2 です。ここまでで単一のクラスターが表示されているはずです。

![Alt Cluster](../images/k8s-cluster.png)

* Kubernetes Navigator では、クラスターは黒い線で囲まれた四角形で表されます。
* その中にノードまたはコンピュートエンジンを表す 1 つ以上の青い四角形が含まれています。
* さらにその中に Pod を表す 1 つ以上の色付きボックスが含まれています（サービスが実行される場所です）。
* ご想像の通り、**green** は正常を意味し、**red** は問題があることを意味します。

赤いボックスまたはタイルが 2 つあるので、何が起きているのか、そしてこれが Online Boutique サイトに影響するかどうかを確認しましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* まず、作業する時間ウィンドウを過去 15 分に設定します。フィルターペインの Time picker を **-4h** から **Last 15 minutes** に変更してください。
* マウスを Cluster、Node、Pod（**green** と **red** の両方）の上にホバーしてください。
* 表示される情報ペインにオブジェクトの状態が表示されます。**red** の Pod は **Pod Phase: Failed** と表示されていることに注意してください。これはクラッシュして動作していないことを意味します。
* クラスターに関する情報を提供する Cluster Metric チャートを確認してください（クラスターイメージの下にあるチャートです）。メモリ消費量やノードあたりの Pod 数など、クラスターの全般的な健全性に関する情報が提供されます。
* **red** の Pod に対してフラグは立ちません。クラッシュした Pod は Kubernetes のパフォーマンスに影響しないためです。
* Splunk Kubernetes Analyzer がより有用な情報を提供してくれるか確認しましょう。**K8s Analyzer** をクリックしてください。
{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}

Splunk Kubernetes Analyzer は、Splunk Observability Cloud のバックグラウンドで実行されるスマートプロセスで、異常間の関係を検出するように設計されています。

{{% /notice %}}

* **K8s Analyzer** は、2 つの **red** Pod が類似していることを検出しているはずです（各行の後の 2 で示されます）。また、同じ Namespace で実行されていることも検出されます。
* K8s analyzer ビューで、どの namespace か見つけられますか？（ヒント: `k8s.namespace.name` を探してください）。
* 次に、ノードレベルでもこれを確認したいので、ノードにドリルダウンします。まず、クラスターの上にマウスをホバーし、黒い Cluster Line の内側のノードの周りに青い線が表示され、左上に ![blue triangle ](../images/node-blue-traingle.png?classes=inline) が見えるまで待ちます。
* 三角形をクリックしてください。ビューに各 Pod 内の小さなボックスが表示されるはずです。これらは実際のコードを実行するコンテナを表しています。*K8s Analyzer* がこの問題がノードレベルでも発生していることを確認するはずです。

![Analyser result](../images/k8s-analyser-result.png?width=20vw)

* **K8s node** をクリックしてください。ノードメトリクスが表示されます。チャートを確認すると、development namespace には 2 つの Pod しかないことがわかります。
* Filter Pane で `k8s.namespace.name=development` でフィルタリングするとより見やすくなります。**# Total Pods** チャートには 2 つの Pod のみが表示され、**Node Workload** チャートには *test-job* のみが表示されており、失敗しています。

{{% notice title="Spunk Kubernetes Analyzer" style="info" %}}

上記のシナリオは、チームがさまざまなステージでアプリケーションをデプロイする共有 Kubernetes 環境では一般的です。Kubernetes はこれらの環境を完全に分離するように設計されています。

{{% /notice %}}

{{% /notice %}}

Online Boutique サイトを構成する Pod はいずれも development namespace で実行されておらず、他のすべての Pod は green です。これらの Pod は影響しないと安全に判断できるので、さらにいくつかの項目を確認していきましょう。
