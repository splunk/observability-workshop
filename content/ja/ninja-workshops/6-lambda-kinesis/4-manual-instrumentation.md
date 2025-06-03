---
title: 手動計装
linkTitle: 4. 手動計装
weight: 4
---

ワークショップの第 2 部では、OpenTelemetry による手動計装が計測データ収集を強化する方法を実演することに焦点を当てます。より具体的には、今回のケースでは、`producer-lambda`関数から`consumer-lambda`関数にトレースコンテキストデータを伝播させることができるようになります。これにより、現在は自動コンテキスト伝播をサポートしていない Kinesis ストリームを介しても、2 つの関数間の関係を見ることができるようになります。

### 手動計装ワークショップディレクトリとコンテンツ

再度、作業ディレクトリとそのファイルの一部を確認することから始めます。今回は `o11y-lambda-workshop/manual` ディレクトリです。ここにはワークショップの手動計装部分のすべてのコンテンツがあります。

#### `manual` ディレクトリ

- 以下のコマンドを実行して `o11y-lambda-workshop/manual` ディレクトリに移動します：

  ```bash
  cd ~/o11y-lambda-workshop/manual
  ```

- `ls` コマンドでこのディレクトリの内容を確認します：

  ```bash
  ls
  ```

  - _出力には以下のファイルとディレクトリが含まれるはずです：_

    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
このディレクトリと最初に始めた auto ディレクトリに何か違いがありますか？
{{% /notice %}}

#### `auto` と `manual` のファイルを比較する

見た目が同じように見えるこれらのファイルが実際に同じかどうか確認しましょう。

- `auto` と `manual` ディレクトリの `main.tf` ファイルを比較します：

  ```bash
  diff ~/o11y-lambda-workshop/auto/main.tf ~/o11y-lambda-workshop/manual/main.tf
  ```

  - 違いはありません！_(違いがあるはずはありません。もし違いがあれば、ワークショップ進行役に支援を求めてください)_

- 次に、`producer.mjs` ファイルを比較してみましょう：

  ```bash
  diff ~/o11y-lambda-workshop/auto/handler/producer.mjs ~/o11y-lambda-workshop/manual/handler/producer.mjs
  ```

  - ここにはかなりの違いがあります！

- ファイル全体を表示してその内容を調べたい場合は以下を実行します：

  ```bash
  cat ~/o11y-lambda-workshop/handler/producer.mjs
  ```

  - 必要な手動計装タスクを処理するために、いくつかの OpenTelemetry オブジェクトを関数に直接インポートしていることに注目してください。

  ```js
  import { context, propagation, trace } from "@opentelemetry/api";
  ```

  - プロデューサー関数でコンテキストを伝播するために、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) から次のオブジェクトをインポートしています：
    - context
    - propagation
    - trace

- 最後に、`consumer.mjs` ファイルを比較します：

  ```bash
  diff ~/o11y-lambda-workshop/auto/handler/consumer.mjs ~/o11y-lambda-workshop/manual/handler/consumer.mjs
  ```

  - ここにもいくつかの注目すべき違いがあります。より詳しく見てみましょう：

    ```bash
    cat handler/consumer.mjs
    ```

    - このファイルでは、次の [@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) オブジェクトをインポートしています：
      - propagation
      - trace
      - ROOT_CONTEXT
    - これらを使用して、プロデューサー関数から伝播されたトレースコンテキストを抽出します
    - その後、抽出したトレースコンテキストに `name` と `superpower` に基づいた新しいスパン属性を追加します

#### プロデューサー関数からのトレースコンテキスト伝播

以下のコードはプロデューサー関数内で次のステップを実行します：

1. このトレース用のトレーサーを取得する
2. コンテキストキャリアオブジェクトを初期化する
3. アクティブスパンのコンテキストをキャリアオブジェクトに注入する
4. Kinesis ストリームに配置しようとしているレコードを修正し、アクティブスパンのコンテキストをコンシューマーに運ぶキャリアを含める

```js
...
import { context, propagation, trace, } from "@opentelemetry/api";
...
const tracer = trace.getTracer('lambda-app');
...
  return tracer.startActiveSpan('put-record', async(span) => {
    let carrier = {};
    propagation.inject(context.active(), carrier);
    const eventBody = Buffer.from(event.body, 'base64').toString();
    const data = "{\"tracecontext\": " + JSON.stringify(carrier) + ", \"record\": " + eventBody + "}";
    console.log(
      `Record with Trace Context added:
      ${data}`
    );

    try {
      await kinesis.send(
        new PutRecordCommand({
          StreamName: streamName,
          PartitionKey: "1234",
          Data: data,
        }),
        message = `Message placed in the Event Stream: ${streamName}`
      )
...
    span.end();
```

#### コンシューマー関数でのトレースコンテキスト抽出

以下のコードはコンシューマー関数内で次のステップを実行します：

1. `producer-lambda`から取得したコンテキストをキャリアオブジェクトに抽出する
2. 現在のコンテキストからトレーサーを抽出する
3. 抽出したコンテキスト内でトレーサーを使用して新しいスパンを開始する
4. ボーナス：メッセージからの値を含むカスタム属性など、追加の属性をスパンに追加する！
5. 完了したら、スパンを終了する

```js
import { propagation, trace, ROOT_CONTEXT } from "@opentelemetry/api";
...
      const carrier = JSON.parse( message ).tracecontext;
      const parentContext = propagation.extract(ROOT_CONTEXT, carrier);
      const tracer = trace.getTracer(process.env.OTEL_SERVICE_NAME);
      const span = tracer.startSpan("Kinesis.getRecord", undefined, parentContext);

      span.setAttribute("span.kind", "server");
      const body = JSON.parse( message ).record;
      if (body.name) {
        span.setAttribute("custom.tag.name", body.name);
      }
      if (body.superpower) {
        span.setAttribute("custom.tag.superpower", body.superpower);
      }
...
      span.end();
```

これでどのような違いが生まれるか見てみましょう！
