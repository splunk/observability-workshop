---
title: Instrument the Agentic AI Application
linkTitle: 6. Instrument the Agentic AI Application
weight: 6
time: 15 minutes
---

> 注意: ワークショップのこのセクションでは、複数のファイルを変更する必要があります。
> どこを変更すればよいか分からない場合や、アプリケーションが
> 動作しなくなった場合は、`~/workshop/agentic-ai/app-with-instrumentation` フォルダにある
> このセクションの想定ソリューションを参照してください。

Agentic AI アプリケーションを OpenTelemetry でインストルメントして Kubernetes に
デプロイするには、いくつかの手順が必要です。

1. インストルメンテーションパッケージを `requirements.txt` ファイルに追加する
2. アプリケーションを `opentelemetry-instrument` で起動するように Dockerfile を更新する
3. インストルメンテーションパッケージを含む新しい Docker イメージをビルドする
4. 環境変数を含めて Kubernetes マニフェストを更新する
5. Kubernetes マニフェストをデプロイする

## Add Instrumentation Packages

次に、いくつかのインストルメンテーションパッケージをインストールする必要があります。
`~/workshop/agentic-ai/base-app/requirements.txt` を編集用に開き、ファイルの末尾に
以下のパッケージを追加することで、これを実現できます。

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

これらのパッケージは以下のように説明できます。

* `splunk-opentelemetry`: これは OpenTelemetry Python の Splunk ディストリビューションで、Python アプリケーションをインストルメントして分散トレースを取得し、Splunk APM へレポートします。
* `splunk-otel-instrumentation-langchain`: このパッケージは、LangChain LLM/chat ワークフロー向けの OpenTelemetry インストルメンテーションを提供します。
* `splunk-otel-genai-emitters-splunk`: このパッケージは、Splunk Platform でのストレージとフィルタリングを最適化するため、Evaluation Results ログ向けに Splunk スキーマのエミッターを提供します。
* `splunk-otel-util-genai`: このパッケージには、OpenTelemetry セマンティック規約を用いた生成 AI ワークロードのインストルメンテーションを容易にするための API およびデータ型を提供するユーティリティ関数が含まれています。
* `opentelemetry-instrumentation-flask`: このライブラリは、OpenTelemetry WSGI ミドルウェアを基盤として、Flask アプリケーションの Web リクエストを追跡します。

