---
title: Splunk APM、Lambda Functions & Traces
linkTitle: 4. Lambda Traces in Splunk APM
weight: 4
time: 10 mins
---

Lambda関数はかなりの量のトレースデータを生成しているはずです。これを確認する必要があります。Lambda関数のリソース定義で設定した環境変数とOpenTelemetry Lambdaレイヤーの組み合わせにより、Splunk APMで関数とトレースを表示する準備が整いました。

{{% exercise title="Splunk APMでトレースを表示する" %}}

まず、Splunk APMが受信しているトレースデータから`Environment`を認識していることを確認しましょう。これは`main.tf`のLambda関数定義で`OTEL_RESOURCE_ATTRIBUTES`変数の一部として設定した`deployment.name`です。また、先ほど実行した`terraform apply`コマンドの出力の一つでもあります。

Splunk Observability Cloudで以下を行います。

* 左側のメインメニューから `APM` ボタンをクリックします。Splunk APM Overviewに移動します。
* `Environment:` ドロップダウンからAPM Environmentを選択します。
  * APM Environmentは `PREFIX-lambda-shop` の形式です。`PREFIX`は前提条件のセクションで設定した環境変数から取得されます。

{{< notice warning >}}
トレースがSplunk APMに表示されるまで数分かかる場合があります。環境名がリストに表示されるまで、ブラウザを更新してみてください。
{{< /notice >}}

![Splunk APM, Environment Name](../images/02-Auto-APM-EnvironmentName.png)

Environmentドロップダウンから環境名を選択したら、Lambda関数のService Mapを確認できます。

* APM Overviewページの右側にある `Service Map` ボタンをクリックします。Service Mapビューに移動します。

![Splunk APM, Service Map Button](../images/03-Auto-ServiceMapButton.png)

`producer-lambda`関数と、レコードを送信するためにKinesis Streamに対して行っている呼び出しが表示されます。

![Splunk APM, Service Map](../images/04-Auto-ServiceMap.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
アーキテクチャに基づくと、これらは接続されているべきではありませんか？なぜ接続されていないのでしょうか？
{{% /notice %}}

## Lambda関数からのトレースを確認する

* `Traces` ボタンをクリックしてTrace Analyzerを表示します。

![Splunk APM, Trace Button](../images/05-Auto-TraceButton.png)

このページでは、`producer-lambda`関数のOpenTelemetry Lambdaレイヤーから取り込まれたトレースを確認できます。

![Splunk APM, Trace Analyzer](../images/06-Auto-TraceAnalyzer.png)

* リストからトレースを選択して確認するには、ハイパーリンクされた `Trace ID` をクリックします。

![Splunk APM, Trace and Spans](../images/07-Auto-TraceNSpans.png)

`producer-lambda`関数がKinesis Streamにレコードを送信していることが確認できます。しかし、`consumer-lambda`関数のアクションが見当たりません！

これはトレースコンテキストが伝播されていないためです。このワークショップの時点では、Kinesisサービスはトレースコンテキストの伝播をすぐに使える形ではサポートしていません。分散トレースはKinesisサービスで停止し、コンテキストがストリームを通じて自動的に伝播されないため、その先を確認することができません。

まだ、できませんが...

このワークショップの次のセクションで、この問題を回避する方法を見ていきましょう。その前に、クリーンアップを行いましょう！

{{% /exercise %}}

{{% exercise title="クリーンアップ" %}}

## メッセージを停止する

この自動計装の演習でデプロイしたリソースをクリーンアップする必要があります。同様に、`producer-lambda`エンドポイントに対してトラフィックを生成していたスクリプトがまだ実行中であれば、停止する必要があります。以下の手順に従ってクリーンアップを行います。

* `send_message.py`スクリプトがまだ実行中の場合、以下のコマンドで停止します。

```bash
fg
```

* これによりバックグラウンドプロセスがフォアグラウンドに移動します。
* 次に `[CONTROL-C]` を押してプロセスを終了します。

## すべてのAWSリソースを削除する

Terraformはリソースの状態を個別に、またデプロイメントとして管理するのに優れています。定義の変更に応じてデプロイ済みリソースを更新することもできます。しかし、最初からやり直すために、リソースを削除し、このワークショップの手動計装パートで再デプロイします。

以下の手順に従ってリソースを削除してください。

* `auto`ディレクトリに移動します。

```bash
cd ~/workshop/lambda/auto
```

* 先ほどデプロイしたLambda関数とその他のAWSリソースを削除します。

```bash
terraform destroy
```

* `Enter a value:`プロンプトが表示されたら `yes` と入力します
* これによりリソースが削除され、クリーンな環境が残ります

このプロセスにより、作業の結果として作成されたファイルやディレクトリはそのまま残ります。それらについて心配する必要はありません。

{{% /exercise %}}
