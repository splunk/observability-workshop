---
title: Agentic AIアプリケーションの計装
linkTitle: 6. Agentic AIアプリケーションの計装
weight: 6
time: 15 minutes
---

> [!NOTE]
> ワークショップのこのセクションでは、複数のファイルを変更する必要があります。
> 変更箇所がわからない場合や、アプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-instrumentation` フォルダにある
> このセクションの想定される解答を参照してください。

Agentic AIアプリケーションをOpenTelemetryで計装し、Kubernetesにデプロイするには、いくつかの手順が必要です。

1. `requirements.txt` ファイルに計装パッケージを追加する
2. `opentelemetry-instrument` を使用してアプリケーションを起動するようにDockerfileを更新する
3. 計装パッケージを含む新しいDockerイメージをビルドする
4. 環境変数を使用してKubernetesマニフェストを更新する
5. Kubernetesマニフェストをデプロイする

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を開き、ファイルの末尾に以下のパッケージを追加します。

```text
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
```

各パッケージの説明は以下のとおりです。

* `splunk-opentelemetry`: Splunk版OpenTelemetry Pythonディストリビューションで、Pythonアプリケーションを計装し、分散トレースをキャプチャしてSplunk APMにレポートします。
* `splunk-otel-instrumentation-langchain`: LangChain LLM/チャットワークフローにOpenTelemetry計装を提供するパッケージです。
* `splunk-otel-genai-emitters-splunk`: Splunk Platformでのストレージとフィルタリングを最適化するため、Evaluation Resultsログ用のSplunkスキーマのエミッターを提供するパッケージです。
* `splunk-otel-util-genai`: OpenTelemetryセマンティック規約を使用した生成AIワークロードの計装を容易にするAPIとデータ型を提供するユーティリティ関数を含むパッケージです。
* `opentelemetry-instrumentation-flask`: OpenTelemetry WSGIミドルウェアを基に、FlaskアプリケーションのWebリクエストを追跡するライブラリです。

{{% notice title="次に進む前に作業内容を確認" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します。

```bash
diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-instrumentation/requirements.txt
```

{{% / notice %}}

## Dockerfileの更新

次に、OpenTelemetry計装を有効にする必要があります。これは、`opentelemetry-instrument` を使用してアプリケーションが起動されるようにDockerfileを更新することで実現します。`~/workshop/agentic-ai/base-app/Dockerfile` を開き、最後の行を以下のように更新します。

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

{{% notice title="次に進む前に作業内容を確認" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します。

```bash
diff ~/workshop/agentic-ai/base-app/Dockerfile ~/workshop/agentic-ai/app-with-instrumentation/Dockerfile
```

{{% / notice %}}

### 更新されたDockerイメージのビルド

新しいタグで更新されたDockerイメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、ビルド済みイメージの使用を検討してください。
> その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルのイメージ名を
> `localhost:9999/agentic-ai-app:app-with-instrumentation` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-instrumentation` に更新します。

### ConfigMapの定義

アプリケーションをKubernetesにデプロイする際、テレメトリ（メトリクス、トレース、ログ）が明確でユニークな環境識別子とともにSplunk Observability Cloudに送信されるようにします。これにより、異なるデプロイメント間でデータのフィルタリング、比較、トラブルシューティングが容易になります。

これを実現するために、`deployment.environment` というOpenTelemetryリソース属性を設定します。値をハードコードする代わりに、EC2インスタンスに既に存在する `INSTANCE` 環境変数から値を取得します。これにより、各デプロイメントに正しい環境名が自動的にタグ付けされます。

この設定をKubernetes ConfigMapに保存し、後でアプリケーションPodに環境変数として注入します。

以下のコマンドでConfigMapを作成します。

```bash
kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent
```

このコマンドの動作は以下のとおりです。

* OpenTelemetryが期待する `OTEL_RESOURCE_ATTRIBUTES` 環境変数を定義します。
* `$INSTANCE` の値に応じて、`deployment.environment` を `agentic-ai-shw-1c43` のような値に設定します。
* `travel-agent` ネームスペースにConfigMapを作成します。

次のステップでKubernetesデプロイメントを設定する際に、このConfigMapを参照します。

### Kubernetesマニフェストの更新

OpenTelemetry計装、特にAI Agentモニタリングでは、計装データの収集、処理、エクスポート方法を定義するために多数の環境変数を設定する必要があります。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開きます。計装を含むイメージを使用するように **イメージタグ** を更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

同じファイルで、`Begin: Add Environment Variables` と `End: Add Environment Variables` のコメントの間に以下の **環境変数** を追加します。

> ヒント: 貼り付け前に `:set paste` と入力すると、`vi` による自動インデントを防止できます。

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

> [!NOTE]
> スクロールしないとテキストの一部が表示されない場合があります。
> 右上の `Copy text to clipboard` ボタンを使用して、
> すべてのテキストがコピーされていることを確認してください。
> yamlではインデントが重要です。新しい環境変数が既存の環境変数と揃っていることを確認してください。

以下の環境変数はAgentic AIモニタリングに固有のもので、説明は以下のとおりです。

* `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`: OTLPメトリクスエクスポーターが累積合計、デルタ、またはメモリ効率の良いテンポラリティのいずれで出力メトリクスを報告するかを決定します。Agentic AIモニタリングでは `DELTA` に設定することが推奨されます。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: Agentic AIアプリケーションからのメッセージキャプチャを有効/無効にするために使用します。このワークショップでは `true` に設定しています。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE`: メッセージのキャプチャ方法を定義します。このワークショップでは `SPAN` に設定しており、Spanイベントストアを使用してメッセージがキャプチャされます。
* `OTEL_INSTRUMENTATION_GENAI_EMITTERS`: このワークショップでは `span_metric,splunk` に設定しており、SpanとMetricデータの両方、およびSplunk固有の機能がキャプチャされます。

{{% notice title="次に進む前に作業内容を確認" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します。

```bash
diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-instrumentation/k8s.yaml
```

{{% / notice %}}

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイします。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでのアプリケーションテスト

新しいアプリケーションPodが正常に起動し、古いPodが存在しないことを確認します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
```

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

## トラブルシューティング

トラブルシューティングが必要な場合は、以下のコマンドでアプリケーションログを確認します。

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```
