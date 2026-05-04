---
title: Agentic AI アプリケーションの計装
linkTitle: 6. Agentic AI アプリケーションの計装
weight: 6
time: 15 minutes
---

> 注意: このセクションでは複数のファイルを変更する必要があります。
> 変更箇所がわからない場合やアプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-instrumentation` フォルダにある
> モデルソリューションを参照してください。

Agentic AI アプリケーションを OpenTelemetry で計装し、Kubernetes にデプロイするには、いくつかの手順が必要です:

1. `requirements.txt` ファイルに計装パッケージを追加する
2. `opentelemetry-instrument` を使用してアプリケーションを起動するように Dockerfile を更新する
3. 計装パッケージを含む新しい Docker イメージをビルドする
4. 環境変数を含むように Kubernetes マニフェストを更新する
5. Kubernetes マニフェストをデプロイする

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を開いて編集し、ファイルの末尾に以下のパッケージを追加します:

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

各パッケージの説明は以下のとおりです:

* `splunk-opentelemetry`: Splunk Distribution of OpenTelemetry Python です。Python アプリケーションを計装し、分散トレースをキャプチャして Splunk APM にレポートします。
* `splunk-otel-instrumentation-langchain`: LangChain の LLM/チャットワークフロー向けの OpenTelemetry 計装を提供するパッケージです。
* `splunk-otel-genai-emitters-splunk`: Splunk Platform でのストレージとフィルタリングを最適化するために、Evaluation Results ログの Splunk スキーマ用エミッターを提供するパッケージです。
* `splunk-otel-util-genai`: OpenTelemetry セマンティック規約を使用した生成 AI ワークロードの計装を容易にする API とデータ型を提供するユーティリティ関数を含むパッケージです。
* `opentelemetry-instrumentation-flask`: OpenTelemetry WSGI ミドルウェアを基盤として、Flask アプリケーションの Web リクエストを追跡するライブラリです。

> ヒント: 以下のコマンドを実行して、変更内容をモデルソリューションと比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-instrumentation/requirements.txt`

## Dockerfile の更新

次に、OpenTelemetry 計装を有効にする必要があります。これは、`opentelemetry-instrument` を使用してアプリケーションが起動されるように Dockerfile を更新することで行います。`~/workshop/agentic-ai/base-app/Dockerfile` ファイルを開いて編集し、最後の行を以下のように更新します:

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

> ヒント: 以下のコマンドを実行して、変更内容をモデルソリューションと比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/Dockerfile ~/workshop/agentic-ai/app-with-instrumentation/Dockerfile`

### 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

### ConfigMap の定義

アプリケーションを Kubernetes にデプロイする際、テレメトリー（メトリクス、トレース、ログ）を明確でユニークな環境識別子とともに Splunk Observability Cloud に送信したいと考えます。これにより、異なるデプロイメント間でのフィルタリング、比較、トラブルシューティングが容易になります。

これを実現するために、`deployment.environment` という名前の OpenTelemetry リソース属性を設定します。値をハードコーディングする代わりに、EC2 インスタンスに既に存在する `INSTANCE` 環境変数から値を導出します。これにより、各デプロイメントに正しい環境名が自動的にタグ付けされます。

この設定は Kubernetes ConfigMap に保存し、後でアプリケーション Pod に環境変数として注入できるようにします。

以下のコマンドで ConfigMap を作成します:

```bash
kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent
```

このコマンドが行うこと:

* OpenTelemetry が期待する `OTEL_RESOURCE_ATTRIBUTES` 環境変数を定義します。
* `$INSTANCE` の値に応じて、`deployment.environment` を `agentic-ai-shw-1c43` のような値に設定します。
* `travel-agent` namespace に ConfigMap を作成します。

次のステップで Kubernetes デプロイメントを設定する際に、この ConfigMap を参照します。

### Kubernetes マニフェストの更新

OpenTelemetry 計装、特に AI Agent Monitoring には、計装データの収集、処理、エクスポートの方法を定義する多数の環境変数の設定が必要です。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集します。計装を含むイメージを使用するように**イメージタグ**を更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

同じファイルで、`Begin: Add Environment Variables` と `End: Add Environment Variables` のコメントの間に以下の**環境変数**を追加します:

> ヒント: 貼り付ける前に `:set paste` と入力すると、`vi` がコードを自動インデントするのを防げます。

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

> 注意: スクロールしないとテキストの一部が表示されない場合があります。
> 右上の `Copy text to clipboard` ボタンを使用して、すべてのテキストをコピーしてください。

> 注意: YAML ではインデントが重要です。新しい環境変数が既存の環境変数と揃っていることを確認してください。

以下の環境変数は Agentic AI モニタリングに固有のもので、説明は以下のとおりです:

* `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`: OTLP メトリクスエクスポーターが、出力するメトリクスについて累積合計、デルタ、またはメモリ効率の良いテンポラリティのどれをレポートするかを決定します。Agentic AI モニタリングでは `DELTA` に設定することが推奨されます。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: Agentic AI アプリケーションからのメッセージキャプチャを有効/無効にするために使用します。このワークショップでは `true` に設定しています。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE`: メッセージのキャプチャ方法を定義します。このワークショップでは `SPAN` に設定しており、span イベントストアを使用してメッセージがキャプチャされるようにしています。
* `OTEL_INSTRUMENTATION_GENAI_EMITTERS`: このワークショップでは `span_metric,splunk` に設定しており、span とメトリクスの両方のデータ、および Splunk 固有の機能がキャプチャされるようにしています。

> ヒント: 以下のコマンドを実行して、変更内容をモデルソリューションと比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-instrumentation/k8s.yaml`

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

新しいアプリケーション Pod が正常に起動し、古い Pod がなくなっていることを確認します:

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

次に、以下のコマンドを実行してアプリケーションをテストします:

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

## トラブルシューティング

トラブルシューティングが必要な場合は、以下のコマンドを使用してアプリケーションログを確認します:

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```
