---
title: 6. APM Waterfall
weight: 6
---

**Trace Analyzer** から **Trace Waterfall** に移動しました。トレースは、同じトレース ID を共有するスパンの集合であり、アプリケーションとその構成サービスによって処理される一意のトランザクションを表します。

Splunk APM の各スパンは、単一の操作をキャプチャします。Splunk APM は、スパンに記録された操作がエラーとなった場合、スパンをエラースパンと見なします。

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* ウォーターフォール内の `paymentservice:grpc.hipstershop.PaymentService/Charge` スパンの隣にある {{% button style="red" %}}!{{% /button %}} をクリックします。

{{< tabs >}}
{{% tab title="質問" %}}
**スパンのメタデータに記録されているエラーメッセージとバージョンは何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
***Invalid Request* と `v350.10`** です。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

問題を引き起こしている **paymentservice** のバージョンを既に特定しているので、エラーに関してより詳細な情報を見つけられるか、やってみましょう。ここで **Related logs** が役立ちます。

![Related Logs](../images/apm-related-logs.png)

関連するコンテンツは、特定のメタデータによって実現されており、これにより、APM, Infrastructure Monitoring, Log Observer が Splunk Observability Cloud 内でフィルター条件を共有することで可能になっています。Related Logs が機能するには、ログに次のメタデータが必要です。

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

{{% notice title="Exercise" style="green" icon="running" %}}

* **Trace Waterfall** の一番下で **Logs (1)** と書かれた部分をクリックします。これにより、このトレースに紐づく **Related Logs** があることが分かります。
* ポップアップ内の **Logs for trace XXX** エントリをクリックすると、トレース全体と関係のあるログが **Log Observer** で表示されます。

{{% /notice %}}
