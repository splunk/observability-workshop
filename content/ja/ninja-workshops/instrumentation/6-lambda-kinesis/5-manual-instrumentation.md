---
title: 手動計装
linkTitle: 5. Manual Instrumentation
weight: 5
---

ワークショップの第2部では、OpenTelemetry による手動計装がテレメトリ収集の強化にどのように役立つかを説明します。具体的には、`producer-lambda` 関数から `consumer-lambda` 関数へトレースコンテキストデータを伝播できるようにします。これにより、現在自動コンテキスト伝播をサポートしていない Kinesis Stream を介しても、2つの関数間の関係を確認できるようになります。

### 手動計装ワークショップのディレクトリと内容

まず、作業ディレクトリとそのファイルを確認します。今回は `workshop/lambda/manual` ディレクトリです。ここにワークショップの手動計装部分のすべてのコンテンツが格納されています。

#### `manual` ディレクトリ

* 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します:

```bash
cd ~/workshop/lambda/manual
```

* `ls` コマンドでこのディレクトリの内容を確認します:

```bash
ls
```

* 出力には以下のファイルとディレクトリが含まれているはずです:

```bash
handler             outputs.tf          terraform.tf        variables.tf
main.tf             send_message.py     terraform.tfvars
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
このディレクトリと最初に使用した auto ディレクトリの間に違いはありますか？
{{% /notice %}}

同じように見えるファイルが、実際に同じであることを確認しましょう。

* `auto` ディレクトリと `manual` ディレクトリの `main.tf` ファイルを比較します:

```bash
diff ~/workshop/lambda/auto/main.tf ~/workshop/lambda/manual/main.tf
```

* 違いはありません！_（違いがないはずです。もし違いがある場合は、ワークショップのファシリテーターに相談してください）_

* 次に、`producer.mjs` ファイルを比較します:

```bash
diff ~/workshop/lambda/auto/handler/producer.mjs ~/workshop/lambda/manual/handler/producer.mjs
```

* かなりの違いがあります！

* ファイル全体を表示して内容を確認することをお勧めします

```bash
cat ~/workshop/lambda/manual/handler/producer.mjs
```

* 手動計装に必要なタスクを処理するために、OpenTelemetry オブジェクトを関数に直接インポートしていることに注目してください。

```js
import { context, propagation, trace, } from "@opentelemetry/api";
```

* producer 関数でコンテキストを伝播するために、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) から以下のオブジェクトをインポートしています:
  * context
  * propagation
  * trace

* 最後に、`consumer.mjs` ファイルを比較します:

 ```bash
 diff ~/workshop/lambda/auto/handler/consumer.mjs ~/workshop/lambda/manual/handler/consumer.mjs
 ```

* ここにもいくつかの注目すべき違いがあります。詳しく見てみましょう

```bash
cat handler/consumer.mjs
```

* このファイルでは、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api) から以下のオブジェクトをインポートしています:
  * propagation
  * trace
  * ROOT_CONTEXT
    * これらを使用して、producer 関数から伝播されたトレースコンテキストを抽出します
    * さらに、抽出されたトレースコンテキストに `name` と `superpower` に基づく新しいスパン属性を追加します

以下のコードは、producer 関数内で次のステップを実行します:

1. このトレースのトレーサーを取得する
2. コンテキストキャリアオブジェクトを初期化する
3. アクティブスパンのコンテキストをキャリアオブジェクトに注入する
4. Kinesis ストリームに配置するレコードを変更し、アクティブスパンのコンテキストを consumer に運ぶキャリアを含める

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

以下のコードは、consumer 関数内で次のステップを実行します:

1. `producer-lambda` から取得したコンテキストをキャリアオブジェクトに抽出する
2. 現在のコンテキストからトレーサーを抽出する
3. 抽出されたコンテキスト内でトレーサーを使用して新しいスパンを開始する
4. ボーナス: メッセージの値を使用したカスタム属性を含む、追加の属性をスパンに追加する
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

それでは、これがどのような違いを生むか見てみましょう！
