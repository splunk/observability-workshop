---
title: 手動インストルメンテーション
linkTitle: 4. 手動インストルメンテーション
weight: 4
---

ワークショップの2つ目のパートでは、OpenTelemetryによる手動インストルメンテーションがどのようにテレメトリ収集を強化するのかを示すことに焦点を当てます。具体的には、`producer-lambda` 関数から `consumer-lambda` 関数へトレースコンテキストデータを伝播させ、現在自動コンテキスト伝播をサポートしていない Kinesis Stream をまたいでも、2つの関数間の関係を確認できるようにします。

### 手動インストルメンテーションワークショップのディレクトリと内容

ここでも、まず作業ディレクトリとそのファイルを確認することから始めます。今回は `workshop/lambda/manual` ディレクトリです。これがワークショップの手動インストルメンテーション部分のすべてのコンテンツが格納されている場所です。

#### `manual` ディレクトリ

- 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します：

  ```bash
  cd ~/workshop/lambda/manual
  ```

- `ls` コマンドでこのディレクトリの内容を確認します：

  ```bash
  ls
  ```

  - _出力には以下のファイルとディレクトリが含まれているはずです：_

    ```bash
    handler             outputs.tf          terraform.tf        variables.tf
    main.tf             send_message.py     terraform.tfvars
    ```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
このディレクトリと、最初に作業した auto ディレクトリとの間に違いはありますか？
{{% /notice %}}

#### `auto` と `manual` のファイルを比較する

見た目が同じこれらのファイルが、実際に同じであるかを確認しましょう。

- `auto` と `manual` ディレクトリの `main.tf` ファイルを比較します：

  ```bash
  diff ~/workshop/lambda/auto/main.tf ~/workshop/lambda/manual/main.tf
  ```

  - 違いはありません！ _（あってはなりません。もし違いがある場合は、ワークショップのファシリテーターにご相談ください）_

- 次に、`producer.mjs` ファイルを比較してみましょう：

  ```bash
  diff ~/workshop/lambda/auto/handler/producer.mjs ~/workshop/lambda/manual/handler/producer.mjs
  ```

  - ここにはかなりの違いがあります！

- ファイル全体を表示してその内容を確認したい場合があります

  ```bash
  cat ~/workshop/lambda/manual/handler/producer.mjs
  ```

  - 必要となる手動インストルメンテーションタスクの一部を処理するために、いくつかの OpenTelemetry オブジェクトを関数に直接インポートしていることに注目してください。

  ```js
  import { context, propagation, trace, } from "@opentelemetry/api";
  ```

  - producer 関数内でコンテキストを伝播させるために、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) から以下のオブジェクトをインポートしています：
    - context
    - propagation
    - trace

- 最後に、`consumer.mjs` ファイルを比較します：

  ```bash
  diff ~/workshop/lambda/auto/handler/consumer.mjs ~/workshop/lambda/manual/handler/consumer.mjs
  ```

  - こちらにも注目すべき違いがいくつかあります。詳しく見てみましょう

    ```bash
    cat handler/consumer.mjs
    ```

    - このファイルでは、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) から以下のオブジェクトをインポートしています：
      - propagation
      - trace
      - ROOT_CONTEXT
    - これらを使って、producer 関数から伝播されたトレースコンテキストを抽出します
    - その後、抽出されたトレースコンテキストに対して、`name` と `superpower` に基づく新しいスパン属性を追加します

#### Producer 関数からのトレースコンテキスト伝播

下記のコードは、producer 関数の内部で以下のステップを実行します：

1. このトレース用の tracer を取得する
2. コンテキストキャリアオブジェクトを初期化する
3. アクティブなスパンのコンテキストをキャリアオブジェクトに注入する
4. Kinesis ストリームに送信しようとしているレコードを変更し、アクティブスパンのコンテキストを consumer に伝えるキャリアを含める

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

#### Consumer 関数でのトレースコンテキストの抽出

下記のコードは、consumer 関数の内部で以下のステップを実行します：

1. `producer-lambda` から取得したコンテキストをキャリアオブジェクトに抽出する。
2. 現在のコンテキストから tracer を抽出する。
3. 抽出されたコンテキスト内で tracer を使って新しいスパンを開始する。
4. ボーナス：メッセージの値から取得したカスタム属性を含む追加の属性をスパンに追加する！
5. 完了したらスパンを終了する。

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

それでは、これによってどのような違いが生まれるかを見ていきましょう！
