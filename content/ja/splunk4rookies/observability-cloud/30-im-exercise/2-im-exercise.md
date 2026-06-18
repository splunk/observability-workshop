---
title: Infrastructure Exercise - Part 2
linkTitle: Part 2
weight: 2
time: 10 minutes
---

ここからは Infrastructure Monitoring 演習のパート2です。現在、単一のクラスターが表示されているはずです。

![Alt Cluster](../images/k8s-cluster.png)

* Kubernetes Navigator では、クラスターは黒い線で囲まれた四角形で表されます。
* その中にはノードまたはコンピューティングエンジンを表す1つ以上の青い四角形が含まれます。
* 各ノードには Pod を表す1つ以上の色付きボックスが含まれます（サービスはここで実行されます）。
* ご想像の通り、**green** は正常を意味し、**red** は問題があることを意味します。

赤いボックスまたはタイルが2つあるので、何が起きているのか、Online Boutique サイトに影響があるのか確認しましょう。

{{% exercise title="クラスターと Pod の正常性を確認する" %}}

* まず、作業する時間枠を過去15分に設定します。フィルターペインの Time picker を **-4h** から **Last 15 minutes** に変更してください。
* マウスをクラスター、ノード、Pod（**green** と **red** の両方）の上にホバーしてください。
* 表示される情報ペインに、オブジェクトの状態が表示されます。**red** の Pod は **Pod Phase: Failed** と表示されていることに注目してください。これはクラッシュして動作していないことを意味します。
* クラスターに関する情報を提供する Cluster Metric チャートを確認してください（クラスター画像の下にあるチャートです）。メモリ消費量やノードあたりの Pod 数など、クラスターの正常性に関する一般的な情報を提供します。
* **red** の Pod についてはフラグが立っていません。クラッシュした Pod は Kubernetes のパフォーマンスに影響を与えないためです。
* Splunk Kubernetes Analyzer がより有用な情報を提供できるか確認しましょう。**K8s Analyzer** をクリックしてください。
{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}

Splunk Kubernetes Analyzer は Splunk Observability Cloud のバックグラウンドで実行されるスマートプロセスで、異常間の関連性を検出するように設計されています。

{{% /notice %}}

* **K8s Analyzer** は、2つの **red** Pod が類似していることを検出しているはずです（各行の後の2で示されます）。また、同じ Namespace で実行されていることがわかります。
* K8s analyzer ビューでどの namespace かわかりますか？（ヒント: `k8s.namespace.name` を探してください）。
* 次に、ノードレベルでも確認したいので、ノードにドリルダウンします。まず、クラスターの上にマウスをホバーし、黒いクラスターラインの内側、左上に ![blue triangle ](../images/node-blue-traingle.png?classes=inline) がある青い線がノードの周りに表示されるまで待ちます。
* 三角形をクリックしてください。各 Pod 内に小さなボックスが表示されるはずです。これらは実際のコードを実行するコンテナを表しています。*K8s Analyzer* は、この問題がノードレベルでも発生していることを確認するはずです。

![Analyser result](../images/k8s-analyser-result.png?width=20vw)

* **K8s node** をクリックしてください。ノードメトリクスが表示され、チャートを確認すると、development namespace には2つの Pod しかないことがわかります。
* Filter Pane で `k8s.namespace.name=development` でフィルターするとより見やすくなります。**# Total Pods** チャートには2つの Pod のみが表示され、**Node Workload** チャートには *test-job* のみがあり、失敗していることがわかります。

{{% notice title="Spunk Kubernetes Analyzer" style="info" %}}

上記のシナリオは、チームがさまざまなステージでアプリケーションをデプロイする共有 Kubernetes 環境では一般的です。Kubernetes はこれらの環境を完全に分離するように設計されています。

{{% /notice %}}

{{% /exercise %}}

Online Boutique サイトを構成する Pod はいずれも development namespace で実行されておらず、他のすべての Pod は green です。これらの Pod は影響を与えないと安全に判断できるので、さらにいくつかの項目を確認しましょう。
