---
title: Kubernetes Navigatorツアー
linkTitle: 2. Kubernetes Navigator
weight: 2
hidden: true
--- 

## 1. クラスターとワークロードビュー

Kubernetes Navigatorでは、Kubernetesデータを表示するための2つのユースケースが提供されています。

* **K8s workloads** はワークロード、つまり *デプロイメント* に関する情報を提供することに重点を置いています。
* **K8s nodes** はクラスター、ノード、Pod、コンテナのパフォーマンスに関するインサイトを提供することに重点を置いています。

最初に必要に応じてどちらかのビューを選択します（必要に応じていつでもビューを切り替えることができます）。このワークショップで最もよく使用するのはワークロードビューであり、そちらに焦点を当てます。

### 1.1 K8sクラスター名の確認

最初のタスクは、自分のクラスターを特定して見つけることです。クラスター名は、事前設定された環境変数 `INSTANCE` によって決定されます。クラスター名を確認するには、ターミナルで次のコマンドを実行します。

``` bash
echo $INSTANCE-k3s-cluster
```

クラスター名をメモしておいてください。ワークショップの後半でフィルタリングに使用します。

## 2. ワークロードとワークロード詳細ペイン

Observability UIの **Infrastructure** ページに移動し、**Kubernetes** を選択します。Kubernetesサービスのセットが表示され、その中に **Kubernetes workloads** ペインがあります。このペインには、すべてのワークロードで処理されている負荷の概要を示す小さなグラフが表示されます。**Kubernetes workloads** ペインをクリックすると、ワークロードビューに移動します。

最初は、Observability Cloud Orgに報告されているすべてのクラスターのすべてのワークロードが表示されます。いずれかのワークロードでアラートが発生している場合、下の画像の右上にハイライト表示されます。

![workloads](../images/k8s-workloads-screen.png)

次に、フィルターツールバーで **Cluster** でフィルタリングして自分のクラスターを見つけます。

{{% notice title="注意" style="info" %}}
検索ボックスに `emea-ws-7*` のような部分的な名前を入力すると、クラスターをすばやく見つけることができます。

また、デフォルトの時間範囲を **-4h** から直近15分（**-15m**）に切り替えることをお勧めします。
{{% /notice %}}

![workloads-filter](../images/k8s-workloads-filter.png)

これで、自分のクラスターのデータのみが表示されます。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
クラスターで実行されているワークロードの数と、ネームスペースの数はいくつですか？
{{% /notice %}}

### 2.1 Navigator選択チャートの使用

デフォルトでは、**Kubernetes Workloads** テーブルは `# Pods Failed` でフィルタリングされ、`k8s.namespace.name` でグループ化されています。`default` ネームスペースを展開して、そのネームスペース内のワークロードを確認します。

![k8s-workload-selection](../images/workload-selection.png)

次に、**Map** アイコン（**Table** アイコンの隣）を選択して、リストビューをヒートマップビューに変更します。このオプションを変更すると、次のような表示になります。

![k8s-Heat-map](../images/workloads-heatmap.png)

このビューでは、各ワークロードが色付きの四角形で表示されています。これらの四角形は、選択した **Color by** オプションに応じて色が変わります。色は正常性や使用率を視覚的に示しています。ヒートマップの右下にある **legend** の感嘆符アイコン {{% icon icon="exclamation-circle" %}} にカーソルを合わせると、意味を確認できます。

この画面のもう1つの有用なオプションは **Find outliers** で、**Color by** ドロップダウンで選択した内容に基づいてクラスターの履歴分析を提供します。

次に、**Color by** ドロップダウンボックスから **Network transferred (bytes)** を選択し、**Find outliers** をクリックして、ダイアログの **Scope** を **Per k8s.namespace.name** に、**Deviation from Median** に変更します。

![k8s-Heat-map](../images/set-find-outliers.png)

**Find Outliers** ビューは、ワークロード（または使用するNavigatorに応じて任意のサービス）の選択を表示し、何か変化があったかどうかをすばやく把握する必要がある場合に非常に便利です。

パフォーマンスが異なる（増加または減少した）項目（この場合はワークロード）を素早く把握でき、問題を発見しやすくなります。

### 2.2 Deployment Overviewペイン

Deployment Overviewペインでは、デプロイメントのステータスを素早く把握できます。デプロイメントのPodがPending、Running、Succeeded、Failed、Unknownのいずれの状態にあるかを一目で確認できます。

![k8s-workload-overview](../images/k8s-deployment-overview.png)

* *Running:* Podがデプロイされ、実行中の状態
* *Pending:* デプロイ待ち
* *Succeeded:* Podがデプロイされ、ジョブが完了して終了した状態
* *Failed:* Pod内のコンテナが実行され、何らかのエラーが返された状態
* *Unknown:* Kubernetesが既知の状態を報告していない状態（例えば、Podの起動中や停止中の場合など）

ワークロード名がチャートの表示幅を超えている場合は、マウスをホバーすることで名前を展開できます。

特定のワークロードにフィルタリングするには、**k8s.workload.name** 列のワークロード名の横にある3つのドット **...** をクリックし、ドロップダウンボックスから **Filter** を選択します。

![workload-add-filter](../images/workload-add-filter.png)

これにより、選択したワークロードがフィルターに追加されます。**default** ネームスペース内の単一のワークロードが表示されます。

![workload-add-filter](../images/heatmap-filter-down.png)

上のヒートマップから **default** ネームスペース内の **splunk-otel-collector-k8s-cluster-receiver** を見つけて、四角形をクリックしてワークロードの詳細情報を表示します。

![workload-add-filter](../images/k8s-workload-detail.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
otel-collectorのCPUリクエストとCPUリミットの単位は何ですか？
{{% /notice %}}

この時点でPodの情報をさらに掘り下げることができますが、それはこのワークショップの範囲外です。

## 3. Navigator Sidebar

ワークショップの後半で、Apacheサーバーをクラスターにデプロイします。デプロイすると **Navigator Sidebar** にアイコンが表示されます。

KubernetesのNavigatorでは、Navigator Sidebarで依存するサービスやコンテナを追跡できます。Navigator Sidebarを最大限に活用するには、`service.name` という追加ディメンションを設定して追跡するサービスを構成します。このワークショップでは、Apache監視用のCollector設定で `extraDimensions` をすでに構成しています。

```yaml
extraDimensions:
  service.name: php-apache
```

Navigator Sidebarが展開され、下の画像のように検出されたサービスへのリンクが追加されます。

![Pivotbar](../images/pivotbar.png)

これにより、Navigator間を簡単に切り替えることができます。Apacheサーバーインスタンスについても同様で、Navigator Sidebarから素早くKubernetes Navigatorに戻ることができます。
