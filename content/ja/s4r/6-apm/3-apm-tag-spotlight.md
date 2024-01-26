---
title: 3. APM タグスポットライト
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

* **paymentservice**のタグを表示するには、**paymentservice**をクリックしてから右側の機能ペインで**Tag Spotlight**をクリックします（画面解像度によってはスクロールが必要な場合があります）。
* **Tag Spotlight**に入ったら、トグルスイッチ**Show tags with no values**がオフになっていることを確認してください。

{{% /notice %}}

![APM タグスポットライト](../images/apm-tag-spotlight.png)

**Tag Spotlight**には、2つの表示モードがあります。デフォルトは**Request/Errors**で、もう1つは**Latency**です。

Request/Errorチャートでは、リクエストの合計数、エラーの合計数、およびルート原因のエラーが表示されます。Latencyチャートでは、p50、p90、およびp99のレイテンシが表示されます。これらの値は、Splunk APMがインデックス化された各スパンタグに対して生成するトラブルシューティングメトリクセット（TMS）に基づいています。これらはREDメトリクス（リクエスト、エラー、および所要時間）として知られています。

{{% notice title="Exercise" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**どのチャートが問題を特定するためのタグを公開していますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
** *version* チャートです。`v350.10`に対するリクエストの数はエラーの数と一致しています。**
{{% /tab %}}
{{< /tabs >}}

* これで、問題を引き起こしている**paymentservice**のバージョンを特定したので、エラーに関する詳細情報を見つけることができるかどうかを確認してみましょう。ページの上部にある**← Tag Spotlight**をクリックしてService Mapに戻ります。

{{% /notice %}}
