---
title: Infrastructure Navigators
linkTitle: 6.1 Infrastructure Navigators
weight: 2
hidden: true
---

メインメニューの**Infrastructure**をクリックすると、Infrastructure ホームページが表示されます。このページは 4 つの明確なセクションで構成されています。

![Infra main](../images/infrastructure-main.png)

1. **オンボーディングペイン:** Splunk Infrastructure Monitoring の使用を開始するためのトレーニングビデオとドキュメントへのリンク。
2. **時間とフィルターペイン:** 時間ウィンドウ（トップレベルでは設定不可）
3. **インテグレーションペイン:** Splunk Observability Cloud にメトリクスを送信しているすべてのテクノロジーのリスト。
4. **タイルペイン:** インテグレーション別に分類された、監視対象サービスの総数。

Infrastructure ペインを使用して、関心のあるインフラストラクチャ/テクノロジーを選択できます。今すぐやってみましょう。

{{% notice title="演習" style="green" icon="running" %}}

* インテグレーションペイン **(3)** の**Containers**セクションで、調査したいテクノロジーとして**Kubernetes**を選択します。
* **K8s Nodes**と**K8s Workloads**の 2 つのタイルが表示されるはずです。
* 各タイルの下部には履歴グラフがあり、上部には発生したアラートの通知が表示されます。すべてのタイルにわたって、各タイルのこの追加情報により、インフラストラクチャの健全性の良好な概要を把握できます。
* **K8s Nodes**タイルをクリックします。
* 1 つ以上の Kubernetes クラスターの表示が提示されます。
* {{% button %}}Add filters{{% /button %}} ボタンをクリックします。`k8s.cluster.name` と入力し、検索結果をクリックします。
* リストから**[NAME OF WORKSHOP]-k3s-cluster**を選択し、{{% button style="blue" %}}Apply Filter{{% /button %}} ボタンをクリックします。

  ![cluster](../images/k8s-cluster.png)

* Kubernetes Navigator は色を使用して健全性を示します。ご覧のように、2 つの Pod またはサービスが異常で Failed 状態にあります **(1)**。残りは健全で実行中です。これは共有 Kubernetes 環境では珍しくないため、ワークショップ用に再現しました。
* サイドのタイル、**Nodes dependencies** **(2)** の下、特に MySQL と Redis のタイルに注目してください。これらは e コマースアプリケーションで使用される 2 つのデータベースです。

{{% /notice %}}

{{% notice title="Node Dependencies" style="info" %}}

UI は、OpenTelemetry Collector によって監視されるように設定されている場合、選択したノードで実行されているサービスを表示します。

{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

* **Redis**タイルをクリックすると、**Redis instances** navigator に移動します。**REDIS INSTANCE**の下の**redis-[NAME OF WORKSHOP]**をクリックします。
* **Redis instance**に移動します。この navigator は、e コマースサイトのアクティブな Redis インスタンスからのメトリクスデータを含むチャートを表示します。
  ![redis](../images/redis-2.png)
{{< tabs >}}
{{% tab title="質問" %}}
**このビューの Instance dependencies タイルの名前を挙げることができますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**はい、Kubernetes 用のタイルがあります。**
{{% /tab %}}
{{< /tabs >}}

* タイルをクリックすると、Kubernetes Navigator に戻ります。今度は Pod レベルで、Redis サービスを実行している Pod が表示されます。
* クラスターレベルに戻るには、画面上部の**Cluster** **(1)** リンクをクリックするだけです。

![node](../images/node-link.png)

{{% /notice %}}

これで**Splunk Observability Cloud**のツアーは完了です。

ここで、仮想の 💶 を差し上げます。e コマースサイト「Online Boutique」に行って、ショッピングをしましょう。
