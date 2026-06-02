---
title: Dimension、Properties、Tags
weight: 3
description: Dimension と Properties はどう違うのか、どちらをいつ使うべきかを解説します。
draft: false
---

## メトリクスにコンテキストを付与する

よく話題になる議論のひとつに、Dimensions と Properties のどちらを使うべきかという問題があります。それぞれの説明から始めるのではなく、まずはこれらをどのように使い、どのような点が共通しているのかを理解した上で、両者の違いやそれぞれを使うべき理由の例を見ていくのが理にかなっています。

## Dimensions と Properties の共通点

最もシンプルに言えば、どちらもメトリクスにコンテキストを加えるためのメタデータの `key:value` ペアです。メトリクス自体は、`cpu.utilization` のような標準的なインフラストラクチャメトリクスであれ、受信した API コール数のようなカスタムメトリクスであれ、私たちが実際に計測したいものです。

`cpu.utilization` メトリクスで 50% という値を受け取っても、それがどこから来たのか、その他のコンテキストがわからなければ、ただの数字でしかなく、私たちにとって有用ではありません。少なくとも、それがどのホストから来たものなのかを知る必要があります。

最近では、個々のホストの性能や使用率よりも、クラスタやデータセンター全体の性能や使用率の方が重要視されることが多くなっています。そのため、ホストのクラスタ全体での平均 `cpu.utilization`、同じサービスを実行している他のホストと比較して特定のホストの `cpu.utilization` が外れ値になっている場合、あるいは異なる環境間の平均 `cpu.utilization` の比較といったことに、より関心が向けられます。

このように `cpu.utilization` メトリクスをスライス、集約、グループ化できるようにするには、受信した `cpu.utilization` メトリクスに、ホストが属するクラスタ、ホスト上で実行されているサービス、そしてそのホストが属する環境などの追加のメタデータが必要になります。このメタデータは、dimension または property の `key:value` ペアの形で表現できます。

たとえば、ダッシュボードにフィルタを適用したり、分析実行時に Group by 関数を使用したりする際には、property または dimension のいずれかを使用できます。

## それでは、Dimensions と Properties はどう違うのでしょうか?

Dimensions はメトリクスがインジェストされる時点でメトリクスとともに送信されるのに対し、Properties はインジェスト後にメトリクスや dimension に対して適用されます。これは、データポイント（メトリクスの個々の報告値）を一意にするために必要なメタデータ、たとえば `cpu.utilization` の値がどのホストから来ているのかといった情報は、dimension にする必要があるということです。メトリクス名 + dimensions が MTS（metric time series）を一意に定義します。

例: 特定のホスト（server1）から送信される `cpu.utilization` メトリクスに dimension `host:server1` が付与されている場合、これは一意のタイムシリーズと見なされます。10 台のサーバーがそれぞれそのメトリクスを送信している場合、10 個のタイムシリーズが存在し、各タイムシリーズはメトリクス名 `cpu.utilization` を共有し、dimension の key-value ペア（host:server1、host:server2…host:server10）によって一意に識別されます。

ただし、サーバー名が環境全体ではなくデータセンター内でのみ一意である場合は、データセンターの場所を表す 2 つ目の dimension `dc` を追加する必要があります。これにより、可能な MTS の数は倍になります。受信される cpu.utilization メトリクスは、2 組の dimension の key-value ペアによって一意に識別されることになります。

cpu.utilization に dc:east と host:server1 を組み合わせたものは、cpu.utilization に dc:west と host:server1 を組み合わせたものとは異なるタイムシリーズになります。

## Dimensions は不変、Properties は可変

前述のとおり、メトリクス名 + dimensions が一意の MTS を構成します。したがって、dimension の値が変更されると、メトリクス名 + dimension 値の新しい一意の組み合わせとなり、新しい MTS が作成されます。

一方、Properties はインジェスト後にメトリクス（または dimension）に適用されます。メトリクスに property を適用すると、それはそのメトリクスが含まれるすべての MTS に伝播して適用されます。あるいは、host:server1 のような dimension に property を適用すると、そのホストからのすべてのメトリクスにそれらの property がアタッチされます。property の値を変更すると、その property がアタッチされているすべての MTS に対して値の更新が伝播します。なぜこれが重要なのでしょうか? それは、property の履歴値を保持したい場合は、それを dimension にする必要があるということを意味するからです。

例: 私たちはアプリケーション上でカスタムメトリクスを収集しています。1 つのメトリクスは latency で、これはアプリケーションへのリクエストのレイテンシをカウントします。customer という dimension があるので、レイテンシを顧客ごとに並べ替え、比較できます。さらに application version も追跡したいと考えます。これにより、顧客が使用しているバージョンごとにアプリケーションの latency を並べ替えて比較できます。そこで、customer dimension にアタッチする version という property を作成します。当初、すべての顧客がアプリケーションのバージョン 1 を使用しているため、version:1 となります。

