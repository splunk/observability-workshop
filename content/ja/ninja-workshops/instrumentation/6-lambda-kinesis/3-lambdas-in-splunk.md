---
title: Splunk APM, Lambda Functions & Traces
linkTitle: 3. Lambda Traces in Splunk APM
weight: 3
---

Lambda 関数からは大量のトレースデータが生成されているはずですので、これを確認していきましょう。Lambda 関数のリソース定義に設定した環境変数と OpenTelemetry Lambda Layer の組み合わせにより、Splunk APM で関数とトレースを表示する準備が整っているはずです。

#### Splunk APM Overview で Environment 名を確認する

まず、Splunk APM が受信しているトレースデータから `Environment` を認識していることを確認しましょう。これは `main.tf` の Lambda 関数定義で設定した `OTEL_RESOURCE_ATTRIBUTES` 変数の一部として指定した `deployment.name` です。先ほど実行した `terraform apply` コマンドの出力にも含まれていました。

Splunk Observability Cloud で次の手順を実行します。

- 左側のメインメニューから `APM` ボタンをクリックします。Splunk APM Overview が表示されます。

- `Environment:` ドロップダウンから APM Environment を選択します。
  - _APM environment は `PREFIX-lambda-shop` の形式になっているはずです。`PREFIX` は Prerequisites セクションで設定した環境変数から取得されます。_

> [!NOTE]
> トレースが Splunk APM に表示されるまで数分かかる場合があります。environment 名がリストに表示されるまで、ブラウザの更新ボタンを何度かクリックしてみてください。

![Splunk APM, Environment Name](../images/02-Auto-APM-EnvironmentName.png)

#### Environment の Service Map を表示する

Environment ドロップダウンから Environment 名を選択したら、Lambda 関数の Service Map を確認できます。

- APM Overview ページの右側にある `Service Map` ボタンをクリックします。Service Map ビューが表示されます。

![Splunk APM, Service Map Button](../images/03-Auto-ServiceMapButton.png)

`producer-lambda` 関数と、レコードを格納するために Kinesis Stream に対して行われている呼び出しを確認できるはずです。

![Splunk APM, Service Map](../images/04-Auto-ServiceMap.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
`consumer-lambda` 関数についてはどうでしょうか？
{{% /notice %}}

#### Lambda 関数からのトレースを調べる

- `Traces` ボタンをクリックして Trace Analyzer を表示します。

![Splunk APM, Trace Button](../images/05-Auto-TraceButton.png)

このページでは、`producer-lambda` 関数の OpenTelemetry Lambda Layer から取り込まれたトレースを確認できます。

![Splunk APM, Trace Analyzer](../images/06-Auto-TraceAnalyzer.png)

- リストからトレースを選択し、ハイパーリンクされた `Trace ID` をクリックして詳細を確認します。

![Splunk APM, Trace and Spans](../images/07-Auto-TraceNSpans.png)

`producer-lambda` 関数が Kinesis Stream にレコードを格納していることが確認できます。しかし、`consumer-lambda` 関数のアクションが見当たりません！

これはトレースコンテキストが伝播されていないためです。本ワークショップの執筆時点では、Kinesis サービスは out-of-the-box でトレースコンテキストの伝播をサポートしていません。分散トレースは Kinesis サービスで途切れてしまい、コンテキストがストリームを通じて自動的に伝播されないため、それ以上は確認できません。

少なくとも、まだは...

本ワークショップの次のセクションで、これをどのように回避するか見ていきましょう。ただしその前に、後片付けを行いましょう！

### Clean Up

この自動インストルメンテーションの演習でデプロイしたリソースをクリーンアップする必要があります。同様に、`producer-lambda` エンドポイントに対してトラフィックを生成していたスクリプトも、まだ実行中であれば停止する必要があります。以下の手順に従ってクリーンアップしてください。

#### `send_message` を停止する

- `send_message.py` スクリプトがまだ実行中の場合、次のコマンドで停止します。

  ```bash
  fg
  ```

  - これにより、バックグラウンドプロセスがフォアグラウンドに移動します。
  - 次に `[CONTROL-C]` を押してプロセスを停止できます。

#### すべての AWS リソースを破棄する

Terraform は、リソースを個別に、またデプロイ全体として状態管理するのに優れています。デプロイされたリソースを定義の変更に応じて更新することもできます。しかし、まっさらな状態から始めるために、リソースを破棄し、本ワークショップの手動インストルメンテーション部分の一環として再デプロイします。

リソースを破棄するには、次の手順に従ってください。

- `auto` ディレクトリにいることを確認します。

  ```bash
  pwd
  ```

  - _期待される出力は **~/workshop/lambda/auto** です_

- `auto` ディレクトリにいない場合は、次のコマンドを実行します。

  ```bash
  cd ~/workshop/lambda/auto
  ```

- 先ほどデプロイした Lambda 関数およびその他の AWS リソースを破棄します。

  ```bash
  terraform destroy
  ```

  - `Enter a value:` プロンプトが表示されたら `yes` と入力します
  - これによりリソースが破棄され、クリーンな環境が残ります

この処理を実行しても、これまでの作業によって作成されたファイルやディレクトリは残ります。それらについては気にする必要はありません。
