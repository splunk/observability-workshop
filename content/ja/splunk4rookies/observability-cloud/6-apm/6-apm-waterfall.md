---
title: 6. APMウォーターフォール
weight: 6
---

**トレースアナライザー**から**トレースウォーターフォール**に到達しました。トレースは同じトレース ID を共有するスパンの集まりで、アプリケーションとその構成サービスによって処理される一意のトランザクションを表します。

Splunk APM の各スパンは、単一の操作をキャプチャします。Splunk APM は、スパンがキャプチャする操作がエラーになった場合、そのスパンをエラースパンとみなします。

![トレースウォーターフォール](../images/apm-trace-waterfall.png)

{{% notice title="演習" style="green" icon="running" %}}

- ウォーターフォール内の任意の`paymentservice:grpc.hipstershop.PaymentService/Charge`スパンの横にある{{% button style="red"  %}}!{{% /button %}}をクリックします。

{{< tabs >}}
{{% tab title="質問" %}}
**スパン詳細で報告されているエラーメッセージとバージョンは何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**`Invalid request`（無効なリクエスト）と`v350.10`です**。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
問題を引き起こしている**paymentservice**のバージョンを特定したので、エラーについてさらに詳しい情報が見つかるか確認してみましょう。ここで**関連ログ**の出番です。

関連コンテンツ(Related Contents)は、APM、インフラストラクチャモニタリング、および Log Observer が可観測性クラウド全体でフィルターを渡すことを可能にする特定のメタデータに依存しています。関連ログが機能するためには、ログに以下のメタデータが必要です：

- `service.name`
- `deployment.environment`
- `host.name`
- `trace_id`
- `span_id`

{{% notice title="演習" style="green" icon="running" %}}

- **トレースウォーターフォール**の一番下で**Logs (1)**をクリックします。これは、このトレースに**関連ログ**があることを示しています。
- ポップアップの**Logs for trace xxx**（トレース xxx のログ）エントリをクリックすると、**Log Observer**で完全なトレースのログが開きます。

{{% /notice %}}

![関連ログ](../images/apm-related-logs.png)

次に、ログのエラーについてさらに詳しく調べてみましょう。
