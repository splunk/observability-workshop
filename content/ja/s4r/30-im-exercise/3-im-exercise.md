---
title: インフラストラクチャ演習 - パート3
linkTitle: パート3
weight: 3
---

{{% badge icon="clock" %}}10分{{% /badge %}}

さて、Navigator の右側にある *Information Pane* や、底部の *Related Content Pane* など、UI の他の部分も見てみましょう。

まず、*Information Pane* を見てみましょう。このペインは、アラートと検出されたサービスの情報、および見ているオブジェクトに関連するメタデータを提供します。

![info pane](../images/k8s-info-pane.png)

メタデータはメトリクスと共に送信されます。問題を調査する際、問題の傾向を特定するのに非常に役立ちます。例として、特定のオペレーティングシステムで Pod が失敗する場合が挙げられます。

{{% notice title="Exercise" style="green" icon="running" %}}

* メタデータから、ノードのオペレーティングシステムとアーキテクチャを特定できますか？

{{% /notice %}}

前の演習で見たように、これらのフィールドは、チャートやナビゲーターのビューを特定のメトリクスのサブセットに絞り込む際に非常に便利です。

UI のもう1つの機能は **Related Content** です。

{{% notice title="Related Content" style="info" %}}

Splunk Observability のユーザーインターフェースは、現在アクティブに見ているものに関連する追加情報を表示しようとします。Kubernetes Navigator がこのノードで実行されていると検出されたサービスに関して情報ペインの中に関連するコンテンツタイルを表示しているのは、この機能の一つの例です。

{{% /notice %}}

**Information Pane** では、eコマースアプリケーションで使用される2つのデータベースのサービスが検出された2つのタイルが表示されるはずです。この **Related Content** を使用してみましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

* まず、開発用の名前空間に対するフィルターがアクティブでないことを確認します（フィルターペインから削除するには、**x**をクリックします）。開発用の名前空間にはデータベースがないためです。
* **Redis** タイルの上にマウスを移動させ、{{% button style="blue" %}}Go to all my Redis instances{{% /button %}} ボタンをクリックします。
* Navigator のビューが Redis インスタンス全体のビューに変わるはずです。
* クラスタで実行されているインスタンスを選択します（Redis Instances ペインの中の**redis-[ワークショップの名前]** という名前の青いリンクをクリックします）。
* これで、Redis インスタンスの情報だけが表示されるはずで、**Information Pane** もあります。
* 再びメタデータが表示されますが、UIは **Related Content** タイルに、この Redis サーバーが Kubernetes 上で実行されていることを示しています。
* これを確認するために **Kubernetes** タイルをクリックします。
* Kubernetes Navigator に戻り、ページのトップにクラスタとノードの名前がすべて表示され、最初に見ていた K8s クラスタを見ていることを確認します。

{{% /notice %}}

これで Splunk Observability Cloud のツアーが完了しました。さあ、eコマースサイトを見て、お買い物をしましょう。
