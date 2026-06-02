---
title: 6. APM Waterfall
weight: 6
---

**Trace Analyzer** から **Trace Waterfall** に到達しました。トレースとは、同じトレース ID を共有するスパンの集合体であり、アプリケーションとそれを構成するサービスによって処理される 1 つのユニークなトランザクションを表します。

Splunk APM の各スパンは、単一の操作をキャプチャします。Splunk APM は、スパンがキャプチャした操作がエラーになった場合、そのスパンをエラースパンとみなします。

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{% exercise title="失敗したスパンを開く" %}}

* Waterfall 内の任意の `paymentservice:grpc.hipstershop.PaymentService/Charge` スパンの隣にある {{% button style="red"  %}}!{{% /button %}} をクリックします。

{{< tabs >}}
{{% tab title="質問" %}}
**Span Details に報告されているエラーメッセージとバージョンは何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**`Invalid request` と `v350.10`** です。
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
問題の原因となっている **paymentservice** のバージョンを特定できたので、次はエラーに関する詳細情報を確認していきましょう。ここで活躍するのが **Related Logs** です。

Related Content は、APM、Infrastructure Monitoring、Log Observer が Observability Cloud 全体でフィルターを受け渡せるようにする特定のメタデータに依存しています。Related Logs を機能させるには、ログに以下のメタデータが含まれている必要があります。

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

{{% exercise title="APM から Related Logs にジャンプする" %}}

* **Trace Waterfall** の一番下で **Logs (1)** をクリックします。これにより、このトレースに **Related Logs** があることが強調表示されます。
* ポップアップで **Logs for trace xxx** のエントリをクリックすると、**Log Observer** でこのトレース全体のログが開きます。

{{% /exercise %}}

![Related Logs](../images/apm-related-logs.png)

次に、ログでエラーに関する詳細を調べていきましょう。
