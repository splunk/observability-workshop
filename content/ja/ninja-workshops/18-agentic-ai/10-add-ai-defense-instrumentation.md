---
title: AI Defense 計装の追加
linkTitle: 10. AI Defense 計装の追加
weight: 10
time: 15 minutes
---

Splunk Observability Cloud は
[Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html)
と統合し、AI エージェントの実行時に検出された[セキュリティおよびプライバシーリスク](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita)を統合的に可視化することで、パフォーマンスとリスクを一箇所で監視できるようにします。

これは **Splunk AI Security Monitoring** と呼ばれ、以下のことに役立ちます

* プロンプトインジェクションや PII 漏洩などの検出またはブロックされたセキュリティおよびプライバシーリスクに関係するエージェント、インタラクション、サービスを特定する
* リスクの傾向をレイテンシ、エラー、その他のパフォーマンスメトリクスと共に時系列で追跡する
* 特定のプロンプトとレスポンスに至るまで、トレースコンテキスト内でリスクのあるインタラクションを調査する

このセクションでは、Agentic AI アプリケーションに AI Defense 統合を追加し、
Splunk Observability Cloud で結果のデータを確認します。

## 仕組み

Splunk AI Security Monitoring は、Python ベースの AI エージェント向けにセキュリティおよびプライバシーリスクのトレーシングを自動化する計装ライブラリ
[opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense)
を提供します。
このライブラリは、AI エージェントが LLM（OpenAI など）やオーケストレーションフレームワーク（LangChain など）に対して行う呼び出しにセキュリティテレメトリをキャプチャして付加し、すべてのプロンプトとレスポンスがセキュリティガードレールに対して監査され、統一された OpenTelemetry トレース内に記録されることを保証します。これは LLM またはワークフロースパンに `gen_ai.security.event_id attribute` を追加することで実現されます。

## SDK モード vs. Gateway モード

`opentelemetry-instrumentation-aidefense` ライブラリは、SDK モードまたは Gateway モードのいずれかで動作できます

* SDK モードでは、開発者が `inspect_prompt()` を使用して明示的なセキュリティチェックを追加します。このオプションは、セキュリティチェックの実装方法と問題への対処方法を完全に制御したい開発者に最適です。
* Gateway モードでは、LLM 呼び出しが Cisco AI Defense Gateway を経由してプロキシされるため、アプリケーションコードの変更は不要です。このモードは、OpenAI、Anthropic などの人気のある商用 LLM でサポートされています。

このワークショップでは、Azure OpenAI を使用した Gateway モードを利用します。

## Cisco AI Defense 統合のセットアップ

最初のステップは、[Cisco AI Defense との統合をセットアップする](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense)ことです。

**Data Management -> Deployed integrations** に移動し、`AI Defense` を検索すると、
この統合がすでに設定されていることがわかります

![AI Defense Config](../images/AIDefenseConfig.png)

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。これは
`~/workshop/agentic-ai/base-app/requirements.txt` を編集用に開き、
以下のパッケージを追加することで実現できます

````
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
````

### 更新された Docker イメージのビルド

新しいタグを使用して更新された Docker イメージをビルドします

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

### Kubernetes マニフェストの更新

Kubernetes マニフェストファイルを更新する前に、
AI Defense Gateway URL を保存するためのシークレットを作成しましょう

> 注：シークレットの作成時に使用する実際の AI Defense URL はインストラクターから提供されます

```bash
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-gateway-url='https://us.gateway.aidefense.security.cisco.com/{tenant}/connections/{conn}'
```

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、
以下の環境変数のみが含まれていることを確認します

> `AZURE_OPENAI_ENDPOINT` は AI Defense Gateway URL を使用するように設定されており、
> Azure OpenAI 宛てのリクエストが代わりにゲートウェイを経由して送信されることを保証します

```yaml
            - name: AZURE_OPENAI_DEPLOYMENT_NAME
              value: "gpt-4.1-mini"
            - name: AZURE_OPENAI_ENDPOINT
              valueFrom:
                secretKeyRef:
                  name: ai-defense-secret
                  key: ai-defense-gateway-url
            - name: AZURE_OPENAI_API_VERSION
              value: "2024-12-01-preview"
            - name: AZURE_OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: azure-openai-api
                  key: azure-openai-api-key
            # OpenAI Model
            - name: OPENAI_MODEL
              value: "gpt-4.1-mini"
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
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して更新されたアプリケーションをデプロイできます

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションテスト

新しいアプリケーション Pod が正常に起動し、古い Pod がなくなっていることを確認します。

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

今のところは、アプリケーションがまだ動作していることを確認するだけです。次のセクションでは、
セキュリティリスクを追加し、それがどのように検出されるかを示します。
