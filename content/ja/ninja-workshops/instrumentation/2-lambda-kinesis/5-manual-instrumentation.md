---
title: 手動計装
linkTitle: 5. 手動計装
weight: 5
---

ワークショップの第2部では、OpenTelemetryによる手動計装がテレメトリ収集をどのように強化できるかを示します。具体的には、`producer-lambda`関数から `consumer-lambda`関数へトレースコンテキストデータを伝搬できるようになり、現在自動コンテキスト伝搬をサポートしていないKinesis Streamを跨いでも、2つの関数間の関係を確認できるようになります。

### 手動計装ワークショップのディレクトリと内容

まず、作業ディレクトリといくつかのファイルを確認します。今回は `workshop/lambda/manual` ディレクトリです。ここにワークショップの手動計装パートのすべてのコンテンツが格納されています。

#### `manual` ディレクトリ

* 以下のコマンドを実行して `workshop/lambda/manual` ディレクトリに移動します

```bash
cd ~/workshop/lambda/manual
```

* `ls` コマンドでこのディレクトリの内容を確認します

```bash
ls
```

* 出力には以下のファイルとディレクトリが含まれます

```bash
handler             outputs.tf          terraform.tf        variables.tf
main.tf             send_message.py     terraform.tfvars
```

{{% notice title="ワークショップの質問" style="tip" icon="question" %}}
このディレクトリと最初に使用したautoディレクトリの間に違いはありますか？
{{% /notice %}}

同じように見えるファイルが、実際に同じかどうか確認しましょう。

* `auto` と `manual` ディレクトリの `main.tf` ファイルを比較します

```bash
diff ~/workshop/lambda/auto/main.tf ~/workshop/lambda/manual/main.tf
```

* 違いはありません！ _（違いがないはずです。もし違いがある場合は、ワークショップのファシリテーターに確認してください）_

* 次に、`producer.mjs` ファイルを比較します

```bash
diff ~/workshop/lambda/auto/handler/producer.mjs ~/workshop/lambda/manual/handler/producer.mjs
```

* かなり多くの違いがあります！

* ファイル全体を表示して内容を確認することもできます

```bash
cat ~/workshop/lambda/manual/handler/producer.mjs
```

* 手動計装に必要なタスクを処理するために、OpenTelemetryオブジェクトを関数に直接インポートしていることに注目してください。

```js
import { context, propagation, trace, } from "@opentelemetry/api";
```

* producer関数でコンテキストを伝搬するために、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api)から以下のオブジェクトをインポートしています
  * context
  * propagation
  * trace

* 最後に、`consumer.mjs` ファイルを比較します

 ```bash
 diff ~/workshop/lambda/auto/handler/consumer.mjs ~/workshop/lambda/manual/handler/consumer.mjs
 ```

* ここにもいくつかの注目すべき違いがあります。詳しく見てみましょう

```bash
cat handler/consumer.mjs
```

* このファイルでは、[@opentelemetry/api](https://www.npmjs.com/package/@opentelemetry/api)から以下のオブジェクトをインポートしています
  * propagation
  * trace
  * ROOT_CONTEXT
    * これらを使用して、producer関数から伝搬されたトレースコンテキストを抽出します
    * さらに、抽出したトレースコンテキストに `name` と `superpower` に基づく新しいSpan属性を追加します

以下のコードは、producer関数内で次のステップを実行します

1. このトレースのtracerを取得する
2. コンテキストキャリアオブジェクトを初期化する
3. アクティブなSpanのコンテキストをキャリアオブジェクトに注入する
4. Kinesis Streamに配置するレコードを変更して、アクティブなSpanのコンテキストをconsumerに運ぶキャリアを含める

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

#### Consumer関数でのトレースコンテキストの抽出

以下のコードは、consumer関数内で次のステップを実行します

1. `producer-lambda` から取得したコンテキストをキャリアオブジェクトに抽出する
2. 現在のコンテキストからtracerを抽出する
3. 抽出したコンテキスト内でtracerを使用して新しいSpanを開始する
4. ボーナス: メッセージの値を使用したカスタム属性を含む、追加の属性をSpanに追加する
5. 完了したら、Spanを終了する

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

では、これがどのような違いを生むか見てみましょう！
