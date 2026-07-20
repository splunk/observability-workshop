---
title: Splunk APM、Lambda FunctionsとTraces、再び！
linkTitle: 7. 更新されたLambdaをSplunk APMで確認
weight: 7
---

ログ以外でコンテキスト伝播の結果を確認するために、再度 [Splunk APM UI](https://app.us1.signalfx.com/#/apm) を参照します。

{{% exercise title="Splunk APM MapでLambda Functionsを確認する" %}}

APMで環境のService Mapをもう一度確認しましょう。

Splunk Observability Cloudで以下を行います。

* メインメニューの `APM` ボタンをクリックします。
* `Environment:` ドロップダウンからAPM環境を選択します。
* APM概要ページの右側にある `Service Map` ボタンをクリックします。Service Mapビューに移動します。

{{< notice warning >}}
Splunk APMにTraceが表示されるまで数分かかる場合があります。環境名がリストに表示されるまで、ブラウザの更新を試してください。
{{< /notice >}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
違いに気付きましたか？
{{% /notice %}}

* 今回は、伝播されたコンテキストによって `producer-lambda` と `consumer-lambda` 関数がリンクされていることが確認できるはずです！

![Splunk APM, Service Map](../images/09-Manual-ServiceMap.png)

{{% /exercise %}}

{{% exercise title="Trace IDからTraceを検索する" %}}

次に、環境に関連するTraceをもう一度確認します。

* consumer関数のログからコピーしたTrace IDを、Tracesの下にある `View Trace ID` 検索ボックスに貼り付けて `Go` をクリックします

![Splunk APM, Trace Button](../images/10-Manual-TraceButton.png)

{{< notice info >}}
Trace IDは、伝播したトレースコンテキストの一部です。
{{< /notice >}}

最も一般的な2つの伝播標準について詳しく読むことができます。

1. [W3C](https:///www.w3.org/TR/trace-context/#traceparent-header)
2. [B3](https://github.com/openzipkin/b3-propagation#overall-process)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
どちらを使用していますか？

* _NodeJS関数をサポートするSplunk Distribution of OpenTelemetry JSは、[デフォルト](https://docs.splunk.com/observability/en/gdi/get-data-in/application/nodejs/splunk-nodejs-otel-distribution.html#defaults-of-the-splunk-distribution-of-opentelemetry-js)で `W3C` 標準を使用します_

{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
ボーナス問題: W3CとB3のヘッダーを混在させるとどうなりますか？
{{% /notice %}}

![Splunk APM, Trace by ID](../images/11-Manual-TraceByID.png)

`consumer-lambda` Spanをクリックします。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
メッセージの属性を見つけることができますか？
{{% /notice %}}

![Splunk APM, Span Tags](../images/12-Manual-SpanTags.png)

{{% /exercise %}}

確認が完了したので、クリーンアップを行います。

{{% exercise title="クリーンアップ" %}}

## メッセージの停止

この計装演習の一部としてデプロイしたリソースをクリーンアップする必要があります。同様に、`producer-lambda` エンドポイントに対してトラフィックを生成していたスクリプトがまだ実行中の場合は停止する必要があります。以下の手順に従ってリソースをクリーンアップします。

* `send_message.py` スクリプトがまだ実行中の場合、以下のコマンドで停止します。

```bash
fg
```

* これによりバックグラウンドプロセスがフォアグラウンドに移動します。
* 次に `[CONTROL-C]` を押してプロセスを終了します。

## すべてのAWSリソースの削除

以下の手順に従ってリソースを削除します。

* `manual` ディレクトリに移動します。

```bash
cd ~/workshop/lambda/manual
```

* 先ほどデプロイしたLambda関数およびその他のAWSリソースを削除します。

```bash
terraform destroy
```

* `Enter a value:` プロンプトが表示されたら `yes` と入力します
* リソースが削除され、クリーンな環境が残ります

{{% /exercise %}}
