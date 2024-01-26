---
title: 6. APM ウォーターフォール
weight: 6
---

**トレースアナライザー** から **トレースウォーターフォール** に到着しました。トレースは、同じトレースIDを共有するスパンのコレクションであり、アプリケーションとその構成サービスによって処理される一意のトランザクションを表します。

Splunk APMの各スパンは、単一の操作をキャプチャします。Splunk APMは、スパンがエラーの結果となる操作をキャプチャする場合、スパンをエラースパンと見なします。

![Trace Waterfall](../images/apm-trace-waterfall.png)

{{% notice title="演習" style="green" icon="running" %}}

* ウォーターフォール内の `paymentservice:grpc.hipstershop.PaymentService/Charge` スパンの隣にある {{% button style="red" %}}!{{% /button %}} をクリックします。

{{< tabs >}}
{{% tab title="質問" %}}
**スパンメタデータに報告されているエラーメッセージとバージョンは何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**無効なリクエストと `v350.10`**。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

**paymentservice** のバージョンが問題を引き起こしていることが判明したので、エラーに関する詳細情報を見てみましょう。ここで **関連するログ** が役立ちます。

![関連するログ](../images/apm-related-logs.png)

関連するコンテンツは、Observability Cloud内でフィルターをパスするための特定のメタデータに依存しています。関連ログが機能するには、ログに次のメタデータが必要です。

* `service.name`
* `deployment.environment`
* `host.name`
* `trace_id`
* `span_id`

{{% notice title="演習" style="green" icon="running" %}}

* **トレースウォーターフォール** の一番下で **Logs (1)** と書かれた部分をクリックします。これにより、このトレースには **関連するログ** があることが強調されます。
* ポップアップ内の **Logs for trace XXX** エントリをクリックすると、**Log Observer** でトレース全体のログが開きます。

{{% /notice %}}
