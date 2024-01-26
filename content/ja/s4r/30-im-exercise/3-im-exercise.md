---
title: インフラストラクチャ演習 - パート3
linkTitle: パート3
weight: 3
---

{{% badge icon="clock" %}}10分{{% /badge %}}

さて、ナビゲーターの右側にある*Information Pane*や、底部の*Related Content Pane*など、UIの他の部分も見てみましょう。

まず、*Information Pane*を見てみましょう。このペインは、アラートと検出されたサービスの情報、および見ているオブジェクトに関連するメタデータを提供します。

![info pane](../images/k8s-info-pane.png)

メトリクスと一緒にメタデータが送信され、問題を調査する際に傾向を特定するのに非常に役立ちます。例として、特定のオペレーティングシステムでPodが失敗する場合が挙げられます。

{{% notice title="演習" style="green" icon="running" %}}

* メタデータからノードのオペレーティングシステムとアーキテクチャを特定できますか？

{{% /notice %}}

前の演習で見たように、これらのフィールドは、チャートやナビゲーターのビューを特定のメトリクスのサブセットに絞り込むために非常に役立ちます。

UIのもう1つの機能は**Related Content**です。

{{% notice title="Related Content" style="info" %}}

Splunk Observabilityのユーザーインターフェースは、現在アクティブに見ているものに関連する追加情報を表示しようとします。これの良い例は、Kubernetes Navigatorがこのノードで実行されているサービスに関する情報ペインの中に関連するコンテンツタイルを表示していることです。

{{% /notice %}}

**Information Pane**では、eコマースアプリケーションで使用される2つのデータベースのサービスが検出された2つのタイルが表示されるはずです。この**Related Content**を使用しましょう。

{{% notice title="演習" style="green" icon="running" %}}

* まず、開発名前空間に対するフィルターがアクティブでないことを確認します（フィルターペインから削除するには、**x**をクリックします）。開発名前空間にはデータベースがないためです。
* **Redis**タイルの上にホバーし、{{% button style="blue" %}}Goto all my Redis instances{{% /button %}}ボタンをクリックします。
* ナビゲータのビューがRedisインスタンス全体のビューに変わるはずです。
* クラスタで実行されているインスタンスを選択します（Redis Instancesペインの中の**redis-[ワークショップの名前]**という名前の青いリンクをクリックします）。
* これで、Redisインスタンスの情報だけが表示されるはずで、**Information Pane**もあります。
* 再びメタデータが表示されますが、UIは**Related Content**タイルに、このRedisサーバーがKubernetes上で実行されていることを示しています。
* これを確認するために**Kubernetes**タイルをクリックします。
* Kubernetes Navigatorに戻り、ページのトップにクラスタとノードの名前がすべて表示され、最初に見ていたK8sクラスタを見ていることを確認します。

{{% /notice %}}

これでSplunk Observability Cloudのツアーが完了しました。さあ、eコマースサイトを見て、お買い物をしましょう。
