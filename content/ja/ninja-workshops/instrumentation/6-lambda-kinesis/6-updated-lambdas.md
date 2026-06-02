---
title: Splunk APM、Lambda 関数とトレース、再び!
linkTitle: 6. Splunk APM での更新された Lambda
weight: 6
---

ログ以外でコンテキスト伝播の結果を確認するため、再び [Splunk APM UI](https://app.us1.signalfx.com/#/apm) を参照します。

#### Splunk APM Service Map で Lambda 関数を表示する

APM の環境の Service Map をもう一度見てみましょう。

Splunk Observability Cloud で:

- メインメニューの `APM` ボタンをクリックします。

- `Environment:` ドロップダウンから APM 環境を選択します。

- APM Overview ページの右側にある `Service Map` ボタンをクリックします。これにより Service Map ビューに移動します。

> [!NOTE]
> _注意: トレースが Splunk APM に表示されるまで数分かかることがあります。環境名のリストに自分の環境名が表示されるまで、ブラウザの更新を試してください。_

{{% notice title="Workshop Question" style="tip" icon="question" %}}
違いに気づきましたか?
{{% /notice %}}

- 今回は `producer-lambda` と `consumer-lambda` 関数が、伝播されたコンテキストによってリンクされていることが確認できるはずです!

![Splunk APM, Service Map](../images/09-Manual-ServiceMap.png)

#### Trace ID で Lambda トレースを探索する

次に、環境に関連するトレースをもう一度見てみましょう。

- consumer 関数のログからコピーした Trace ID を Traces の下の `View Trace ID` 検索ボックスに貼り付け、`Go` をクリックします

![Splunk APM, Trace Button](../images/10-Manual-TraceButton.png)

> [!NOTE]
> Trace ID は、私たちが伝播したトレースコンテキストの一部でした。

最も一般的な 2 つの伝播標準について読むことができます:

1. [W3C](https:///www.w3.org/TR/trace-context/#traceparent-header)
2. [B3](https://github.com/openzipkin/b3-propagation#overall-process)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
どちらを使用していますか?

- _NodeJS 関数をサポートする Splunk Distribution of Opentelemetry JS は、[デフォルト](https://docs.splunk.com/observability/en/gdi/get-data-in/application/nodejs/splunk-nodejs-otel-distribution.html#defaults-of-the-splunk-distribution-of-opentelemetry-js) で `W3C` 標準を使用します_

{{% /notice %}}

{{% notice title="Workshop Question" style="tip" icon="question" %}}
ボーナス問題: W3C と B3 のヘッダーを混在させるとどうなるでしょうか?
{{% /notice %}}

![Splunk APM, Trace by ID](../images/11-Manual-TraceByID.png)

`consumer-lambda` スパンをクリックします。

{{% notice title="Workshop Question" style="tip" icon="question" %}}
メッセージの属性を見つけることができますか?
{{% /notice %}}

![Splunk APM, Span Tags](../images/12-Manual-SpanTags.png)

### クリーンアップ

ようやくワークショップの最後にたどり着きました。後片付けをお願いします!

#### `send_message` を終了する

- `send_message.py` スクリプトがまだ実行中の場合は、次のコマンドで停止します:

  ```bash
  fg
  ```

  - これによりバックグラウンドプロセスがフォアグラウンドに移動します。
  - 次に `[CONTROL-C]` を押してプロセスを終了できます。

#### すべての AWS リソースを破棄する

Terraform は、リソースを個別に、そしてデプロイ全体としての状態を管理するのに優れています。定義の変更に応じてデプロイ済みリソースを更新することもできます。しかし、最初からやり直すために、リソースを破棄し、このワークショップの手動計装パートの一環として再デプロイします。

リソースを破棄するには、以下の手順に従ってください:

- `manual` ディレクトリにいることを確認します:

  ```bash
  pwd
  ```

  - _期待される出力は **~/workshop/lambda/manual** です_

- `manual` ディレクトリにいない場合は、次のコマンドを実行します:

  ```bash
  cd ~/workshop/lambda/manual
  ```

- 先ほどデプロイした Lambda 関数およびその他の AWS リソースを破棄します:

  ```bash
  terraform destroy
  ```

  - `Enter a value:` プロンプトが表示されたら `yes` と応答します
  - これによりリソースが破棄され、クリーンな環境になります
