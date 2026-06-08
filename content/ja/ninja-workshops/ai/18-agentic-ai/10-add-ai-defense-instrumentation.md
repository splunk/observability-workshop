---
title: AI Defense インストルメンテーションの追加
linkTitle: 10. AI Defense インストルメンテーションの追加
weight: 10
time: 15 minutes
---

> [!NOTE]
> このセクションでは、複数のファイルを変更する必要があります。
> 変更箇所が分からない場合や、アプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-ai-defense` フォルダにある
> このセクションの想定される解答を参照してください。

Splunk Observability Cloud は
[Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html)
と統合し、AI エージェントに対してランタイムで検出された[セキュリティおよびプライバシーリスク](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita)の統合ビューを提供します。これにより、パフォーマンスとリスクを一箇所で監視できます。

これは **Splunk AI Security Monitoring** と呼ばれ、以下のことが可能になります

* プロンプトインジェクションや PII 漏洩などの検出またはブロックされたセキュリティおよびプライバシーリスクに関与するエージェント、インタラクション、サービスの特定
* リスクの傾向をレイテンシー、エラー、その他のパフォーマンスメトリクスと並行して経時的に追跡
* トレースコンテキスト内でリスクのあるインタラクションを、特定のプロンプトとレスポンスのレベルまで調査

このセクションでは、Agentic AI アプリケーションに AI Defense インテグレーションを追加し、Splunk Observability Cloud で結果のデータを確認します。

## 仕組み

Splunk AI Security Monitoring は、Python ベースの AI エージェント向けにセキュリティおよびプライバシーリスクのトレーシングを自動化するインストルメンテーションライブラリ
[opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense)
を提供します。
このライブラリは、AI エージェントが LLM（OpenAI など）やオーケストレーションフレームワーク（LangChain など）に対して行う呼び出しにセキュリティテレメトリをキャプチャしてアタッチします。これにより、すべてのプロンプトとレスポンスがセキュリティガードレールに対して監査され、統一された OpenTelemetry トレース内に記録されます。これは、LLM またはワークフロースパンに `gen_ai.security.event_id attribute` を追加することで実現されます。

## SDK モード vs. Gateway モード

`opentelemetry-instrumentation-aidefense` ライブラリは、SDK モードまたは Gateway モードのいずれかで動作できます

* SDK モードでは、開発者が `inspect_prompt()` を使用して明示的なセキュリティチェックを追加します。このオプションは、セキュリティチェックの実装方法と問題への対処方法を完全に制御したい開発者に最適です。
* Gateway モードでは、LLM 呼び出しが Cisco AI Defense Gateway を経由してプロキシされるため、アプリケーションコードの変更は不要です。このモードは、OpenAI、Anthropic などの一般的な商用 LLM でサポートされています。

このワークショップでは、Azure OpenAI を使用した SDK モードを利用します。

## Cisco AI Defense インテグレーションのセットアップ

最初のステップは、[Cisco AI Defense とのインテグレーションをセットアップ](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense)することです。

**Data Management -> Deployed integrations** に移動して `AI Defense` を検索すると、このインテグレーションがすでに設定されていることが確認できます

> [!NOTE]
> このインテグレーションを表示するには、`aiDefenseIntegration` フィーチャーフラグを有効にする必要があります

![AI Defense Config](../images/AIDefenseConfig.png)

## インストルメンテーションパッケージの追加

次に、いくつかのインストルメンテーションパッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を編集用に開き、以下のパッケージを追加します

```text
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
```

{{% notice title="進む前に作業内容を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較してください

```bash
diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-ai-defense/requirements.txt
```

{{% / notice %}}

## AI Defense SDK のインポート

アプリケーションを修正して、エージェントに Cisco AI Defense の保護を追加しましょう。

`~/workshop/agentic-ai/base-app/main.py` ファイルを編集用に開きます。

`Begin: Initialize AI Defense` と `End: Initialize AI Defense` の間に、AI Defense の保護をインポートして有効化します

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
> 保護のインポートと有効化は、`langchain_openai` などの LLM クライアントパッケージをインポートする前に行う必要があります

{{% notice title="進む前に作業内容を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較してください

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-ai-defense/main.py
```

{{% / notice %}}

### 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを使用することを検討してください。
> その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルのイメージ名を
> `localhost:9999/agentic-ai-app:app-with-ai-defense` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-ai-defense` に更新してください。

### AI Defense 用の Secret の作成

以下のコマンドを実行して、Cisco AI Defense のインスペクション API キーとエンドポイントを格納する Secret を作成します

```bash
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-inspection-api-key="$AI_DEFENSE_INSPECTION_API_KEY" --from-literal=ai-defense-inspection-api-endpoint="$AI_DEFENSE_INSPECTION_API_ENDPOINT"
```

### Kubernetes マニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開き、AI Defense を含むイメージを使用するようにイメージを更新します

```yaml
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

環境変数セクションの末尾に以下の環境変数を追加します

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

{{% notice title="進む前に作業内容を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される解答と比較してください

```bash
diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-ai-defense/k8s.yaml
```

{{% / notice %}}

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイします

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションテスト

新しいアプリケーション Pod が正常に起動し、古い Pod が存在しないことを確認します

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

今はアプリケーションが正常に動作していることを確認するだけで構いません。次のセクションでは、セキュリティリスクを追加し、それがどのように検出されるかを示します。
