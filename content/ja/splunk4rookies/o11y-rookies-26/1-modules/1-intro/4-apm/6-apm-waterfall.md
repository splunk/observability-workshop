---
title: 6. APM ウォーターフォール
weight: 6
---

**Trace Waterfall** ビューは、トレース内のすべての span を階層的なタイムラインとして表示します。各 span は横棒として表示され、棒の長さがその所要時間を、位置が他の span との相対的な発生タイミングを示します。

トレースは、同じ trace ID を共有する span の集まりであり、アプリケーションとそれを構成するサービスによって処理される 1 つのトランザクションを表します。

span は、トレース内の 1 つの作業単位を表し、API 呼び出し、データベースクエリ、サービスリクエストなど、特定の操作に関する情報をキャプチャします。各 span には、オペレーション名、開始時刻、所要時間などのメタデータと、実行されている作業のコンテキストを提供する関連タグや属性が含まれます。

{{% exercise title="失敗している span を開く" %}}

* ウォーターフォール内の `paymentservice:grpc.hipstershop.PaymentService/Charge` span のいずれかの隣にある {{% button style="red"  %}}!{{% /button %}} をクリックします。

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{< tabs >}}
{{% tab title="質問" %}}
**Span Details に表示されているエラーメッセージとバージョンは何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**`Invalid request` と `v350.10`** です。
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
