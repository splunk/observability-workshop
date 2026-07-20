---
title: AI Defense計装の追加
linkTitle: 10. AI Defense計装の追加
weight: 10
time: 15 minutes
---

> [!NOTE]
> ワークショップのこのセクションでは、複数のファイルを変更する必要があります。
> どこを変更すればよいかわからない場合や、アプリケーションが
> 動作しなくなった場合は、このセクションの想定される解答である
> `~/workshop/agentic-ai/app-with-ai-defense` フォルダを参照してください。

Splunk Observability Cloudは
[Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html)
と統合し、AIエージェントのランタイムで検出された[セキュリティおよびプライバシーリスク](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita)の統合ビューを提供します。これにより、パフォーマンスとリスクを一箇所でモニタリングできます。

これは **Splunk AI Security Monitoring** と呼ばれ、以下のことが可能になります。

* プロンプトインジェクションやPII漏洩など、検出またはブロックされたセキュリティおよびプライバシーリスクに関与するエージェント、インタラクション、サービスを特定する
* リスクの傾向をレイテンシ、エラー、その他のパフォーマンスメトリクスと並べて時系列で追跡する
* リスクのあるインタラクションをTraceコンテキストで調査し、特定のプロンプトとレスポンスまで掘り下げる

このセクションでは、Agentic AIアプリケーションにAI Defense統合を追加し、Splunk Observability Cloudで生成されたデータを確認します。

## 仕組み

Splunk AI Security Monitoringは、Pythonベースの AIエージェント向けにセキュリティおよびプライバシーリスクのトレーシングを自動化する計装ライブラリ
[opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense)
を提供します。
このライブラリは、AIエージェントがLLM（OpenAIなど）やオーケストレーションフレームワーク（LangChainなど）に対して行う呼び出しにセキュリティテレメトリをキャプチャしてアタッチします。これにより、すべてのプロンプトとレスポンスをセキュリティガードレールに対して監査し、統合されたOpenTelemetry Traceに記録できます。これはLLMまたはワークフローのSpanに `gen_ai.security.event_id attribute` を追加することで実現されます。

## SDKモード vs. Gatewayモード

`opentelemetry-instrumentation-aidefense` ライブラリは、SDKモードまたはGatewayモードのいずれかで動作できます。

* SDKモードでは、開発者が `inspect_prompt()` を使用して明示的にセキュリティチェックを追加します。このオプションは、セキュリティチェックの実装方法と問題への対処方法を完全に制御したい開発者に最適です。
* Gatewayモードでは、LLM呼び出しがCisco AI Defense Gatewayを経由してプロキシされるため、アプリケーションコードの変更は不要です。このモードは、OpenAI、Anthropicなどの一般的な商用LLMでサポートされています。

このワークショップでは、Azure OpenAIでSDKモードを使用します。

## Cisco AI Defense統合のセットアップ

最初のステップは、[Cisco AI Defenseとの統合をセットアップ](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense)することです。

**Data Management -> Deployed integrations** に移動して `AI Defense` を検索すると、この統合がすでに設定されていることが確認できます。

> [!NOTE]
> この統合を表示するには `aiDefenseIntegration` フィーチャーフラグを有効にする必要があります

![AI Defense Config](../images/AIDefenseConfig.png)

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を開いて編集し、以下のパッケージを追加します。

```text
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
```

{{% notice title="次に進む前に確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します。

```bash
diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-ai-defense/requirements.txt
```

{{% / notice %}}

## AI Defense SDKのインポート

アプリケーションを変更して、エージェントにCisco AI Defense保護を追加しましょう。

`~/workshop/agentic-ai/base-app/main.py` ファイルを開いて編集します。

`Begin: Initialize AI Defense` と `End: Initialize AI Defense` の行の間に、AI Defense保護のインポートと有効化を追加します。

```python
# Begin: Initialize AI Defense

from aidefense.runtime import agentsec
agentsec.protect(
    api_mode={
        "llm": {
            "mode": "monitor",    # "enforce" to block violations, "monitor" to log only
            "endpoint": os.environ["AI_DEFENSE_API_MODE_LLM_ENDPOINT"],
            "api_key": os.environ["AI_DEFENSE_API_MODE_LLM_API_KEY"],
        }
    }
)

# End: Initialize AI Defense
```

> [!IMPORTANT]
> 保護のインポートと有効化は、`langchain_openai` などのLLMクライアントパッケージをインポートする前に行う必要があります

{{% notice title="次に進む前に確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します。

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-ai-defense/main.py
```

{{% / notice %}}

### 更新されたDockerイメージのビルド

新しいタグで更新されたDockerイメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、ビルド済みの
> イメージを使用することを検討してください。その場合は、
> `~/workshop/agentic-ai/base-app/k8s.yaml` ファイルのイメージ名を
> `localhost:9999/agentic-ai-app:app-with-ai-defense` の代わりに `ghcr.io/splunk/agentic-ai-app:app-with-ai-defense` に変更します。

### AI Defense用Secretの作成

以下のコマンドを実行して、Cisco AI DefenseのインスペクションAPIキーとエンドポイントを保存するSecretを作成します。

```bash
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-inspection-api-key="$AI_DEFENSE_INSPECTION_API_KEY" --from-literal=ai-defense-inspection-api-endpoint="$AI_DEFENSE_INSPECTION_API_ENDPOINT"
```

### Kubernetesマニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開き、AI Defense対応のイメージを使用するようにイメージを更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

環境変数セクションの末尾に以下の環境変数を追加します。

```yaml
            - name: AI_DEFENSE_API_MODE_LLM_API_KEY
              valueFrom:
                secretKeyRef:
                  name: ai-defense-secret
                  key: ai-defense-inspection-api-key
            - name: AI_DEFENSE_API_MODE_LLM_ENDPOINT
              valueFrom:
                secretKeyRef:
                  name: ai-defense-secret
                  key: ai-defense-inspection-api-endpoint
```

{{% notice title="次に進む前に確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較します。

```bash
diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-ai-defense/k8s.yaml
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
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

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

ここでは、アプリケーションがまだ正常に動作していることを確認するだけで構いません。次のセクションでは、セキュリティリスクを追加し、それがどのように検出されるかを確認します。
