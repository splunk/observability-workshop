---
title: Locustでトラフィックを発生させる
weight: 3
isCJKLanguage: true
---

## 1. トラフィックを発生させる

Online Boutique のデプロイメントには、Locust が動作するコンテナが含まれており、これを使用してウェブサイトに対する負荷トラフィックを生成し、メトリクス、トレース、スパンを生成することができます。

Locust は、EC2インスタンスのIPアドレスの82番ポートで利用できます。ウェブブラウザで新しいタブを開き、 `http://{==EC2-IP==}:82/` にアクセスすると、Locust が動作しているのが確認できます。

![Locust](../../../images/locust.png)

**Spawn rate** を 2 に設定し、**Start Swarming** をクリックすると、アプリケーションに緩やかな負荷がかかり続けます。

![Spawn Rate](../../../images/locust-spawn-rate.png)

![Statistics](../../../images/locust-statistics.png)

---

それでは、**Dashboards → APM Services → Service** を開きましょう。

このためには、アプリケーションの Environment 名を知る必要があります。このワークショップでは、`{==hostname==}-apm-env` のような Environment 名で定義されています。

ホスト名を調べるには、AWS/EC2インスタンス上で以下のコマンドを実行します:

{{< tabpane >}}
  {{< tab header="Echo Hostname" lang="bash" >}}
    echo $(hostname)-apm-env
  {{< /tab >}}
  {{< tab header="Output Example" lang= "bash" >}}
    bdzx-apm-env
  {{< /tab >}}
{{< /tabpane >}}

前のステップで見つけた Environment を選択し、「frontend」サービスを選択し、時間を「Past 15 minutes」に設定します。

![APM Dashboard](../../../images/online-boutique-service-dashboard.png)

この自動生成されたダッシュボードでは、RED (Rate, Error & Duration) メトリクスを使用して、サービスの状態を監視することができます。このダッシュボードでは、パフォーマンスに関連したさまざまなチャートのほか、基盤となるホストやKubernetesポッド（該当する場合）の相関情報も提供されます。

ダッシュボードの様々なチャートを見てみましょう。

---

## 2. Splunk APM のメトリクスを確認する

左上のハンバーガーメニューから「APM」をクリックすると、APM Overview ダッシュボードが表示されます。

![select APM](../../../images/online-boutique-apm.png)

右側の **Explore** を選択し、先ほど見つけた Environment を選択し、時間を15分に設定します。これにより、自動的に生成されたOnline BoutiqueアプリケーションのDependency/Service Mapが表示されます。

以下のスクリーンショットのように表示されます:

![Online Boutique in APM](../../../images/online-boutique-map.png)

ページの下部にある凡例では、依存関係/サービスマップでの表記について説明しています。

![APM Legend](../../../images/apm-legend.png){: : .shadow .zoom}

* サービスリクエスト、エラーレート、ルートエラーレート。
* リクエストレート、レイテンシー、エラーレート

また、このビューでは、全体的なエラー率とレイテンシー率のタイムチャートを見ることができます。

## 3. OpenTelemetry ダッシュボード

Open Telemetery Collector がデプロイされると、プラットフォームは自動的に OpenTelemetry Collector のメトリクスを表示するダッシュボードを作成します。

左上のハンバーガーメニューから、 **Dashboards → OpenTelemetry Collector** を選択し、メトリクスとスパンが送信されていることを確認しましょう。

![OpenTelemetry Collector dashboard](../../../images/otel-dashboard.png)

## 4. OpenTelemetry zpages

送信されたトレースをデバッグするには、zpages 拡張機能を使用できます。[zpages][zpages] は OpenTelemetry Collector の一種で、トラブルシューティングや統計用のライブデータを提供します。これらは、EC2インスタンスのIPアドレスのポート `55679` で利用できます。Webブラウザで新しいタブを開き、 `http://{==EC2-IP==}:55679/debug/tracez` と入力すると、zpages の出力を見ることができます。

[zpages]: https://github.com/open-telemetry/opentelemetry-specification/blob/main/experimental/trace/zpages.md#tracez

![zpages](../../../images/zpages.png)

また、シェルプロンプトから、テキストベースのブラウザを実行することもできます。

{{< tabpane >}}
  {{< tab header="Lynx Command" lang="text" >}}
    lynx http://localhost:55679/debug/tracez
  {{< /tab >}}
{{< /tabpane >}}
