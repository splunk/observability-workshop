---
title: 3. インスタンスを選択して Navigator を開く
weight: 3
---

対象となるインスタンスが見つかったら、それをクリックして **Navigator** を開きます。Navigator はインスタンス固有のビューで、このワークショップの残りの部分で主に使用する画面です。

Navigator の上部には5つのタブがあります:

- **Queries** — このインスタンスで実行されている上位の SQL ステートメントです。
- **Query samples** — パラメータや実行プランを含む、キャプチャされた個々の実行です。
- **Query metrics** — クエリごとの経時的なトレンドです。
- **Dependencies** — このインスタンスを呼び出しているアプリケーションとホストです。
- **Metadata** — エンジンバージョン、ホスト、および設定の詳細です。

インスタンスに対するアクティブなアラートは、右上隅に表示されます。

{{% notice title="演習" style="green" icon="running" %}}

- **Overview** ページに戻り、チャートを **Duration** に切り替えて、最も遅いインスタンスを対象にします。
- インスタンスリストで、**上位のインスタンス**の名前をクリックして開きます。
- そのインスタンスの **Navigator** ビューが表示されます。
- 上部にある5つのタブ **(1)** と右上のアラートエリア **(2)** を確認してください。

<!-- TODO screenshot: Navigator view for an instance with the five tabs annotated (1) and the alerts area annotated (2) -->
![Navigator ビュー](../images/navigator.png)

{{< tabs >}}
{{% tab title="質問" %}}
**Navigator を開いたとき、デフォルトで選択されているタブはどれですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**Queries** — Navigator はトップクエリビューで開きます。これは、概要からの調査がほぼ常にここから続行されるためです。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
