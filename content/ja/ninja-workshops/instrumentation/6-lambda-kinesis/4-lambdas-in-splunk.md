---
title: Splunk APM、Lambda Functions とトレース
linkTitle: 4. Splunk APM での Lambda トレース
weight: 4
time: 10 mins
---

Lambda 関数はかなりの量のトレースデータを生成しているはずですので、それを確認する必要があります。Lambda 関数のリソース定義で設定した環境変数と OpenTelemetry Lambda レイヤーの組み合わせにより、Splunk APM で関数とトレースを表示する準備が整っているはずです。

{{% exercise title="Splunk APM でトレースを表示する" %}}

まず、Splunk APM が受信しているトレースデータから `Environment` を認識していることを確認しましょう。これは `main.tf` の Lambda 関数定義で `OTEL_RESOURCE_ATTRIBUTES` 変数の一部として設定した `deployment.name` です。また、先ほど実行した `terraform apply` コマンドの出力の一つでもあります。

Splunk Observability Cloud で以下を行います

* 左側のメインメニューから `APM` ボタンをクリックします。Splunk APM の概要ページに移動します。
* `Environment:` ドロップダウンから APM 環境を選択します。
  * APM 環境は `PREFIX-lambda-shop` の形式になっています。`PREFIX` は前提条件セクションで設定した環境変数から取得されます。

{{< notice warning >}}
トレースが Splunk APM に表示されるまで数分かかる場合があります。環境名が環境のリストに表示されるまで、ブラウザの更新を試してください。
{{< /notice >}}

![Splunk APM, Environment Name](../images/02-Auto-APM-EnvironmentName.png)

Environment ドロップダウンから環境名を選択したら、Lambda 関数の Service Map を確認できます。

* APM 概要ページの右側にある `Service Map` ボタンをクリックします。Service Map ビューに移動します。

![Splunk APM, Service Map Button](../images/03-Auto-ServiceMapButton.png)

`producer-lambda` 関数と、レコードを配置するために Kinesis Stream に対して行っている呼び出しを確認できるはずです。

![Splunk APM, Service Map](../images/04-Auto-ServiceMap.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
アーキテクチャに基づくと、これらは接続されているべきではないでしょうか？なぜ接続されていないのでしょうか？
{{% /notice %}}

## Lambda 関数からのトレースを探索する

* `Traces` ボタンをクリックして Trace Analyzer を表示します。

![Splunk APM, Trace Button](../images/05-Auto-TraceButton.png)

このページでは、`producer-lambda` 関数の OpenTelemetry Lambda レイヤーから取り込まれたトレースを確認できます。

![Splunk APM, Trace Analyzer](../images/06-Auto-TraceAnalyzer.png)

* リストからトレースを選択して確認するには、ハイパーリンクされた `Trace ID` をクリックします。

![Splunk APM, Trace and Spans](../images/07-Auto-TraceNSpans.png)

`producer-lambda` 関数が Kinesis Stream にレコードを配置していることがわかります。しかし、`consumer-lambda` 関数のアクションが見つかりません！

これはトレースコンテキストが伝播されていないためです。このワークショップの時点では、Kinesis サービスによるトレースコンテキストの伝播はすぐに使える状態ではサポートされていません。分散トレースは Kinesis サービスで停止し、そのコンテキストがストリームを通じて自動的に伝播されないため、それ以上先を確認することができません。

まだ、ですが...

このワークショップの次のセクションで、この問題を回避する方法を見ていきましょう。その前に、クリーンアップを行いましょう！

{{% /exercise %}}

{{% exercise title="クリーンアップ" %}}

## メッセージを停止する

この自動計装の演習の一部としてデプロイしたリソースをクリーンアップする必要があります。同様に、`producer-lambda` エンドポイントに対してトラフィックを生成していたスクリプトも、まだ実行中であれば停止する必要があります。以下の手順に従ってクリーンアップを行ってください。

* `send_message.py` スクリプトがまだ実行中の場合は、以下のコマンドで停止します

```bash
fg
```

* これによりバックグラウンドプロセスがフォアグラウンドに戻ります。
* 次に `[CONTROL-C]` を押してプロセスを終了します。

## すべての AWS リソースを破棄する

Terraform はリソースを個別に、またデプロイメントとして状態管理するのに優れています。定義の変更に応じてデプロイ済みリソースを更新することもできます。しかし、新たに始めるために、このワークショップの手動計装部分の一部としてリソースを破棄して再デプロイします。

以下の手順に従ってリソースを破棄してください

* `auto` ディレクトリに移動します

```bash
cd ~/workshop/lambda/auto
```

* 先ほどデプロイした Lambda 関数やその他の AWS リソースを破棄します

```bash
terraform destroy
```

* `Enter a value:` プロンプトが表示されたら `yes` と応答します
* これによりリソースが破棄され、クリーンな環境が残ります

このプロセスにより、アクティビティの結果として作成されたファイルやディレクトリは残ります。それらについて心配する必要はありません。

{{% /exercise %}}
