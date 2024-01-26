---
title:  Infrastructure Navigators
linkTitle: 6.1 Infrastructure Navigators
weight: 2
---

**Infrastructure**をメインメニューでクリックすると、Infrastructureホームページが4つの異なるセクションで構成されています。

![Infra main](../images/infrastructure-main.png)

1. **オンボーディングパネル:** Splunk Infrastructure Monitoringを始めるためのトレーニングビデオとドキュメンテーションへのリンク。
2. **時間とフィルタパネル:** 時間ウィンドウ（トップレベルで構成不可）
3. **統合パネル:** Splunk Observability Cloudにメトリクスを送信しているすべてのテクノロジのリスト。
4. **タイルパネル:** 統合によって監視されているサービスの合計数（統合ごとに分割）

Infrastructureパネルを使用して、興味を持っているインフラストラクチャ/テクノロジを選択できます。それをやってみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* 統合パネルの**Containers**セクション（**3**）の下で、調査したいテクノロジとして**Kubernetes**を選択します。
* これにより、**K8s Nodes**と**K8s Workloads**の2つのタイルが表示されるはずです。
* 各タイルの下部には履歴グラフがあり、上部にはアラートの通知が表示されます。これらのタイルの追加情報全体は、インフラストラクチャの健康状態について良い概要を提供します。
* **K8s Nodes**タイルをクリックします。
* Kubernetesクラスターの1つ以上の表現が表示されます。
* {{% button %}}フィルタの追加{{% /button %}}ボタンをクリックします。 `k8s.cluster.name` と入力し、検索結果をクリックします。
* リストから **[WORKSHOPの名前]-k3s-cluster** を選択し、{{% button style="blue" %}}フィルタの適用{{% /button %}} ボタンをクリックします。

  ![cluster](../images/k8s-cluster.png)

* Kubernetes Navigatorでは、色を使用して健康状態を示します。ご覧の通り、2つのポッドまたはサービスが健康でなく、Failed状態にあります（**1**）。残りは健康で実行しています。これは共有されたKubernetes環境では一般的なことであり、ワークショップでそれを再現しました。
* サイドにあるタイルに注目してください。**Nodes dependencies**（**2**）の下に、特にMySQLとRedisのタイルがあります。これらは弊社のeコマースアプリケーションで使用されている2つのデータベースです。

{{% /notice %}}

{{% notice title="Node Dependencies" style="info" %}}

選択したノードで監視されている場合、UIにはそのノードで実行されているサービスが表示されます。

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* **Redis**タイルをクリックすると、**Redis instances**ナビゲータに移動します。**REDIS INSTANCE**の下で **redis-[WORKSHOPの名前]** をクリックします。
* これにより、**Redisインスタンス**に移動します。このナビゲータは、弊社のeコマースサイトのアクティブなRedisインスタンスからのメトリクスデータを含むチャートを表示します。
  ![redis](../images/redis-2.png)
{{< tabs >}}
{{% tab title="質問" %}}
**このビューでのInstance dependenciesタイルの名前を挙げられますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**はい、それはKubernetesのものです。**
{{% /tab %}}
{{< /tabs >}}

* タイルをクリックすると、Redisサービスを実行するPodが表示されるPodレベルでのKubernetes Navigatorに移動します。
* クラスターレベルに戻るには、画面の上部にある **Cluster**（**1**）のリンクをクリックします。

 ![node](../images/node-link.png)

{{% /notice %}}

これで**Splunk Observability Cloud**のツアーが完了しました。

さて、仮想の💶をお持ちいただき、eコマースサイト「Online Boutique」を見て、ショッピングをしてみましょう。
