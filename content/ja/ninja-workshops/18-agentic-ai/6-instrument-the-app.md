---
title: Agentic AI アプリケーションの計装
linkTitle: 6. Agentic AI アプリケーションの計装
weight: 6
time: 15 minutes
---

Agentic AI アプリケーションを OpenTelemetry で計装し、Kubernetes にデプロイするにはいくつかの手順が必要です

1. `requirements.txt` ファイルに計装パッケージを追加する
2. `opentelemetry-instrument` を使用してアプリケーションを起動するように Dockerfile を更新する
3. 計装パッケージを含む新しい Docker イメージをビルドする
4. 環境変数を使用して Kubernetes マニフェストを更新する
5. Kubernetes マニフェストをデプロイする

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を開いて編集し、ファイルの末尾に以下のパッケージを追加します

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

これらのパッケージは以下のように説明できます

* `splunk-opentelemetry`: これは Splunk Distribution of OpenTelemetry Python であり、Python アプリケーションを計装して分散トレースをキャプチャし、Splunk APM に報告します。
* `splunk-otel-instrumentation-langchain`: このパッケージは LangChain LLM/チャットワークフローの OpenTelemetry 計装を提供します。
* `splunk-otel-genai-emitters-splunk`: このパッケージは Splunk Platform でのストレージとフィルタリングを最適化するために、Evaluation Results ログの Splunk スキーマ用エミッターを提供します。
* `splunk-otel-util-genai`: このパッケージには、OpenTelemetry セマンティック規約を使用して生成 AI ワークロードの計装を容易にするための API とデータ型を提供するユーティリティ関数が含まれています。
* `opentelemetry-instrumentation-flask`: このライブラリは OpenTelemetry WSGI ミドルウェアを基盤として、Flask アプリケーションの Web リクエストを追跡します。

## Dockerfile の更新

次に、OpenTelemetry 計装を有効にする必要があります。これは Dockerfile を更新して、アプリケーションが `opentelemetry-instrument` で起動されるようにすることで行います。`~/workshop/agentic-ai/base-app/Dockerfile` ファイルを開いて編集し、最後の行を以下のように更新します

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

### 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

### ConfigMap の定義

アプリケーションを Kubernetes にデプロイする際、テレメトリ（メトリクス、トレース、ログ）を明確で一意の環境識別子とともに Splunk Observability Cloud に送信したいと考えています。これにより、異なるデプロイメント間でデータをフィルタリング、比較、トラブルシューティングすることが容易になります。

これを行うために、`deployment.environment` という名前の OpenTelemetry リソース属性を設定します。値をハードコーディングするのではなく、EC2 インスタンスにすでに存在する `INSTANCE` 環境変数から値を導出します。これにより、各デプロイメントが正しい環境名で自動的にタグ付けされます。

この設定を Kubernetes ConfigMap に保存し、後でアプリケーション Pod に環境変数として注入できるようにします。

以下のコマンドで ConfigMap を作成します

```bash
kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent
```

このコマンドが行うこと

* OpenTelemetry が期待する `OTEL_RESOURCE_ATTRIBUTES` 環境変数を定義します。
* `$INSTANCE` の値に応じて、`deployment.environment` を `agentic-ai-shw-1c43` のような値に設定します。
* `travel-agent` namespace に ConfigMap を作成します。

次のステップで Kubernetes デプロイメントを設定する際に、この ConfigMap を参照します。

### Kubernetes マニフェストの更新

OpenTelemetry 計装、特に AI Agent Monitoring には、計装データの収集、処理、およびエクスポート方法を定義するいくつかの環境変数を設定する必要があります。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、以下の環境変数を追加します

```yaml
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
```

同じファイルで、計装を含むイメージを使用するようにイメージを更新します

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

以下の環境変数は Agentic AI モニタリングに固有のものであり、次のように説明できます

* `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`: これは OTLP メトリクスエクスポーターが、出力されるメトリクスに対して累積合計、デルタ、またはメモリ効率の良い時間性のいずれを報告するかを決定します。Agentic AI モニタリングには `DELTA` に設定することが推奨されます。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: これは Agentic AI アプリケーションからのメッセージキャプチャを有効/無効にするために使用されます。このワークショップでは `true` に設定しています。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE`: これはメッセージのキャプチャ方法を定義します。このワークショップでは `SPAN` に設定しており、メッセージがスパンイベントストアを使用してキャプチャされるようにしています。
* `OTEL_INSTRUMENTATION_GENAI_EMITTERS`: このワークショップでは `span_metric,splunk` に設定しており、スパンとメトリクスの両方のデータ、および Splunk 固有の機能がキャプチャされるようにしています。

### 更新されたアプリケーションのデプロイ

マニフェストファイルを使用して、更新されたアプリケーションを以下のようにデプロイできます

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

新しいアプリケーション Pod が正常に起動し、古い Pod が存在しないことを確認します

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

次に、以下のコマンドを実行してアプリケーションをテストします

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
