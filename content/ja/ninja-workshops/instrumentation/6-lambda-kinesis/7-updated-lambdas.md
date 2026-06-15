---
title: Splunk APM、Lambda Functions とトレース、再び！
linkTitle: 7. 更新された Lambda を Splunk APM で確認
weight: 7
---

ログ以外でコンテキスト伝播の結果を確認するために、再度 [Splunk APM UI](https://app.us1.signalfx.com/#/apm) を参照します。

{{% exercise title="Splunk APM マップで Lambda Functions を確認する" %}}

APM で環境のサービスマップをもう一度確認しましょう。

Splunk Observability Cloud で

* メインメニューの `APM` ボタンをクリックします。
* `Environment:` ドロップダウンから APM 環境を選択します。
* APM Overview ページの右側にある `Service Map` ボタンをクリックします。これにより、サービスマップビューに移動します。

{{< notice warning >}}
トレースが Splunk APM に表示されるまで数分かかる場合があります。環境名が環境リストに表示されるまで、ブラウザのリフレッシュを試してください。
{{< /notice >}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
違いに気づきましたか？
{{% /notice %}}

* 今回は、伝播されたコンテキストによってリンクされた `producer-lambda` と `consumer-lambda` 関数が表示されるはずです！

![Splunk APM, Service Map](../images/09-Manual-ServiceMap.png)

{{% /exercise %}}

{{% exercise title="Trace ID からトレースを見つける" %}}

次に、環境に関連するトレースをもう一度確認します。

* consumer 関数のログからコピーした Trace ID を、Traces の下にある `View Trace ID` 検索ボックスに貼り付けて、`Go` をクリックします。

![Splunk APM, Trace Button](../images/10-Manual-TraceButton.png)

{{< notice info >}}
Trace ID は、伝播したトレースコンテキストの一部でした。
{{< /notice >}}

最も一般的な2つの伝播標準について詳しく読むことができます

1. [W3C](https:///www.w3.org/TR/trace-context/#traceparent-header)
2. [B3](https://github.com/openzipkin/b3-propagation#overall-process)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
どちらを使用していますか？

* _NodeJS 関数をサポートする Splunk Distribution of Opentelemetry JS は、[デフォルト](https://docs.splunk.com/observability/en/gdi/get-data-in/application/nodejs/splunk-nodejs-otel-distribution.html#defaults-of-the-splunk-distribution-of-opentelemetry-js)で `W3C` 標準を使用します_

{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
ボーナス質問：W3C と B3 のヘッダーを混在させるとどうなりますか？
{{% /notice %}}

![Splunk APM, Trace by ID](../images/11-Manual-TraceByID.png)

`consumer-lambda` スパンをクリックします。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
メッセージの属性を見つけることができますか？
{{% /notice %}}

![Splunk APM, Span Tags](../images/12-Manual-SpanTags.png)

{{% /exercise %}}

確認ができたので、クリーンアップを行います。

{{% exercise title="クリーンアップ" %}}

## メッセージの停止

この自動計装演習の一環としてデプロイしたリソースをクリーンアップする必要があります。同様に、`producer-lambda` エンドポイントに対してトラフィックを生成していたスクリプトも、まだ実行中であれば停止する必要があります。以下の手順に従ってクリーンアップを行ってください。

* `send_message.py` スクリプトがまだ実行中の場合は、以下のコマンドで停止します

```bash
fg
```

* これにより、バックグラウンドプロセスがフォアグラウンドに移動します。
* 次に `[CONTROL-C]` を押してプロセスを終了します。

## すべての AWS リソースの破棄

Terraform は、リソースを個別に、またデプロイメントとして状態管理するのに優れています。定義の変更に応じてデプロイ済みリソースを更新することもできます。しかし、最初からやり直すために、リソースを破棄し、このワークショップの手動計装パートとして再デプロイします。

以下の手順に従ってリソースを破棄してください

* `manual` ディレクトリに移動します

```bash
cd ~/workshop/lambda/manual
```

* 先ほどデプロイした Lambda functions およびその他の AWS リソースを破棄します

```bash
terraform destroy
```

* `Enter a value:` プロンプトが表示されたら `yes` と入力します
* これにより、リソースが破棄され、クリーンな環境が残ります

{{% /exercise %}}
