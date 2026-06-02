---
title:  Infrastructure Navigators
linkTitle: 6.1 Infrastructure Navigators
weight: 2
hidden: true
---

メインメニューで **Infrastructure** をクリックします。Infrastructure Home ページは 4 つの異なるセクションで構成されています。

![Infra main](../images/infrastructure-main.png)

1. **Onboarding Pane:** Splunk Infrastructure Monitoring を始めるためのトレーニング動画とドキュメントへのリンク。
2. **Time & Filter Pane:** 時間ウィンドウ（トップレベルでは設定不可）。
3. **Integrations Pane:** Splunk Observability Cloud にメトリクスを送信しているすべてのテクノロジーのリスト。
4. **Tile Pane:** 監視中のサービスの総数を、インテグレーションごとに分類して表示します。

Infrastructure ペインを使用して、注目したいインフラストラクチャ／テクノロジーを選択できます。早速やってみましょう。

{{% exercise title="Explore the Kubernetes navigator" %}}

* Integrations Pane **(3)** の **Containers** セクションで、調査したいテクノロジーとして **Kubernetes** を選択します。
* **K8s Nodes** と **K8s Workloads** という 2 つのタイルが表示されるはずです。
* 各タイルの下部には履歴グラフが表示され、上部にはトリガーされたアラートの通知が表示されます。すべてのタイルにわたるこれらの追加情報により、インフラストラクチャの健全性の概要を把握できます。
* **K8s Nodes** タイルをクリックします。
* Kubernetes クラスターを表す 1 つまたは複数の表現が表示されます。
* {{% button %}}Add filters{{% /button %}} ボタンをクリックします。`k8s.cluster.name` と入力し、検索結果をクリックします。
* リストから **[NAME OF WORKSHOP]-k3s-cluster** を選択し、{{% button style="blue" %}}Apply Filter{{% /button %}} ボタンをクリックします。

  ![cluster](../images/k8s-cluster.png)

* Kubernetes Navigator は色を使って健全性を示します。ご覧のとおり、2 つの pod またはサービスが不健全で Failed 状態 **(1)** にあります。残りは健全に稼働中です。共有 Kubernetes 環境ではこれは珍しいことではないため、ワークショップでもその状況を再現しています。
* サイドにあるタイル、特に **Nodes dependencies** **(2)** の下にある MySQL と Redis のタイルに注目してください。これらは e コマースアプリケーションで使用される 2 つのデータベースです。

{{% /exercise %}}

{{% notice title="Node Dependencies" style="info" %}}

選択したノード上で動作しているサービスは、OpenTelemetry Collector で監視するように構成されている場合に UI に表示されます。

{{% /notice %}}

{{% exercise title="Open the Redis instance navigator" %}}

* **Redis** タイルをクリックすると、**Redis instances** ナビゲーターに遷移します。**REDIS INSTANCE** の下で **redis-[NAME OF WORKSHOP]** をクリックします。
* これにより、**Redis instance** に移動します。このナビゲーターには、e コマースサイトで稼働中の Redis インスタンスからのメトリクスデータがチャートで表示されます。
  ![redis](../images/redis-2.png)
{{< tabs >}}
{{% tab title="Question" %}}
**このビューの Instance dependencies タイルの名前は何ですか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**はい、Kubernetes 用のものが 1 つあります。**
{{% /tab %}}
{{< /tabs >}}

* タイルをクリックすると、Kubernetes Navigator に戻ります。今度は Pod レベルで、Redis サービスを実行している Pod が表示されます。
* Cluster レベルに戻るには、画面上部の **Cluster** **(1)** リンクをクリックするだけです。

![node](../images/node-link.png)

{{% /exercise %}}

これで **Splunk Observability Cloud** のツアーは完了です。

ここで仮想の 💶 を受け取って、e コマースサイトの「Online Boutique」を見に行き、ショッピングをしてみましょう。
