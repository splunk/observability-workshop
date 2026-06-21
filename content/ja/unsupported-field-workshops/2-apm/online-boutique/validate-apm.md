---
title: 1.1 APM データの検証
weight: 2
time: 5 minutes
---

## 1. RED メトリクス

**Dashboards → All Dashboards → APM Services → Service** に移動します。ここで Online Boutique アプリケーションの RED メトリクス（Rate、Error、Duration）を確認できます。

これには、アプリケーション環境の名前を知る必要があります。このワークショップでは、すべての環境が `<instance>-workshop` を使用します。

`instance` を確認するには、AWS/EC2 インスタンスで以下のコマンドを実行します

{{< tabs >}}
{{% tab title="Echo Instance" %}}

``` bash
echo $INSTANCE-workshop
```

{{% /tab %}}
{{% tab title="Output Example" %}}

``` text
bdzx-workshop
```

{{% /tab %}}
{{< /tabs >}}

前のステップで確認した環境を選択し、`frontend` サービスを選択して、時間を Past 15 minutes に設定します。

![APM Dashboard](../../images/online-boutique-service-dashboard.png)

この自動生成されたダッシュボードを使用して、RED（Rate、Error、Duration）メトリクスによりサービスの健全性を監視できます。さまざまなパフォーマンス関連のチャートに加え、基盤となるホストや Kubernetes Pod（該当する場合）の相関情報も提供されます。

このダッシュボードのさまざまなチャートを探索してみてください。

---

## 2. APM メトリクス

左側のメニューカードで **APM** をクリックすると、APM Overview ダッシュボードが表示されます

![select APM](../../images/online-boutique-apm.png)

右側の **Explore** を選択し、先ほど確認した環境を選択して、時間を 15 minutes に設定します。これにより、Online Boutique アプリケーションの自動生成された Dependency/Service Map が表示されます。

以下のスクリーンショットのように表示されるはずです

![Online Boutique in APM](../../images/online-boutique-map.png)

ページ下部の凡例は、Dependency/Service Map のさまざまな可視化の説明です。

![APM Legend](../../images/apm-legend.png)

* サービスリクエスト、エラーレート、ルートエラーレート
* リクエストレート、レイテンシー、エラーレート

また、このビューでは、全体的な Error レートと Latency レートの時系列チャートを確認できます。

## 3. OpenTelemetry Dashboard

OpenTelemetry Collector がデプロイされると、プラットフォームは自動的に OpenTelemetry Collector メトリクスを表示する組み込みダッシュボードを提供します。

左上のハンバーガーメニューから **Dashboards → OpenTelemetry Collector** を選択し、ページの一番下までスクロールして、メトリクスとスパンが送信されていることを確認します

![OpenTelemetry Collector dashboard](../../images/otel-dashboard.png)

## 4. OpenTelemetry zpages

送信されているトレースをデバッグするには、zpages 拡張機能を使用できます。[zpages][zpages] は OpenTelemetry Collector の一部であり、トラブルシューティングと統計のためのライブデータを提供します。

{{% expand title="{{% badge style=primary icon=star %}}**Ninja** - EC2 インスタンスで zPages にアクセス{{% /badge %}}" %}}
{{% notice style="blue" %}}
zPages は EC2 インスタンスの IP アドレスのポート `55679` で利用できます。Web ブラウザで新しいタブを開き、`http://{==EC2-IP==}:55679/debug/tracez` を入力すると、zpages の出力を確認できます。

または、シェルプロンプトからテキストベースのブラウザを実行できます

``` bash
lynx http://localhost:55679/debug/tracez
```

{{% /notice %}}
{{% /expand %}}

ワークショップのインストラクターが zPages にアクセスするための URL を提供します。この URL をブラウザに入力すると、zPages の出力が表示されます。

[zpages]: https://github.com/open-telemetry/opentelemetry-specification/blob/main/experimental/trace/zpages.md#tracez

![zpages](../../images/zpages.png)