その後、一部の顧客がアプリケーションのバージョン 2 を使用するようになり、それらの顧客については property を version:2 に更新します。それらの顧客の version property の値を更新すると、その変更はその顧客のすべての MTS に伝播します。これにより、それらの顧客がかつて version 1 を使用していたという履歴は失われます。そのため、version 1 と version 2 の latency を過去の期間にわたって比較したいと思っても、正確なデータは得られません。この場合、メトリクスのタイムシリーズを一意にするためにアプリケーションの version は必要ありませんが、履歴値が重要なので version は dimension にする必要があります。

## では、いつ Property を dimension の代わりに使うべきでしょうか?

最初の理由は、メトリクスにアタッチしたいメタデータがあるものの、インジェストの時点ではそれが分からない場合です。
2 つ目の理由は、ベストプラクティスとして、dimension にする必要がないものは property にすべきだという点です。なぜでしょうか?
理由のひとつは、現在、分析ジョブまたはチャートのレンダリングごとに 5K MTS という制限があり、dimension が増えれば増えるほど MTS が増えてしまうからです。Properties は完全に自由形式なので、MTS 数を増やすことなく、必要なだけメトリクスや dimension に情報を追加できます。

Dimensions はすべてのデータポイントとともに送信されるため、dimension が多ければ多いほど、送信されるデータ量も増えます。クラウドプロバイダーがデータ転送に対して課金している場合、これはコスト増加につながる可能性があります。

property にすべきものの良い例は、追加のホスト情報です。machine_type、processor、os などの情報を見られるようにしたい場合、これらを dimension にしてホストからのすべてのメトリクスとともに送信するのではなく、property にして host dimension にアタッチすることができます。

例: host:server1 に対して property machine_type:ucs、processor:xeon-5560、os:rhel71 を設定します。dimension host:server1 を持つメトリクスが入ってくるたびに、上記のすべての property が自動的に適用されます。

property のユースケースの他の例としては、各サービスのエスカレーション連絡先や、各顧客の SLA レベルを知りたい場合などが挙げられます。これらの項目はメトリクスを一意に識別するために必要ではなく、また履歴値も気にしないため、property にすることができます。これらの property を service dimension や customer dimension に追加すれば、それらの dimension を持つすべてのメトリクスや MTS に適用されます。

## Tags はどうでしょうか?

Tags は、メトリクスにコンテキストを与えたり、メトリクスを整理したりするのに使用できる 3 つ目のタイプのメタデータです。dimensions や properties とは異なり、tags は key:value ペアではありません。Tags はラベルやキーワードのようなものと考えることができます。Properties と同様に、Tags はインジェスト後に UI のカタログ経由、または API 経由でプログラム的にデータに適用されます。Tags は Metrics、Dimensions、または Detectors などの他のオブジェクトに適用できます。

## どこで Tags を使うべきでしょうか?

Tags は、tags とオブジェクトの間に多対一の関係、または tag と適用先オブジェクトの間に一対多の関係が必要な場合に使用します。本質的には関連付けられていないかもしれないメトリクスをグループ化する際に役立ちます。

例として、複数のアプリケーションを実行するホストがあるとします。各アプリケーション用の tag（ラベル）を作成し、各ホストに複数の tag を適用して、そのホストで実行されているアプリケーションをラベル付けすることができます。

例: Server1 は 3 つのアプリケーションを実行しています。app1、app2、app3 という tag を作成し、3 つすべての tag を dimension host:server1 に適用します。

上の例をさらに拡張して、アプリケーションからもメトリクスを収集していると仮定しましょう。作成した tag を、アプリケーション自体から送信されてくるメトリクスに対しても適用できます。tag に基づいてフィルタリングできるため、アプリケーション単位でフィルタリングしつつ、アプリケーションと関連ホストのメトリクスの両方を含む全体像を把握できます。

例: App1 は dimension service:application1 でメトリクスを送信しています。dimension service:application1 に tag app1 を適用します。これにより、チャートやダッシュボードで tag app1 でフィルタリングできるようになります。

tag のもう 1 つのユースケースは、可能な値が 1 つしかないバイナリ状態の場合です。たとえば、カナリアテストを実施しており、カナリアデプロイを行う際に新しいコードを受け取ったホストにマークを付けて、そのメトリクスを簡単に識別し、新しいコードを受け取らなかったホストとパフォーマンスを比較できるようにしたいとします。値が「canary」という 1 つだけなので、key:value ペアは必要ありません。

tag に対してはフィルタリングはできますが、groupBy 関数は使用できないことに注意してください。groupBy 関数は key:value ペアの key 部分を指定して実行され、その key ペアの値ごとに結果がグループ化されます。

## 追加情報

カスタムメトリクスに対する dimension の送信については、使用するライブラリの Client Libraries ドキュメントをご確認ください。

API 経由でメトリクスや dimension に property や tag を適用する方法については、`/metric/:name` および `/dimension/:key/:value` の API ドキュメントをご覧ください。

UI のメタデータカタログから property や tag を追加・編集する方法については、[Search the Metric Finder and Metadata catalog](https://docs.splunk.com/Observability/metrics-and-metadata/metrics-finder-metadata-catalog.html#use-the-metadata-catalog) の **Add or edit metadata** セクションを参照してください。
