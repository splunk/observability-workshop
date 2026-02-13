---
title: 3. APM Tag Spotlight
weight: 3
---

{{% notice title="演習" style="green" icon="running" %}}

- **paymentservice**のタグを表示するには、**paymentservice**をクリックし、右側の機能ペインの**Tag Spotlight**をクリックします（画面の解像度によっては下にスクロールする必要があるかもしれません）。
- **Tag Spotlight**に入ったら、フィルターアイコンから**Show tags with no values**チェックボックスがオフになっていることを確認してください。

{{% /notice %}}

![APM Tag Spotlight](../images/apm-tag-spotlight.png)

**Tag Spotlight**のビューは、チャートとカードの両方で設定可能です。デフォルトでは**リクエストとエラー**に設定されています。

また、カードに表示されるタグメトリクスを設定することも可能です。以下の任意の組み合わせを選択できます

- Requests
- Errors
- Root Cause errors
- P50 Latency
- P90 Latency
- P99 Latency

改めて、フィルターアイコンから**Show tags with no values**チェックボックスがオフになっていることを確認してください。

{{% notice title="演習" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="質問" %}}
**どのカードが問題を特定するタグを明らかにしていますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**「Version」カードです。`v350.10` に対するリクエスト数がエラー数と一致しています（つまり 100%）**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

**paymentservice**の問題を引き起こしているバージョンを特定したので、エラーについてさらに詳しい情報が見つかるか確認してみましょう。ページ上部の **← Tag Spotlight** をクリックして、サービスマップに戻ります。
