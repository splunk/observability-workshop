---
title: Agentic AI アプリケーションの計装
linkTitle: 6. Agentic AI アプリケーションの計装
weight: 6
time: 20 minutes
---

Agentic AIアプリケーションをOpenTelemetryで計装し、Kubernetesにデプロイするには、いくつかの手順が必要です：

1. `requirements.txt` ファイルに計装パッケージを追加する
2. `opentelemetry-instrument` を使用してアプリケーションを起動するようにDockerfileを更新する
3. 計装パッケージを含む新しいDockerイメージをビルドする
4. 環境変数を含むようにKubernetesマニフェストを更新する
5. Kubernetesマニフェストをデプロイする

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を編集用に開き、以下のパッケージを追加します：

````
deepeval
litellm==1.82.0
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
splunk-otel-util-genai-evals==0.1.8
splunk-otel-genai-evals-deepeval==0.1.13
opentelemetry-instrumentation-flask==0.59b0
````

## Dockerfile の更新

次に、コンテナイメージが `opentelemetry-instrument` で起動されるようにDockerfileを更新する必要があります。`~/workshop/agentic-ai/base-app/Dockerfile` ファイルを編集用に開き、最後の行を以下のように更新します：

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

### 更新された Docker イメージのビルド

新しいタグを付けて更新されたDockerイメージをビルドします：

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

### DeepEval 用の Secret の作成

DeepEvalの設定を保存するためのKubernetes Secretを作成します。以下のコマンドを実行する前に、Azure OpenAIエンドポイントを置き換えてください。DeepEvalのリクエストはAzure OpenAIエンドポイントに直接ルーティングされます：

```bash
kubectl create secret generic deepeval-secret -n travel-agent --from-literal=deepeval-llm-base-url=your_deepeval_llm_base_url
````

### Kubernetes マニフェストの更新

OpenTelemetryの計装、特にAI Agent Monitoringでは、計装データの収集、処理、エクスポート方法を定義するために、多くの環境変数を設定する必要があります。

Kubernetesマニフェストファイルを更新する前に、EC2インスタンスの `INSTANCE` 環境変数を使用して、Kubernetesマニフェストの `OTEL_RESOURCE_ATTRIBUTES` 環境変数を設定するConfigMapを作成しましょう：

```bash
kubectl create configmap instance-config --from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE -n travel-agent
```

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、以下の環境変数を追加します：

```yaml
            - name: DEEPEVAL_LLM_BASE_URL
              valueFrom:
                secretKeyRef:
                  name: deepeval-secret
                  key: deepeval-llm-base-url
            - name: DEEPEVAL_LLM_MODEL
              value: "gpt-4.1-mini"
            - name: DEEPEVAL_LLM_PROVIDER
              value: "azure"
            - name: DEEPEVAL_LLM_API_KEY
              valueFrom:
                secretKeyRef:
                  name: azure-openai-api
                  key: azure-openai-api-key
            - name: DEEPEVAL_LLM_EXTRA_HEADERS
              value: '{"api_version":"2024-01-01-preview"}'
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
            - name: HOME
              value: "/tmp"
            - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
              value: "DELTA"
            - name: OTEL_LOGS_EXPORTER
              value: "otlp"
            - name: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED
              value: "true"
            - name: OTEL_PYTHON_EXCLUDED_URLS
              value: "^(https?://)?[^/]+(/health)?$"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT
              value: "true"
            - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE
              value: "SPAN_AND_EVENT"
            - name: OTEL_INSTRUMENTATION_GENAI_EVALS_RESULTS_AGGREGATION
              value: "true"
            - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS
              value: "span_metric_event,splunk"
            - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS_EVALUATION
              value: "replace-category:SplunkEvaluationResults"
            - name: OTEL_GENAI_EVAL_DEBUG_SKIPS
              value: "true"
            - name: OTEL_GENAI_EVAL_DEBUG_EACH
              value: "false"
            - name: OTEL_INSTRUMENTATION_GENAI_DEBUG
              value: "false"
            - name: SPLUNK_PROFILER_ENABLED
              value: "true"
            - name: DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE
              value: "300"
            - name: DEEPEVAL_RETRY_MAX_ATTEMPTS
              value: "2"
            - name: DEEPEVAL_FILE_SYSTEM
              value: "READ_ONLY"
```

同じファイル内で、計装を含むイメージを使用するようにイメージを更新します：

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

### 更新されたアプリケーションのデプロイ

マニフェストファイルを使用して、更新されたアプリケーションをデプロイします：

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

以下のコマンドを実行してアプリケーションをテストします：

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
