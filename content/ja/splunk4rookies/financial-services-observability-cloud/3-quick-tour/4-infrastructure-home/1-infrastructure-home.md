---
title: Infrastructure Navigators
linkTitle: 4.1 Infrastructure Navigators
weight: 2
hidden: true
---

メインメニューの **Infrastructure** をクリックすると、Infrastructure ホームページが表示されます。このページは4つのセクションで構成されています。

![Infra main](../images/infrastructure-main.png)

1. **Onboarding Pane:** Splunk Infrastructure Monitoring を使い始めるためのトレーニングビデオとドキュメントへのリンクです。
2. **Time & Filter Pane:** 時間枠（トップレベルでは設定変更できません）
3. **Integrations Pane:** Splunk Observability Cloud にメトリクスを送信しているすべての技術のリストです。
4. **Tile Pane:** インテグレーションごとに分類された、監視されているサービスの総数です。

Infrastructure ペインを使用して、関心のあるインフラストラクチャや技術を選択できます。実際にやってみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* Integrations Pane **(3)** の **Containers** セクションで、調べたい技術として **Kubernetes** を選択します。
* **K8s Nodes** と **K8s Workloads** の2つのタイルが表示されるはずです。
* 各タイルの下部には履歴グラフがあり、上部には発生したアラートの通知が表示されます。すべてのタイルにわたって、これらの追加情報によりインフラストラクチャの健全性の概要を把握できます。
* **K8s Nodes** タイルをクリックします。
* 1つ以上の Kubernetes クラスターの表現が表示されます。
* {{% button %}}Add filters{{% /button %}} ボタンをクリックします。`k8s.cluster.name` と入力し、検索結果をクリックします。
* リストから **[NAME OF WORKSHOP]-k3s-cluster** を選択し、{{% button style="blue" %}}Apply Filter{{% /button %}} ボタンをクリックします。

  ![cluster](../images/k8s-cluster.png)

* Kubernetes Navigator は色を使って健全性を示します。ご覧のとおり、2つの Pod またはサービスが異常で Failed 状態になっています **(1)**。残りは正常に稼働しています。これは共有 Kubernetes 環境では珍しいことではないため、ワークショップ用に再現しました。
* 横にあるタイル、特に **Nodes dependencies** **(2)** の下にある MySQL と Redis のタイルに注目してください。これらは e コマースアプリケーションで使用されている2つのデータベースです。

{{% /notice %}}

{{% notice title="Node Dependencies" style="info" %}}

選択したノードで実行されているサービスは、OpenTelemetry Collector によって監視されるように設定されている場合、UI に表示されます。

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* **Redis** タイルをクリックすると、**Redis instances** ナビゲーターに移動します。**REDIS INSTANCE** の下にある **redis-[NAME OF WORKSHOP]** をクリックします。
* **Redis instance** 画面が表示されます。このナビゲーターには、e コマースサイトのアクティブな Redis インスタンスからのメトリクスデータを含むチャートが表示されます。
  ![redis](../images/redis-2.png)
{{< tabs >}}
{{% tab title="Question" %}}
**このビューの Instance dependencies タイルの名前を言えますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**はい、Kubernetes 用のタイルがあります。**
{{% /tab %}}
{{< /tabs >}}

* タイルをクリックすると、Kubernetes Navigator に戻ります。今度は Pod レベルで、Redis サービスを実行している Pod が表示されます。
* クラスターレベルに戻るには、画面上部の **Cluster** **(1)** リンクをクリックするだけです。

![node](../images/node-link.png)

{{% /notice %}}

これで **Splunk Observability Cloud** のツアーは完了です。

仮想の 💶 を受け取って、e コマースサイト「Online Boutique」でショッピングをしてみましょう。
