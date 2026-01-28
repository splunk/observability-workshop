---
title: Kubernetes Navigator のツアー
linkTitle: 2. Kubernetes Navigator
weight: 2
hidden: true
---

## 1. クラスタービューとワークロードビュー

Kubernetes Navigator は、Kubernetes データを表示するための2つの異なるユースケースを提供します。

* **K8s workloads** は、ワークロード（*デプロイメント*）に関する情報の提供に焦点を当てています。
* **K8s nodes** は、クラスター、ノード、Pod、コンテナのパフォーマンスに関する洞察を提供することに焦点を当てています。

最初に、必要に応じてどちらかのビューを選択します（必要に応じてビューを切り替えることができます）。このワークショップで最もよく使用するのはワークロードビューであり、特にそれに焦点を当てます。

### 1.1 K8s クラスター名の確認

最初のタスクは、クラスターを識別して見つけることです。クラスターは、事前設定された環境変数 `INSTANCE` によって決定された名前が付けられます。クラスター名を確認するには、ターミナルで以下のコマンドを入力します:

``` bash
echo $INSTANCE-k3s-cluster
```

ワークショップの後半でフィルタリングに必要になるため、クラスター名をメモしておいてください。

## 2. ワークロードとワークロード詳細ペイン

Observability UI の **Infrastructure** ページに移動し、**Kubernetes** を選択します。これにより、一連の Kubernetes サービスが表示され、その1つが **Kubernetes workloads** ペインです。このペインには、すべてのワークロードで処理されている負荷の概要を示す小さなグラフが表示されます。**Kubernetes workloads** ペインをクリックすると、ワークロードビューに移動します。

最初は、Observability Cloud 組織に報告されているすべてのクラスターのすべてのワークロードが表示されます。いずれかのワークロードでアラートが発火した場合、以下の画像の右上にハイライト表示されます。

![workloads](../images/k8s-workloads-screen.png)

次に、フィルターツールバーで **Cluster** をフィルタリングしてクラスターを見つけましょう。

{{% notice title="注意" style="info" %}}
`emea-ws-7*` のような部分的な名前を検索ボックスに入力して、クラスターをすばやく見つけることができます。

また、デフォルトの時間を **-4h** から過去15分（**-15m**）に切り替えることを強くお勧めします。
{{% /notice %}}

![workloads-filter](../images/k8s-workloads-filter.png)

これで、自分のクラスターのデータのみが表示されます。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
クラスターで実行されているワークロードの数と Namespace の数はいくつですか？
{{% /notice %}}

### 2.1 Navigator 選択チャートの使用

デフォルトでは、**Kubernetes Workloads** テーブルは `k8s.namespace.name` でグループ化された `# Pods Failed` でフィルタリングされます。`default` Namespace を展開して、Namespace 内のワークロードを確認してください。

![k8s-workload-selection](../images/workload-selection.png)

次に、**Map** アイコン（**Table** アイコンの横）を選択して、リストビューをヒートマップビューに変更しましょう。このオプションを変更すると、以下のような（または類似の）可視化が表示されます:

![k8s-Heat-map](../images/workloads-heatmap.png)

このビューでは、各ワークロードが色付きの四角形になっていることに気付くでしょう。これらの四角形は、選択した **Color by** オプションに応じて色が変わります。色は、健全性や使用状況を視覚的に示します。ヒートマップの右下にある **legend** の感嘆符アイコン {{% icon icon="exclamation-circle" %}} にカーソルを合わせると、意味を確認できます。

この画面のもう1つの有用なオプションは **Find outliers** です。これは、**Color by** ドロップダウンで選択された内容に基づいて、クラスターの履歴分析を提供します。

次に、**Color by** ドロップダウンボックスから **Network transferred (bytes)** を選択し、**Find outliers** をクリックして、ダイアログの **Scope** を以下のように **Per k8s.namespace.name** と **Deviation from Median** に変更します:

![k8s-Heat-map](../images/set-find-outliers.png)

**Find Outliers** ビューは、ワークロード（または使用する Navigator に応じて任意のサービス）の選択を表示し、何かが変更されたかどうかをすばやく把握する必要がある場合に非常に便利です。

これにより、パフォーマンスが異なる（増加または減少）項目（この場合はワークロード）に関する迅速な洞察が得られ、問題を見つけやすくなります。

### 2.2 デプロイメント概要ペイン

デプロイメント概要ペインでは、デプロイメントのステータスをすばやく把握できます。デプロイメントの Pod が Pending、Running、Succeeded、Failed、または Unknown 状態にあるかどうかを一目で確認できます。

![k8s-workload-overview](../images/k8s-deployment-overview.png)

* *Running:* Pod がデプロイされ、実行中の状態
* *Pending:* デプロイ待ち
* *Succeeded:* Pod がデプロイされ、ジョブを完了して終了
* *Failed:* Pod 内のコンテナが実行され、何らかのエラーを返した
* *Unknown:* Kubernetes が既知のステータスのいずれも報告していない（例えば、Pod の起動中または停止中の場合など）

名前がチャートの許容範囲より長い場合は、マウスをワークロード名の上に置くと展開できます。

特定のワークロードにフィルタリングするには、**k8s.workload.name** 列のワークロード名の横にある三点リーダー **...** をクリックし、ドロップダウンボックスから **Filter** を選択します:

![workload-add-filter](../images/workload-add-filter.png)

これにより、選択したワークロードがフィルターに追加されます。その後、**default** Namespace 内の単一のワークロードが表示されます:

![workload-add-filter](../images/heatmap-filter-down.png)

上記のヒートマップから、**default** Namespace 内の **splunk-otel-collector-k8s-cluster-receiver** を見つけて、四角形をクリックしてワークロードの詳細情報を確認します:

![workload-add-filter](../images/k8s-workload-detail.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
otel-collector の CPU request と CPU limit の単位は何ですか？
{{% /notice %}}

この時点で、Pod の情報にドリルダウンできますが、それはこのワークショップの範囲外です。

## 3. Navigator サイドバー

ワークショップの後半で、クラスターに Apache サーバーをデプロイします。これにより、**Navigator Sidebar** にアイコンが表示されます。

Kubernetes の Navigator では、Navigator サイドバーで依存するサービスとコンテナを追跡できます。Navigator サイドバーを最大限に活用するには、`service.name` という追加ディメンションを設定して、追跡するサービスを構成します。このワークショップでは、Apache を監視するための `extraDimensions` を Collector 設定で既に構成しています。例:

```yaml
extraDimensions:
  service.name: php-apache
```

Navigator サイドバーが展開し、以下の画像のように検出されたサービスへのリンクが追加されます:

![Pivotbar](../images/pivotbar.png)

これにより、Navigator 間を簡単に切り替えることができます。Apache サーバーインスタンスにも同様に Navigator サイドバーがあり、Kubernetes Navigator にすばやく戻ることができます。
