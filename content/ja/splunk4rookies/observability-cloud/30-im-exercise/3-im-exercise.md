---
title: Infrastructure Exercise - Part 3
linkTitle: Part 3
weight: 3
time: 10 minutes
---

ナビゲーターの右側にある *Information Pane* や下部の *Related Content Pane* など、UI のその他の部分も見ていきましょう。

まずは *Information Pane* を見てみます。このペインでは、アラート情報や検出されたサービスの情報、現在表示しているオブジェクトに関連するメタデータが提供されます。

![info pane](../images/k8s-info-pane.png)

メタデータはメトリクスとともに送信されており、問題を調査する際に傾向を特定するのに非常に役立ちます。例えば、特定のオペレーティングシステムにデプロイされた際にポッドが失敗するようなケースを特定できます。

{{% exercise title="Read the node metadata" %}}

* メタデータからノードのオペレーティングシステムとアーキテクチャを特定できますか？

{{% /exercise %}}

前の演習で見たように、これらのフィールドは、チャートやナビゲーターのビューを、関心のある特定のメトリクスのサブセットに絞り込むためにとても役立ちます。

UI のもう一つの機能が **Related content** です。

{{% notice title="Related Content" style="info" %}}

Splunk Observability のユーザーインターフェイスは、現在表示している内容に関連する追加情報を表示しようとします。
良い例として、Kubernetes Navigator では、このノード上で実行されているサービスについて、Information Pane に関連コンテンツのタイルが表示されます。

{{% /notice %}}

**Information Pane** には、検出されたサービスとして 2 つのタイルが表示されているはずです。これらは e-commerce アプリケーションで使用されている 2 つのデータベースです。この **Related Content** を活用してみましょう。

{{% exercise title="Drill into your Redis instance" %}}

* まず、Development ネームスペースにはデータベースが存在しないため、Development ネームスペースのフィルターが有効になっていないことを確認してください。（Filter Pane の **x** をクリックすれば削除できます）
* **Redis** タイルにマウスオーバーし、{{% button style="blue" %}}Goto all my Redis instances{{% /button %}} ボタンをクリックします。
* Navigator のビューが、Redis インスタンス全体のビューに切り替わります。
* 自分のクラスターで実行されているインスタンスを選択します。（Redis Instances ペイン内の **redis-[ワークショップ名]** という青いリンクをクリックします）
* これで自分の Redis Instance の情報のみが表示され、**Information Pane** も表示されるはずです。
* ここでもメタデータが表示されますが、**Related Content** タイルには、この Redis サーバーが Kubernetes 上で稼働するコンテナで実行されていることが示されています。
* **Kubernetes** タイルをクリックして、それを確認しましょう。
* コンテナレベルで Kubernetes Navigator に戻ったはずです。
* ページ上部にクラスター名とノード名がすべて表示されていることを確認し、最初に開始した K8s Cluster のビューに戻っていることを確認してください。

{{% /exercise %}}

これで Splunk Observability Cloud のツアーは完了です。次は e-commerce サイトを見て、買い物をしてみましょう。
