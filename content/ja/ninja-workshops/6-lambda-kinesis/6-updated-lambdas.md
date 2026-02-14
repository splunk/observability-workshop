---
title: Splunk APM、Lambda関数とトレース、再び！
linkTitle: 6. Splunk APMでの更新されたLambda
weight: 6
---

ログの外部でコンテキスト伝播の結果を確認するために、もう一度[Splunk APM UI](https://app.us1.signalfx.com/#/apm)を参照します。

#### Splunk APM サービスマップで Lambda 関数を表示する

もう一度APMで環境のサービスマップを確認してみましょう。

Splunk Observability Cloudで：

- メインメニューの `APM` ボタンをクリックします。

- `Environment:` ドロップダウンからあなたのAPM環境を選択します。

- APM概要ページの右側にある `Service Map` ボタンをクリックします。これによりサービスマップビューに移動します。

> [!NOTE] > _注意：トレースが Splunk APM に表示されるまで数分かかる場合があります。環境のリストにあなたの環境名が表示されるまで、ブラウザの更新ボタンを押してみてください_

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
違いに気づきましたか？
{{% /notice %}}

- 今回は、伝播されたコンテキストによってリンクされた `producer-lambda` と `consumer-lambda` 関数が見えるはずです！

![Splunk APM、サービスマップ](../images/09-Manual-ServiceMap.png)

#### トレース ID で Lambda トレースを調査する

次に、環境に関連するトレースをもう一度確認します。

- コンシューマー関数のログからコピーしたトレースIDを、Traces下の `View Trace ID` 検索ボックスに貼り付け、`Go` をクリックします

![Splunk APM、トレースボタン](../images/10-Manual-TraceButton.png)

> [!NOTE]
> トレース ID は、私たちが伝播したトレースコンテキストの一部でした。

最も一般的な2つの伝播規格について読むことができます：

1. [W3C](https:///www.w3.org/TR/trace-context/#traceparent-header)
2. [B3](https://github.com/openzipkin/b3-propagation#overall-process)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
私たちはどちらを使用していますか？

- _私たちの NodeJS 関数をサポートする Splunk Distribution of Opentelemetry JS は、[デフォルト](https://docs.splunk.com/observability/en/gdi/get-data-in/application/nodejs/splunk-nodejs-otel-distribution.html#defaults-of-the-splunk-distribution-of-opentelemetry-js)で `W3C` 標準を使用しています_

{{% /notice %}}

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
ボーナス質問：W3CヘッダーとB3ヘッダーを混在させるとどうなりますか？
{{% /notice %}}

![Splunk APM、IDによるトレース](../images/11-Manual-TraceByID.png)

`consumer-lambda` スパンをクリックしてください。

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
あなたのメッセージからの属性を見つけることができますか？
{{% /notice %}}

![Splunk APM、スパンタグ](../images/12-Manual-SpanTags.png)

### クリーンアップ

いよいよワークショップの最後に来ました。後片付けをしましょう！

#### `send_message` の停止

- `send_message.py` スクリプトがまだ実行中の場合は、次のコマンドで停止します：

  ```bash
  fg
  ```

  - これによりバックグラウンドプロセスがフォアグラウンドに移動します。
  - 次に `[CONTROL-C]` を押してプロセスを終了できます。

#### すべての AWS リソースを破棄する

Terraformは個々のリソースの状態をデプロイメントとして管理するのに優れています。定義に変更があっても、デプロイされたリソースを更新することもできます。しかし、一からやり直すために、リソースを破棄し、このワークショップの手動計装部分の一部として再デプロイします。

以下の手順に従ってリソースを破棄してください：

- `manual` ディレクトリにいることを確認します：

  ```bash
  pwd
  ```

  - _予想される出力は **~/o11y-lambda-workshop/manual** です_

- `manual` ディレクトリにいない場合は、次のコマンドを実行します：

  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- 以前にデプロイしたLambda関数とその他のAWSリソースを破棄します：

  ```bash
  terraform destroy
  ```

  - `Enter a value:` プロンプトが表示されたら `yes` と応答します
  - これにより、リソースが破棄され、クリーンな環境が残ります