{{% notice title="Check your work before proceeding" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定ソリューションと比較してください。

```bash
diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-instrumentation/requirements.txt
```

{{% / notice %}}

## Update the Dockerfile

次に、OpenTelemetry インストルメンテーションを有効化する必要があります。これは、アプリケーションが
`opentelemetry-instrument` で起動されるよう Dockerfile を更新することで実現します。`~/workshop/agentic-ai/base-app/Dockerfile`
ファイルを編集用に開き、最終行を以下のように更新してください。

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

{{% notice title="Check your work before proceeding" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定ソリューションと比較してください。

```bash
diff ~/workshop/agentic-ai/base-app/Dockerfile ~/workshop/agentic-ai/app-with-instrumentation/Dockerfile
```

{{% / notice %}}

### Build an Updated Docker Image

新しいタグで更新された Docker イメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みイメージの利用を
> 検討してください。その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内の
> イメージ名を `localhost:9999/agentic-ai-app:app-with-instrumentation` から
> `ghcr.io/splunk/agentic-ai-app:app-with-instrumentation` に更新してください。

### Define the Config Map

アプリケーションを Kubernetes にデプロイするとき、テレメトリ（メトリクス、トレース、ログ）が
明確で一意の環境識別子とともに Splunk Observability Cloud に送信されるようにしたいと考えます。
これにより、異なるデプロイメント間でのデータのフィルタリング、比較、トラブルシューティングが容易になります。

これを実現するため、`deployment.environment` という名前の OpenTelemetry リソース属性を設定します。
値をハードコードするのではなく、EC2 インスタンスにすでに存在する `INSTANCE` 環境変数から
派生させます。これにより、各デプロイメントが正しい環境名で自動的にタグ付けされることが
保証されます。

この設定は Kubernetes ConfigMap に保存し、後でアプリケーション Pod に環境変数として
注入できるようにします。

以下のコマンドで ConfigMap を作成します。

```bash
kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent
```

このコマンドが行うこと:

* OpenTelemetry が想定する `OTEL_RESOURCE_ATTRIBUTES` 環境変数を定義します。
* `$INSTANCE` の値に応じて、`deployment.environment` を `agentic-ai-shw-1c43` のような値に設定します。
* `travel-agent` ネームスペースに ConfigMap を作成します。

この ConfigMap は次のステップで Kubernetes デプロイメントを設定する際に参照します。

### Update the Kubernetes Manifest

OpenTelemetry インストルメンテーション、特に AI Agent Monitoring では、インストルメンテーションデータの
収集、処理、エクスポート方法を定義する多数の環境変数を設定する必要があります。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開きます。インストルメンテーション付きの
イメージを使用するように、**image tag** を更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

同じファイル内で、`Begin: Add Environment Variables` と `End: Add Environment Variables` という
コメントの間に以下の **環境変数** を追加します。

> ヒント: 内容を貼り付ける前に `:set paste` と入力すると、`vi` が貼り付けたコードを自動インデントするのを防げます。

```yaml
            # Begin: Add Environment Variables
            # Service Name
            - name: OTEL_SERVICE_NAME
              value: "travel-planner"
            # Additional OTEL configuration
            - name: OTEL_RESOURCE_ATTRIBUTES
              valueFrom:
                configMapKeyRef:
                  name: instance-config
                  key: OTEL_RESOURCE_ATTRIBUTES
            - name: SPLUNK_OTEL_AGENT
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://$(SPLUNK_OTEL_AGENT):4317"
            - name: OTEL_EXPORTER_OTLP_PROTOCOL
              value: "grpc"
            - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
              value: "DELTA"
            - name: OTEL_PYTHON_EXCLUDED_URLS
              value: "^(https?://)?[^/]+(/health)?$"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT
              value: "true"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE
              value: "SPAN"
            - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS
              value: "span_metric,splunk"
            - name: SPLUNK_PROFILER_ENABLED
              value: "true"
            # End: Add Environment Variables
```

> 注意: スクロールしないと表示されないテキストがある場合があります。
> すべてのテキストをコピーしたことを確認するため、右上隅の
> `Copy text to clipboard` ボタンを使用してください。

> 注意: yaml ではインデントが重要です。新しい環境変数が
> 既存の環境変数と揃っていることを確認してください。

以下の環境変数は Agentic AI モニタリングに固有のものであり、
以下のように説明できます。

* `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`: これは、OTLP メトリクスエクスポーターが、エクスポートされるメトリクスについて累積合計、デルタ、または低メモリ向けの temporality を報告するかを決定します。Agentic AI モニタリングでは `DELTA` に設定することが推奨されます。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: これは、Agentic AI アプリケーションからのメッセージキャプチャを有効/無効にするために使用します。本ワークショップでは `true` に設定しています。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE`: これは、メッセージをどのようにキャプチャするかを定義します。本ワークショップでは `SPAN` に設定しており、これによりメッセージは span event store を使用してキャプチャされます。
* `OTEL_INSTRUMENTATION_GENAI_EMITTERS`: 本ワークショップでは `span_metric,splunk` に設定しており、これにより span とメトリクスデータの両方、および Splunk 固有の機能がキャプチャされるようになります。

{{% notice title="Check your work before proceeding" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定ソリューションと比較してください。

```bash
diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-instrumentation/k8s.yaml
```

{{% / notice %}}

### Deploy the Updated Application

以下のように、マニフェストファイルを使用して更新したアプリケーションをデプロイできます。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

新しいアプリケーション Pod が正常に起動し、古い Pod が存在しなくなったことを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
````

{{% /tab %}}
{{< /tabs >}}

次に、以下のコマンドを実行してアプリケーションをテストします。

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```

## Troubleshooting

トラブルシューティングが必要な場合は、以下のコマンドでアプリケーションログを表示できます。

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```
