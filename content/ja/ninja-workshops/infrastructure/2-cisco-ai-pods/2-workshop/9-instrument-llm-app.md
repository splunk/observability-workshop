---
title: LLMアプリケーションの計装
linkTitle: 9. LLMアプリケーションの計装
weight: 9
time: 10 minutes
---

## OpenTelemetryによるアプリケーションの計装

### 計装パッケージ

アプリケーションからメトリクス、トレース、ログを収集するために、OpenTelemetryで計装しています。
これには、`requirements.txt` ファイルに以下のパッケージを追加する必要があります（最終的に `pip install` でインストールされます）。

````
splunk-opentelemetry==2.8.0
````

また、このアプリケーションのコンテナイメージをビルドするために使用する `Dockerfile` に、追加のOpenTelemetry計装パッケージをインストールする以下の記述を追加しました。

``` dockerfile
# Add additional OpenTelemetry instrumentation packages
RUN opentelemetry-bootstrap --action=install
```

次に、アプリケーション実行時に `opentelemetry-instrument` を呼び出すよう、`Dockerfile` の `ENTRYPOINT` を変更しました。

``` dockerfile
ENTRYPOINT ["opentelemetry-instrument", "flask", "run", "-p", "8080", "--host", "0.0.0.0"]
```

最後に、このLangChainアプリケーションからOpenTelemetryで収集されるトレースとメトリクスを強化するために、追加のSplunk計装パッケージを追加しました。

````
splunk-otel-instrumentation-langchain==0.1.4
splunk-otel-util-genai==0.1.4
````

### 環境変数

OpenTelemetryでアプリケーションを計装するために、アプリケーションのデプロイに使用するKubernetesマニフェストファイルにいくつかの環境変数を含めています。

``` yaml
  env:
    - name: OTEL_SERVICE_NAME
      value: "llm-app"
    - name: OTEL_EXPORTER_OTLP_ENDPOINT
      value: "http://splunk-otel-collector-agent:4317"
    - name: OTEL_EXPORTER_OTLP_PROTOCOL
      value: "grpc"
      # filter out health check requests to the root URL
    - name: OTEL_PYTHON_EXCLUDED_URLS
      value: "^(https?://)?[^/]+(/)?$"
    - name: OTEL_PYTHON_DISABLED_INSTRUMENTATIONS
      value: "httpx,requests"
    - name: OTEL_INSTRUMENTATION_LANGCHAIN_CAPTURE_MESSAGE_CONTENT
      value: "true"
    - name: OTEL_LOGS_EXPORTER
      value: "otlp"
    - name: OTEL_PYTHON_LOG_CORRELATION
      value: "true"
    - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
      value: "delta"
    - name: OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED
      value: "true"
    - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT
      value: "true"
    - name: OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE
      value: "SPAN_AND_EVENT"
    - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS
      value: "span_metric_event,splunk"
    - name: OTEL_INSTRUMENTATION_GENAI_EMITTERS_EVALUATION
      value: "replace-category:SplunkEvaluationResults"
    - name: SPLUNK_PROFILER_ENABLED
      value: "true"
```

注意: `OTEL_INSTRUMENTATION_LANGCHAIN_CAPTURE_MESSAGE_CONTENT` および `OTEL_INSTRUMENTATION_GENAI_*` 環境変数は、使用しているLangChain計装に固有のものです。
