---
title: 6. APM Waterfall
weight: 6
---

**Trace Waterfall** ビューは、トレース内のすべてのスパンを階層的なタイムラインとして表示します。各スパンは水平バーとして表示され、バーの長さがその所要時間を、位置が他のスパンに対するいつ発生したかを示します。

トレースとは、同じトレース ID を共有するスパンの集合であり、アプリケーションとそれを構成するサービスによって処理される一意のトランザクションを表します。

スパンとは、トレース内の単一の作業単位を表すもので、API コール、データベースクエリ、サービスリクエストなどの特定の操作に関する情報をキャプチャします。各スパンには、操作名、開始時刻、所要時間、および実行されている作業に関するコンテキストを提供する関連タグや属性などのメタデータが含まれます。

{{% exercise title="Open the failing span" %}}

* Waterfall 内の `paymentservice:grpc.hipstershop.PaymentService/Charge` スパンのいずれかの隣にある {{% button style="red"  %}}!{{% /button %}} をクリックします。

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{< tabs >}}
{{% tab title="Question" %}}
**Span Details に報告されているエラーメッセージとバージョンは何ですか?**
{{% /tab %}}
{{% tab title="Answer" %}}
**`Invalid request` と `v350.10`**。
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
