---
title: Splunk APM、Lambda関数およびトレース
linkTitle: 3. Splunk APMでのLambdaトレース
weight: 3
---

Lambda 関数は相当量のトレースデータを生成しているはずで、それを確認する必要があります。Lambda 関数のリソース定義で構成された環境変数と OpenTelemetry Lambda layer の組み合わせにより、Splunk APM で関数とトレースを表示する準備が整いました。

#### Splunk APM 概要で環境名を確認する

まず、Splunk APM が受信しているトレースデータから`Environment`を認識していることを確認しましょう。これは`main.tf`の Lambda 関数定義で設定した`OTEL_RESOURCE_ATTRIBUTES`変数の一部として設定した`deployment.name`です。これは先ほど実行した`terraform apply`コマンドの出力の 1 つでもありました。

Splunk Observability Cloud で：

- 左側のメインメニューから`APM`ボタンをクリックします。これにより Splunk APM 概要に移動します。

- `Environment:`ドロップダウンからあなたの APM 環境を選択します。
  - _APM 環境は`PREFIX-lambda-shop`形式になっているはずです。`PREFIX`は前提条件セクションで設定した環境変数から取得されます_

> [!NOTE]
> トレースが Splunk APM に表示されるまで数分かかる場合があります。環境のリストにあなたの環境名が表示されるまで、ブラウザの更新ボタンを押してみてください

![Splunk APM, Environment Name](../images/02-Auto-APM-EnvironmentName.png)

#### 環境のサービスマップを表示する

Environment ドロップダウンから環境名を選択したら、Lambda 関数のサービスマップを確認できます。

- APM 概要ページの右側にある`Service Map`ボタンをクリックします。これによりサービスマップビューに移動します。

![Splunk APM、サービスマップボタン](../images/03-Auto-ServiceMapButton.png)

`producer-lambda`関数とそのレコードを配置するために Kinesis ストリームに対して行っている呼び出しが表示されるはずです。

![Splunk APM、サービスマップ](../images/04-Auto-ServiceMap.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
あなたの`consumer-lambda`関数はどうなっていますか？
{{% /notice %}}

#### Lambda 関数からのトレースを調査する

- `Traces`ボタンをクリックしてトレースアナライザーを表示します。

![Splunk APM、トレースボタン](../images/05-Auto-TraceButton.png)

このページでは、`producer-lambda`関数の OpenTelemetry Lambda layer から取り込まれたトレースを確認できます。

![Splunk APM、トレースアナライザー](../images/06-Auto-TraceAnalyzer.png)

- リストからハイパーリンクされた`Trace ID`をクリックして、調査するトレースを選択します。

![Splunk APM、トレースとスパン](../images/07-Auto-TraceNSpans.png)

`producer-lambda`関数が Kinesis ストリームにレコードを配置しているのが確認できます。しかし、`consumer-lambda`関数のアクションが見当たりません！

これはトレースコンテキストが伝播されていないためです。このワークショップの時点では、Kinesis サービスはトレースコンテキスト伝播をすぐには対応していません。分散トレースは Kinesis サービスで止まっており、そのコンテキストがストリームを通じて自動的に伝播されないため、それ以上先を見ることができません。

少なくとも、今はまだ...

次のセクションでこの問題にどう対処するか見ていきましょう。しかしその前に、後片付けをしましょう！

### クリーンアップ

この自動計装演習の一部としてデプロイしたリソースはクリーンアップする必要があります。同様に、`producer-lambda`エンドポイントに対してトラフィックを生成していたスクリプトも、まだ実行中であれば停止する必要があります。以下の手順に従ってクリーンアップを行ってください。

#### `send_message`の停止

- `send_message.py`スクリプトがまだ実行中の場合は、次のコマンドで停止します：

  ```bash
  fg
  ```

  - これによりバックグラウンドプロセスがフォアグラウンドに移動します。
  - 次に`[CONTROL-C]`を押してプロセスを終了できます。

#### 全ての AWS リソースを破棄する

Terraform は個々のリソースの状態をデプロイメントとして管理するのに優れています。定義に変更があっても、デプロイされたリソースを更新することもできます。しかし、一からやり直すために、リソースを破棄し、このワークショップの手動計装部分の一部として再デプロイします。

以下の手順に従ってリソースを破棄してください：

- Ensure you are in the `auto` directory:

  ```bash
  pwd
  ```

  - _The expected output would be **~/o11y-lambda-workshop/auto**_

- If you are not in the `auto` directory, run the following command:

  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- Destroy the Lambda functions and other AWS resources you deployed earlier:

  ```bash
  terraform destroy
  ```

  - respond `yes` when you see the `Enter a value:` prompt
  - This will result in the resources being destroyed, leaving you with a clean environment

This process will leave you with the files and directories created as a result of our activity. Do not worry about those.
