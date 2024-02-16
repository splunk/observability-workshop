---
title: 2. APM Service Dashboard
weight: 2
---

{{% notice title="Service Dashboard" style="info" %}}

APM サービスダッシュボードは、サービス、エンドポイント、および Business Workflow のエンドポイントスパンから生成されたモニタリングメトリクセットに基づいて、リクエスト、エラー、および所要時間（**RED**）メトリクスを提供します。ダッシュボードを下にスクロールすると、基盤や Kubernetes に関連するメトリクスも表示され、インフラストラクチャに問題があるかどうかを判断するのに役立ちます。

{{% /notice %}}

![Service Dashboard](../images/apm-service-dashboard.png)

{{% notice title="Exercise" style="green" icon="running" %}}

* **Time** の枠 **(1)** を確認してください。ダッシュボードには、選択したアプリケーションの APM トレースによって取得された、処理にかかった時間に関するデータのみが表示されています（チャートは静的です）。
* **Time** の枠に **-1h** と入力し、Enter キーを押します。
* **Request rate**、**Request latency (p90)**、**Error rate** の Single Value チャートは 10 秒ごとに更新されており、引き続き多くのエラーが発生していることを示しています。
* これらのチャートはパフォーマンスの問題を迅速に特定するのに非常に役立ちます。このダッシュボードを使用してサービスの健康状態を監視したり、ダッシュボードを作成・構成する際のベースとして利用することができます。
* これらのチャートをいくつか、後の演習で使用したいと思います。
  * **Request rate** Single Value チャート(**2**)で **...** をクリックし、**Copy** を選択します。これにより、ページの右上(**3**)の部分に **1** が表示され、クリップボードにコピーされたチャートがあることを示しています。
  * **Request rate** の折れ線グラフ(**4**)では、**Add to clipboard** アイコンをクリックしてクリップボードに追加するか、**...** を使用して **Add to clipboard** を選択します。
* ページの右上(**3**)の部分に**2**が表示されていることを確認してください。
* それでは、エクスプロービューに戻りましょう。ブラウザの戻るボタンをクリックしてください。

{{% /notice %}}

![APM Explore](../images/apm-explore.png)

{{% notice title="Exercise" style="green" icon="running" %}}

{{< tabs >}}
{{% tab title="Question" %}}
**サービスマップで **paymentservice** の上にカーソルを合わせてください。ポップアップして表示されたサービスに関するチャートからどんなことがわかりますか？**
{{% /tab %}}
{{% tab title="Answer" %}}
**エラー率が非常に高いです。**
{{% /tab %}}
{{< /tabs >}}
{{% /notice %}}

![APM Service Chart](../images/apm-service-popup-chart.png)

このエラー率にパターンがあるかどうかを理解する必要があります。そのためには、**Tag Spotlight** が便利です。
