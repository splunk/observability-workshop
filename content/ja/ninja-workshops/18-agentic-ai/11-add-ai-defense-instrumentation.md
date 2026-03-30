---
title: AI Defense 計装の追加
linkTitle: 11. AI Defense 計装の追加
weight: 11
time: 20 minutes
---

Splunk AI Security Monitoringは、Splunk Observability for AIと [Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html) を統合します。
AIエージェントのランタイムで検出された[セキュリティおよびプライバシーリスク](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita)を一元的に表示し、パフォーマンスとリスクを一箇所で監視できます。

Splunk AI Security Monitoringでは、以下のことが可能です：

* プロンプトインジェクションやPII漏洩などの検出またはブロックされたセキュリティおよびプライバシーリスクに関連するエージェント、インタラクション、サービスを特定する
* リスクの傾向をレイテンシ、エラー、その他のパフォーマンスメトリクスとともに時系列で追跡する
* トレースコンテキスト内でリスクのあるインタラクションを、特定のプロンプトとレスポンスまで掘り下げて調査する

このセクションでは、Agentic AIアプリケーションにAI Defense統合を追加し、Splunk Observability Cloudで結果のデータを確認します。

## 仕組み

Splunk AI Security Monitoringは、PythonベースのAIエージェント向けにセキュリティおよびプライバシーリスクのトレースを自動化する計装ライブラリ [opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense) を提供します。
このライブラリは、AIエージェントがLLM（OpenAIなど）やオーケストレーションフレームワーク（LangChainなど）に対して行う呼び出しにセキュリティテレメトリをキャプチャしてアタッチし、すべてのプロンプトとレスポンスがセキュリティガードレールに対して監査され、統一されたOpenTelemetryトレース内に記録されることを保証します。これは、LLMまたはワークフロースパンに `gen_ai.security.event_id attribute` を追加することで実現されます。

## SDK モード vs. Gateway モード

`opentelemetry-instrumentation-aidefense` ライブラリは、SDKモードまたはGatewayモードのいずれかで動作できます：

* SDKモードでは、開発者は `inspect_prompt()` を使用して明示的なセキュリティチェックを追加します。このオプションは、セキュリティチェックの実装方法と問題への対処方法を完全に制御したい開発者に最適です。
* Gatewayモードでは、LLM呼び出しがCisco AI Defense Gatewayを経由してプロキシされるため、アプリケーションコードの変更は不要です。このモードは、OpenAI、Anthropicなどの一般的な商用LLMでサポートされています。

このワークショップでは、Azure OpenAIでGatewayモードを使用します。

## Cisco AI Defense 統合のセットアップ

最初のステップは、[Cisco AI Defense との統合をセットアップ](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense)することです。

**Data Management -> Deployed integrations** に移動し、`AI Defense` を検索すると、この統合がすでに構成されていることがわかります：

![AI Defense Config](../images/AIDefenseConfig.png)

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を開いて編集し、以下のパッケージを追加します：

````
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
````

### 更新された Docker イメージのビルド

新しいタグを付けて更新されたDockerイメージをビルドします：

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

### Kubernetes マニフェストの更新

Kubernetesマニフェストファイルを更新する前に、AI Defense Gateway URLを保存するためのシークレットを作成しましょう：

> 注意：インストラクターがシークレット作成時に使用する実際の AI Defense URL を提供します

```bash
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-gateway-url='https://us.gateway.aidefense.security.cisco.com/{tenant}/connections/{conn}'
```

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、以下の環境変数のみが含まれていることを確認します：

> `AZURE_OPENAI_ENDPOINT` は AI Defense Gateway URL を使用するように構成されていることに注意してください。これにより、Azure OpenAI 宛てのリクエストが代わりにゲートウェイを経由して送信されます

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

同じファイルで、計装を含むイメージを使用するようにイメージを更新します：

```yaml
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

### 更新されたアプリケーションのデプロイ

マニフェストファイルを使用して、更新されたアプリケーションを以下のようにデプロイできます：

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

以下のコマンドを実行してアプリケーションをテストします。AI DefenseのPII検出をトリガーするために（偽の）クレジットカード番号を含めます：

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences. My credit card number is 4111 1111 1111 1111.",
    "travelers": 2
  }'
```

## Cisco AI Defense でのイベントの表示

AI Defenseアプリケーションに直接ログインすると、リクエストに対してイベントがログに記録され、AI Defenseがプロンプトに含めたクレジットカード番号を自動的にマスキングしたことがわかります：

![AI Defense Events](../images/AIDefenseEvents.png)

AI Defenseでは、特定のタイプのセキュリティ問題を監視するかブロックするかを指定するポリシーを構成できることに注意してください。この場合、PCI関連の問題を監視するだけに設定しています。

## Splunk Observability Cloud でのデータの表示

Splunk Observability Cloudに戻り、トレースがどのように見えるか確認しましょう。

`APM` に移動し、`Agents` を選択します。環境名が選択されていることを確認してください（例：`agentic-ai-$INSTANCE`）。ページにセキュリティリスクが含まれるようになったことがわかります！

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

`APM -> Trace Analyzer` に移動します。

環境名が選択されていることを確認してください（例：`agentic-ai-$INSTANCE`）。
新しいトレースの一つを選択します。トレースにセキュリティリスクが含まれるようになったことがわかります！
具体的には、アプリケーションで **Privacy - PCI risk** が検出された（ただしブロックされていない）ことがわかります：

![Trace with Security Risks](../images/TraceWithSecurityRisks.png)
