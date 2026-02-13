---
title: Splunk APM、Lambda関数およびトレース
linkTitle: 3. Splunk APMでのLambdaトレース
weight: 3
---

Lambda関数は相当量のトレースデータを生成しているはずで、それを確認する必要があります。Lambda関数のリソース定義で構成された環境変数とOpenTelemetry Lambda layerの組み合わせにより、Splunk APMで関数とトレースを表示する準備が整いました。

#### Splunk APM 概要で環境名を確認する

まず、Splunk APMが受信しているトレースデータから `Environment` を認識していることを確認しましょう。これは `main.tf` のLambda関数定義で設定した `OTEL_RESOURCE_ATTRIBUTES` 変数の一部として設定した `deployment.name` です。これは先ほど実行した `terraform apply` コマンドの出力の1つでもありました。

Splunk Observability Cloudで：

- 左側のメインメニューから `APM` ボタンをクリックします。これによりSplunk APM概要に移動します。

- `Environment:` ドロップダウンからあなたのAPM環境を選択します。
  - _APM 環境は `PREFIX-lambda-shop` 形式になっているはずです。`PREFIX` は前提条件セクションで設定した環境変数から取得されます_

> [!NOTE]
> トレースが Splunk APM に表示されるまで数分かかる場合があります。環境のリストにあなたの環境名が表示されるまで、ブラウザの更新ボタンを押してみてください

![Splunk APM, Environment Name](../images/02-Auto-APM-EnvironmentName.png)

#### 環境のサービスマップを表示する

Environmentドロップダウンから環境名を選択したら、Lambda関数のサービスマップを確認できます。

- APM概要ページの右側にある `Service Map` ボタンをクリックします。これによりサービスマップビューに移動します。

![Splunk APM、サービスマップボタン](../images/03-Auto-ServiceMapButton.png)

`producer-lambda` 関数とそのレコードを配置するためにKinesisストリームに対して行っている呼び出しが表示されるはずです。

![Splunk APM、サービスマップ](../images/04-Auto-ServiceMap.png)

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
あなたの `consumer-lambda` 関数はどうなっていますか？
{{% /notice %}}

#### Lambda 関数からのトレースを調査する

- `Traces` ボタンをクリックしてトレースアナライザーを表示します。

![Splunk APM、トレースボタン](../images/05-Auto-TraceButton.png)

このページでは、`producer-lambda` 関数のOpenTelemetry Lambda layerから取り込まれたトレースを確認できます。

![Splunk APM、トレースアナライザー](../images/06-Auto-TraceAnalyzer.png)

- リストからハイパーリンクされた `Trace ID` をクリックして、調査するトレースを選択します。

![Splunk APM、トレースとスパン](../images/07-Auto-TraceNSpans.png)

`producer-lambda` 関数がKinesisストリームにレコードを配置しているのが確認できます。しかし、`consumer-lambda` 関数のアクションが見当たりません！

これはトレースコンテキストが伝播されていないためです。このワークショップの時点では、Kinesisサービスはトレースコンテキスト伝播をすぐには対応していません。分散トレースはKinesisサービスで止まっており、そのコンテキストがストリームを通じて自動的に伝播されないため、それ以上先を見ることができません。

少なくとも、今はまだ...

次のセクションでこの問題にどう対処するか見ていきましょう。しかしその前に、後片付けをしましょう！

### クリーンアップ

この自動計装演習の一部としてデプロイしたリソースはクリーンアップする必要があります。同様に、`producer-lambda` エンドポイントに対してトラフィックを生成していたスクリプトも、まだ実行中であれば停止する必要があります。以下の手順に従ってクリーンアップを行ってください。

#### `send_message` の停止

- `send_message.py` スクリプトがまだ実行中の場合は、次のコマンドで停止します：

  ```bash
  fg
  ```

  - これによりバックグラウンドプロセスがフォアグラウンドに移動します。
  - 次に `[CONTROL-C]` を押してプロセスを終了できます。

#### 全ての AWS リソースを破棄する

Terraformは個々のリソースの状態をデプロイメントとして管理するのに優れています。定義に変更があっても、デプロイされたリソースを更新することもできます。しかし、一からやり直すために、リソースを破棄し、このワークショップの手動計装部分の一部として再デプロイします。

以下の手順に従ってリソースを破棄してください：

- `auto` ディレクトリにいることを確認します：

  ```bash
  pwd
  ```

  - _期待される出力は **~/o11y-lambda-workshop/auto** です_

- `auto` ディレクトリにいない場合は、以下のコマンドを実行します：

  ```bash
  cd ~/o11y-lambda-workshop/auto
  ```

- 先ほどデプロイしたLambda関数とその他のAWSリソースを破棄します：

  ```bash
  terraform destroy
  ```

  - `Enter a value:` プロンプトが表示されたら `yes` と応答します
  - これによりリソースが破棄され、クリーンな環境が残ります

このプロセスにより、私たちの活動の結果として作成されたファイルとディレクトリは残ります。それらについては心配する必要はありません。
