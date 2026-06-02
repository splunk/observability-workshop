---
title: Kubernetes Navigator のツアー
linkTitle: 2. Kubernetes Navigator
weight: 2
hidden: true
--- 

## 1. Cluster ビューと Workload ビュー

Kubernetes Navigator では、Kubernetes データを表示するための 2 つの異なるユースケースが提供されています。

* **K8s workloads** はワークロード、つまり *デプロイメント* に関する情報の提供にフォーカスしています。
* **K8s nodes** はクラスター、ノード、Pod、コンテナのパフォーマンスに関するインサイトの提供にフォーカスしています。

最初に必要に応じてどちらかのビューを選択します（必要であればビューを動的に切り替えることもできます）。このワークショップで主に使用するのは workload ビューであり、こちらに焦点を当てて進めていきます。

### 1.1 K8s クラスター名の確認

最初のタスクは、ご自身のクラスターを特定することです。クラスターは事前構成された環境変数 `INSTANCE` に基づいて命名されています。クラスター名を確認するため、ターミナルで以下のコマンドを実行してください。

``` bash
echo $INSTANCE-k3s-cluster
```

ワークショップの後半でフィルタリングに使用するため、クラスター名をメモしておいてください。

## 2. Workloads と Workload Details ペイン

Observability UI で **Infrastructure** ページに移動し、**Kubernetes** を選択します。Kubernetes サービスのセットが表示され、その中の 1 つが **Kubernetes workloads** ペインです。このペインには小さなグラフが表示され、すべてのワークロードで処理されている負荷を俯瞰的に確認できます。**Kubernetes workloads** ペインをクリックすると、workload ビューに移動します。

最初は、Observability Cloud Org にレポートされているすべてのクラスターのすべてのワークロードが表示されます。いずれかのワークロードでアラートが発火している場合は、下の画像の右上にハイライト表示されます。

![workloads](../images/k8s-workloads-screen.png)

それでは、フィルターツールバーの **Cluster** でフィルタリングして、ご自身のクラスターを見つけましょう。

{{% notice title="Note" style="info" %}}
検索ボックスに `emea-ws-7*` のような部分一致の名前を入力すると、素早くクラスターを見つけることができます。

また、デフォルトの時間を **-4h** から直近 15 分（**-15m**）に変更しておくことを強くおすすめします。
{{% /notice %}}

![workloads-filter](../images/k8s-workloads-filter.png)

これで、ご自身のクラスターのデータのみが表示されるようになりました。

{{% notice title="Workshop Question" style="tip" icon="question" %}}
ご自身のクラスターでは、いくつのワークロードが実行されており、いくつの Namespace がありますか？
{{% /notice %}}

### 2.1 Navigator Selection Chart の使用

デフォルトでは、**Kubernetes Workloads** テーブルは `k8s.namespace.name` でグループ化された `# Pods Failed` でフィルタリングされています。`default` namespace を展開して、その namespace 内のワークロードを確認しましょう。

![k8s-workload-selection](../images/workload-selection.png)

次に、**Map** アイコン（**Table** アイコンの隣）を選択してリストビューをヒートマップビューに変更しましょう。このオプションを変更すると、以下のような可視化（または類似のもの）になります。

![k8s-Heat-map](../images/workloads-heatmap.png)

このビューでは、各ワークロードが色付きの四角形になっていることがわかります。これらの四角形は、選択した **Color by** オプションに応じて色が変化します。色は健全性や使用状況を視覚的に示しています。ヒートマップ右下の **legend** の感嘆符アイコン {{% icon icon="exclamation-circle" %}} にカーソルを合わせると、その意味を確認できます。

この画面のもう 1 つの便利なオプションが **Find outliers** で、**Color by** ドロップダウンで選択された内容に基づいて、クラスターの履歴分析を提供します。

それでは、**Color by** ドロップダウンボックスから **Network transferred (bytes)** を選択し、**Find outliers** をクリックして、ダイアログ内の **Scope** を **Per k8s.namespace.name** に、**Deviation from Median** を以下のように変更しましょう。

![k8s-Heat-map](../images/set-find-outliers.png)

**Find Outliers** ビューは、ワークロード（または使用している Navigator によっては任意のサービス）の一部を確認し、何かが変化したかどうかを素早く把握する必要があるときに非常に便利です。

通常とは異なる動作（増加・減少どちらの場合も）をしているアイテム（ここではワークロード）を素早くインサイトとして得られるため、問題の発見が容易になります。

### 2.2 Deployment Overview ペイン

Deployment Overview ペインでは、デプロイメントのステータスを素早く把握できます。デプロイメントの Pod が Pending、Running、Succeeded、Failed、Unknown のいずれの状態にあるかを一目で確認できます。

![k8s-workload-overview](../images/k8s-deployment-overview.png)

* *Running:* Pod がデプロイされ、実行中の状態
* *Pending:* デプロイ待ちの状態
* *Succeeded:* Pod がデプロイされ、ジョブが完了して終了した状態
* *Failed:* Pod 内のコンテナが実行され、何らかのエラーを返した状態
* *Unknown:* Kubernetes が既知のいずれの状態も報告していない状態（例えば Pod の起動中や停止中など）

ワークロード名がチャートで表示しきれない場合は、名前にカーソルを合わせると展開できます。

特定のワークロードにフィルタリングするには、**k8s.workload.name** 列のワークロード名の隣にある 3 つのドット **...** をクリックし、ドロップダウンから **Filter** を選択します。

![workload-add-filter](../images/workload-add-filter.png)

これにより、選択したワークロードがフィルターに追加されます。その結果、**default** namespace 内の単一のワークロードがリスト表示されます。

![workload-add-filter](../images/heatmap-filter-down.png)

上記のヒートマップから、**default** namespace 内の **splunk-otel-collector-k8s-cluster-receiver** を見つけ、四角形をクリックしてワークロードに関する詳細情報を確認します。

![workload-add-filter](../images/k8s-workload-detail.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
otel-collector の CPU request と CPU limit の単位はそれぞれ何ですか？
{{% /notice %}}

この時点で Pod の情報をさらに掘り下げて確認することもできますが、それは本ワークショップの範囲外です。

## 3. Navigator Sidebar

ワークショップの後半で、クラスターに Apache サーバーをデプロイすると、**Navigator Sidebar** にアイコンが表示されます。

Kubernetes 用の Navigator では、依存するサービスやコンテナを Navigator Sidebar で追跡できます。Navigator Sidebar を最大限に活用するには、`service.name` という追加 dimension を構成して、追跡したいサービスを設定します。本ワークショップでは、Apache を監視するために、コレクター構成内の `extraDimensions` を以下のようにすでに構成しています。

```yaml
extraDimensions:
  service.name: php-apache
```

下の画像のように、Navigator Sidebar が展開され、検出されたサービスへのリンクが追加されます。

![Pivotbar](../images/pivotbar.png)

これにより、Navigator 間を簡単に切り替えることができます。同じことが Apache サーバーインスタンスにも当てはまり、Navigator Sidebar から Kubernetes Navigator にすばやく戻ることができます。
