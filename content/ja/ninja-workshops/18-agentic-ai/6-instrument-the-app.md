---
title: エージェント型AIアプリケーションの計装
linkTitle: 6. エージェント型AIアプリケーションの計装
weight: 6
time: 15 minutes
---

> 注意: このセクションでは複数のファイルを変更する必要があります。
> 変更箇所が不明な場合、またはアプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-instrumentation` フォルダにある
> このセクションの想定される解答を参照してください。

エージェント型AIアプリケーションをOpenTelemetryで計装し、Kubernetesにデプロイするには、
いくつかの手順が必要です:

1. `requirements.txt` ファイルに計装パッケージを追加する
2. `opentelemetry-instrument` を使用してアプリケーションを起動するようDockerfileを更新する
3. 計装パッケージを含む新しいDockerイメージをビルドする
4. 環境変数を使用してKubernetesマニフェストを更新する
5. Kubernetesマニフェストをデプロイする

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を
編集用に開き、ファイルの末尾に以下のパッケージを追加します:

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-langchain==0.1.7
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

これらのパッケージの説明は以下の通りです:

* `splunk-opentelemetry`: Splunk版のOpenTelemetry Pythonディストリビューションで、Pythonアプリケーションを計装して分散トレースをキャプチャし、Splunk APMにレポートします。
* `splunk-otel-instrumentation-langchain`: LangChain LLM/チャットワークフロー向けのOpenTelemetry計装を提供するパッケージです。
* `splunk-otel-genai-emitters-splunk`: Splunk Platformでのストレージとフィルタリングを最適化するために、Splunkスキーマの評価結果ログ用エミッターを提供するパッケージです。
* `splunk-otel-util-genai`: OpenTelemetryセマンティック規約を使用した生成AIワークロードの計装を容易にするAPIとデータ型を提供するユーティリティ関数を含むパッケージです。
* `opentelemetry-instrumentation-flask`: OpenTelemetry WSGIミドルウェアを基盤として、FlaskアプリケーションのWebリクエストを追跡するライブラリです。

{{% notice title="進む前に作業内容を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します:

```bash
diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-instrumentation/requirements.txt
```

{{% / notice %}}

## Dockerfileの更新

次に、OpenTelemetry計装を有効にする必要があります。これはDockerfileを更新して、
アプリケーションが `opentelemetry-instrument` で起動されるようにすることで実現します。`~/workshop/agentic-ai/base-app/Dockerfile`
ファイルを編集用に開き、最後の行を以下のように更新します:

```dockerfile
# Run the server with instrumentation
CMD ["opentelemetry-instrument", "python", "main.py"]
```

{{% notice title="進む前に作業内容を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します:

```bash
diff ~/workshop/agentic-ai/base-app/Dockerfile ~/workshop/agentic-ai/app-with-instrumentation/Dockerfile
```

{{% / notice %}}

### 更新されたDockerイメージのビルド

新しいタグを付けて更新されたDockerイメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-instrumentation .
docker push localhost:9999/agentic-ai-app:app-with-instrumentation
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを使用することを
> 検討してください。その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルのイメージ名を
> `localhost:9999/agentic-ai-app:app-with-instrumentation` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-instrumentation` に更新してください。

### ConfigMapの定義

アプリケーションをKubernetesにデプロイする際、テレメトリー（メトリクス、トレース、ログ）を
明確で一意な環境識別子とともにSplunk Observability Cloudに送信したいと考えています。
これにより、異なるデプロイメント間でデータのフィルタリング、比較、トラブルシューティングが容易になります。

これを実現するために、`deployment.environment` という名前のOpenTelemetryリソース属性を設定します。
値をハードコーディングする代わりに、EC2インスタンスに既に存在する `INSTANCE` 環境変数から
値を導出します。これにより、各デプロイメントが正しい環境名で自動的にタグ付けされます。

この設定をKubernetes ConfigMapに保存し、後でアプリケーションPodに環境変数として
注入できるようにします。

以下のコマンドでConfigMapを作成します:

```bash
kubectl create configmap instance-config \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-$INSTANCE \
-n travel-agent
```

このコマンドの動作:

* OpenTelemetryが期待する `OTEL_RESOURCE_ATTRIBUTES` 環境変数を定義します。
* `$INSTANCE` の値に応じて、`deployment.environment` を `agentic-ai-shw-1c43` のような値に設定します。
* `travel-agent` ネームスペースにConfigMapを作成します。

次のステップでKubernetesデプロイメントを構成する際に、このConfigMapを参照します。

### Kubernetesマニフェストの更新

OpenTelemetry計装、特にAI Agent Monitoringでは、計装データの収集、処理、エクスポートの
方法を定義する多数の環境変数を設定する必要があります。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開きます。計装を含むイメージを
使用するように**イメージタグ**を更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-instrumentation
```

同じファイルで、`Begin: Add Environment Variables` と `End: Add Environment Variables` の
コメントの間に以下の**環境変数**を追加します:

> ヒント: 貼り付ける前に `:set paste` と入力すると、`vi` が貼り付けたコードを自動インデントするのを防げます。

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
> 右上の `Copy text to clipboard` ボタンを使用して、
> すべてのテキストをコピーしたことを確認してください。

> 注意: yamlではインデントが重要です。新しい環境変数が既存の環境変数と
> 揃っていることを確認してください。

以下の環境変数はエージェント型AIモニタリングに固有のもので、説明は以下の通りです:

* `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE`: OTLPメトリクスエクスポーターが、出力するメトリクスに対して累積合計、デルタ、またはメモリ効率の良いテンポラリティのどれを報告するかを決定します。エージェント型AIモニタリングでは `DELTA` に設定することが推奨されます。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`: エージェント型AIアプリケーションからのメッセージキャプチャを有効/無効にするために使用します。このワークショップでは `true` に設定しています。
* `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT_MODE`: メッセージのキャプチャ方法を定義します。このワークショップでは `SPAN` に設定しており、スパンイベントストアを使用してメッセージがキャプチャされます。
* `OTEL_INSTRUMENTATION_GENAI_EMITTERS`: このワークショップでは `span_metric,splunk` に設定しており、スパンとメトリクスの両方のデータ、およびSplunk固有の機能がキャプチャされます。

{{% notice title="進む前に作業内容を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します:

```bash
diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-instrumentation/k8s.yaml
```

{{% / notice %}}

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでのアプリケーションテスト

新しいアプリケーションPodが正常に起動し、古いPodが存在しないことを確認します:

{{< tabs >}}
{{% tab title="コマンド" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="出力例" %}}

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
