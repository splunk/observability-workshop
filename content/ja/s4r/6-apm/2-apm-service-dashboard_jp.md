---
title: 2. APM Service Dashboard
weight: 2
---

{{% notice title="Service Dashboard" style="info" %}}

APMサービスダッシュボードは、サービス、エンドポイント、およびビジネスワークフローのためのエンドポイントスパンから作成されたモニタリングメトリクセットに基づいて、リクエスト、エラー、および所要時間（**RED**）メトリクスを提供します。ダッシュボードを下にスクロールすると、基盤と関連するKubernetesメトリクスも表示され、基盤インフラストラクチャに問題があるかどうかを判断するのに役立ちます。

{{% /notice %}}

![Service Dashboard](../images/apm-service-dashboard.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* **Time**ボックス**(1)**を確認してください。ダッシュボードは選択したAPMトレースが完了するのにかかった時間に関連するデータのみを表示します（チャートは静的です）。
* **time**ボックスに**-1h**と入力し、Enterキーを押します。
* **Request rate**、**Request latency (p90)**、**Error rate**のSingle Valueチャートは、引き続き多くのエラーが発生していることを示すように、10秒ごとに更新されます。
* これらのチャートはパフォーマンスの問題を迅速に特定するのに非常に役立ちます。このダッシュボードを使用してサービスの健康状態を監視したり、カスタムの基盤として使用したりできます。
* これらのチャートのいくつかを後の演習で使用したいと思います：
  * **Request rate** Single Valueチャート(**2**)で**...**をクリックし、**Copy**を選択します。これにより、ページの右上に**3**の前に**1**が表示され、クリップボードにコピーされたチャートがあることが示されます。
  * **Request rate**の折れ線グラフ(**4**)では、**Add to clipboard**インジケータをクリックしてクリップボードに追加するか、**...**を使用して**Add to clipboard**を選択します。
* ページの右上に**3**の前に**2**が表示されていることに注意してください。
* それでは、エクスプロービューに戻りましょう。ブラウザのバックボタンをクリックしてください。

{{% /notice %}}

![APM Explore](../images/apm-explore.png)

{{% notice title="Exercise" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**サービスマップで**paymentservice**の上にカーソルを合わせると、ポップアップサービスチャートから何がわかりますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**エラー率が非常に高いです。**
{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

![APM Service Chart](../images/apm-service-popup-chart.png)

このエラー率にパターンがあるかどうかを理解する必要があります。そのためには、**Tag Spotlight**が便利です。
