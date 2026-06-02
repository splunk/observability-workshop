---
title: Infrastructure Exercise - Part 2
linkTitle: Part 2
weight: 2
time: 10 minutes
---

ここは Infrastructure Monitoring エクササイズの Part 2 です。これまでの手順で、1 つのクラスターが表示されているはずです。

![Alt Cluster](../images/k8s-cluster.png)

* Kubernetes Navigator では、クラスターは黒い線で囲まれた四角形で表されます。
* その中には、ノード（コンピュートエンジン）を表す 1 つ以上の青い四角形が含まれます。
* それぞれの中には、Pod を表す 1 つ以上の色付きの四角形が含まれます（Pod はサービスが実行される場所です）。
* ご想像のとおり、**緑** は健全であることを、**赤** は問題があることを意味します。

赤い四角（タイル）が 2 つあるので、何が起きているのか、そしてこれが Online Boutique サイトに影響を与えるかどうかを確認していきましょう。

{{% exercise title="Inspect cluster and pod health" %}}

* まず、対象とする時間枠を直近 15 分に設定します。フィルターペインの Time picker を **-4h** から **Last 15 minutes** に変更します。
* Cluster、Node、Pod の上にマウスをホバーしてください。**緑** と **赤** の両方を確認します。
* 表示される情報ペインで、オブジェクトの状態を確認できます。**赤** の Pod は **Pod Phase: Failed** と表示されており、クラッシュして動作していないことを意味します。
* クラスターに関する情報を提供する Cluster Metric チャート（クラスター画像の下にあるチャート）を確認しましょう。これらは、メモリ消費量やノードあたりの Pod 数など、クラスターの健全性に関する一般的な情報を提供します。
* **赤** の Pod に関するフラグは何も立ちません。これは、クラッシュした Pod が Kubernetes のパフォーマンスには影響しないためです。
* Splunk Kubernetes Analyzer がもっと有用な情報を教えてくれるかどうか確認しましょう。**K8s Analyzer** をクリックしてください。
{{% notice title=" Spunk Kubernetes Analyzer" style="info" %}}

Splunk Kubernetes Analyzer は、Splunk Observability Cloud のバックグラウンドで動作するスマートなプロセスで、異常間の関連性を検出するように設計されています。

{{% /notice %}}

* **K8s Analyzer** は、2 つの **赤** の Pod が類似しており（各行の末尾の 2 で示されます）、同じ Namespace で実行されていることを検出しているはずです。
* K8s Analyzer ビューで、どの Namespace か特定できますか？（ヒント: `k8s.namespace.name` を確認してください）
* 次に、これをノードレベルでも確認したいので、ノードにドリルダウンしましょう。まず、クラスターの上にマウスをホバーして、黒いクラスターラインの内側、ノードの周りに青い線が表示され、左上に ![blue triangle ](../images/node-blue-traingle.png?classes=inline) が現れるまで待ちます。
* その三角形をクリックします。各 Pod 内に小さな四角形が表示されるはずです。これらは実際のコードを実行するコンテナを表しています。*K8s Analyzer* は、この問題がノードレベルでも発生していることを確認できるはずです。

![Analyser result](../images/k8s-analyser-result.png?width=20vw)

* **K8s node** をクリックします。ノードのメトリクスが表示されるので、チャートを確認すると、development Namespace には Pod が 2 つしかないことが分かります。
* Filter Pane で `k8s.namespace.name=development` でフィルタリングすると、より見やすくなります。**# Total Pods** チャートは Pod が 2 つしかないことを示し、**Node Workload** チャートには *test-job* のみが表示され、それが失敗していることが分かります。

{{% notice title="Spunk Kubernetes Analyzer" style="info" %}}

上記のシナリオは、チームが異なるステージでアプリケーションをデプロイする共有 Kubernetes 環境ではよくあるものです。Kubernetes は、これらの環境を完全に分離するように設計されています。

{{% /notice %}}

{{% /exercise %}}

Online Boutique サイトを構成する Pod はどれも development Namespace では実行されておらず、他の Pod はすべて緑です。したがって、これらの Pod は私たちには影響しないと安全に判断できます。それでは、もう少し他のものを見ていきましょう。
