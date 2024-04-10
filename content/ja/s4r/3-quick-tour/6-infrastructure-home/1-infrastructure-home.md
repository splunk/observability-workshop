---
title:  Infrastructure Navigators
linkTitle: 6.1 Infrastructure Navigators
weight: 2
---

**Infrastructure** をメインメニューでクリックします。Infrastructure ホームページは4つの異なるセクションで構成されています。

![Infra main](../images/infrastructure-main.png)

1. **オンボーディングパネル:** Splunk Infrastructure Monitoring を始める際に参照するトレーニングビデオとドキュメンテーションへのリンク。
2. **時間とフィルタパネル:** 時間ウィンドウ（一覧画面上では設定変更できません）
3. **Integration パネル:** Splunk Observability Cloud にメトリクスを送信しているすべてのテクノロジのリスト。
4. **タイルパネル:** Integration によって監視されているサービスの合計数（Integration 別に表示）

Infrastructure パネルを使用して、興味のあるインフラストラクチャ/テクノロジーを選択できます。やってみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* Integration パネルの **Containers** セクション（**3**）にある、**Kubernetes** を調査対象のテクノロジーとして選択します。
* **K8s Nodes** と **K8s Workloads** の2つのタイルが表示されるはずです。
* 各タイルの下部には過去の推移を表すグラフがあり、上部には現在発生しているアラートの数が表示されます。これらの追加情報は全てのタイルに表示されており、インフラストラクチャの健全性を概要として確認するのに役立つはずです。
* **K8s Nodes** タイルをクリックします。
* Kubernetes クラスターが1つ以上の表示されます。
* 次に {{% button %}}Add filters{{% /button %}} ボタンをクリックします。 `k8s.cluster.name` と入力し、検索結果をクリックします。
* リストから **[WORKSHOPの名前]-k3s-cluster** を選択し、{{% button style="blue" %}}Apply Filter{{% /button %}} ボタンをクリックします。

  ![cluster](../images/k8s-cluster.png)

* Kubernetes Navigator では、健全性を色で示します。ご覧の通り、2つの Pod またはサービスが健全ではなく、Failed 状態にあります（**1**）。残りは問題なく動いています。これは共用の Kubernetes 環境では一般的に発生することがあるもので、ワークショップではこれを再現しています。
* サイドにあるタイルに注目してください。**Nodes dependencies**（**2**）の下に、MySQL と Redis のタイルが表示されています。これらは我々のeコマースアプリケーションで使用されている2つのデータベースです。

{{% /notice %}}

{{% notice title="Node Dependencies" style="info" %}}

OpenTelemetry Collector によるモニタリングが構成されている場合、選択したノードで実行されているサービスが UI 上に表示されます。

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* **Redis** タイルをクリックすると、**Redis instances** ナビゲータに移動します。**REDIS INSTANCE** の下で **redis-[WORKSHOPの名前]** をクリックします。
* これにより、**Redis instance** に移動します。このナビゲータは、我々のeコマースサイトのアクティブな Redis インスタンスからのメトリクスデータを含むチャートを表示します。
  ![redis](../images/redis-2.png)
{{< tabs >}}
{{% tab title="質問" %}}
**このビューでの Instance dependencies タイルの名前を挙げられますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**はい、Kubernetes に関するタイルです。**
{{% /tab %}}
{{< /tabs >}}

* タイルをクリックすると、Redis サービスを実行する Pod が表示される Pod レベルでの Kubernetes Navigator に移動します。
* クラスターレベルに戻るには、画面の上部にある **Cluster**（**1**）のリンクをクリックします。

 ![node](../images/node-link.png)

{{% /notice %}}

これで **Splunk Observability Cloud** のツアーが完了しました。

さて、eコマースサイト「Online Boutique」にアクセスし、仮想のクレジット💶を使ってショッピングをしてみましょう。
