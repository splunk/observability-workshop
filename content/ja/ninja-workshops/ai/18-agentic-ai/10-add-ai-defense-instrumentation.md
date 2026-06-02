---
title: AI Defenseインストルメンテーションの追加
linkTitle: 10. AI Defenseインストルメンテーションの追加
weight: 10
time: 15 minutes
---

> 注意: ワークショップのこのセクションでは、複数のファイルへの変更が必要です。
> どこを変更すればよいかわからない場合や、アプリケーションが動作しなくなった場合は、
> このセクションの想定される完成形（`~/workshop/agentic-ai/app-with-ai-defense` フォルダ内）
> を参照してください。

Splunk Observability Cloudは
[Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html)
と連携することで、AIエージェントの実行時に検知された[セキュリティおよびプライバシーリスク](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita)
を統合的に可視化し、パフォーマンスとリスクを一元的に監視できます。

これは **Splunk AI Security Monitoring** と呼ばれ、以下を支援します。

* プロンプトインジェクションやPII漏えいなど、検知またはブロックされたセキュリティ・プライバシーリスクに関連するエージェント、対話、サービスを特定する
* レイテンシ、エラー、その他のパフォーマンスメトリクスとともに、リスクの傾向を経時的に追跡する
* 特定のプロンプトやレスポンスに至るまで、トレースのコンテキスト内でリスクのある対話を調査する

このセクションでは、Agentic AIアプリケーションにAI Defense連携を追加し、
Splunk Observability Cloudで結果のデータを確認します。

## 仕組み

Splunk AI Security Monitoringは、Pythonベースのエージェントに対するセキュリティおよびプライバシーリスクのトレースを自動化するためのインストルメンテーションライブラリ
[opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense)
を提供しています。
このライブラリは、AIエージェントがLLM（OpenAIなど）やオーケストレーションフレームワーク（LangChainなど）に対して行う呼び出しに対して、
セキュリティテレメトリをキャプチャしてアタッチします。
これにより、すべてのプロンプトとレスポンスをセキュリティガードレールに照らして監査でき、
統合されたOpenTelemetryトレース内に記録できることを保証します。
具体的には、LLMまたはワークフローのスパンに
`gen_ai.security.event_id attribute` を追加することで実現されます。

## SDKモード vs ゲートウェイモード

`opentelemetry-instrumentation-aidefense` ライブラリは、SDKモードまたはゲートウェイモードのいずれかで動作します。

* SDKモードでは、開発者が `inspect_prompt()` を使用して明示的なセキュリティチェックを追加します。このオプションは、セキュリティチェックの実装方法や問題への対処方法を完全に制御したい開発者に最適です。
* ゲートウェイモードでは、LLM呼び出しがCisco AI Defense Gateway経由でプロキシされるため、アプリケーションコードの変更は不要です。このモードはOpenAI、Anthropicなど主要な商用LLMでサポートされています。

このワークショップでは、Azure OpenAIとともにSDKモードを利用します。

## Cisco AI Defense連携のセットアップ

最初のステップは、[Cisco AI Defenseとの連携をセットアップする](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense)ことです。

**Data Management -> Deployed integrations** に移動し、`AI Defense` を検索すると、
この連携がすでに構成されていることがわかります。

> 注意: この連携を表示するには、`aiDefenseIntegration` フィーチャーフラグを有効にする必要があります

![AI Defense Config](../images/AIDefenseConfig.png)

## インストルメンテーションパッケージの追加

次に、いくつかのインストルメンテーションパッケージをインストールする必要があります。
`~/workshop/agentic-ai/base-app/requirements.txt` を編集用に開き、
以下のパッケージを追加します。

````
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
````

{{% notice title="先に進む前に作業を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される完成形と比較してください。

```bash
diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-ai-defense/requirements.txt
```

{{% / notice %}}

## AI Defense SDKのインポート

エージェントにCisco AI Defense保護を追加するために、アプリケーションを変更しましょう。

`~/workshop/agentic-ai/base-app/main.py` ファイルを編集用に開きます。

`Begin: Initialize AI Defense` と `End: Initialize AI Defense` の行の間に、
AI Defense保護をインポートして有効化します。

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

> 重要: 保護のインポートと有効化は、`langchain_openai` などのLLMクライアントパッケージをインポートする**前**に実行する必要があります

{{% notice title="先に進む前に作業を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される完成形と比較してください。

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-ai-defense/main.py
```

{{% / notice %}}

### 更新したDockerイメージのビルド

新しいタグで更新後のDockerイメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みイメージの利用を検討してください。
> その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内のイメージ名を
> `localhost:9999/agentic-ai-app:app-with-ai-defense` から
> `ghcr.io/splunk/agentic-ai-app:app-with-ai-defense` に更新してください。

### AI Defense用のシークレット作成

ワークショップインストラクターから提供されたドキュメントには、Cisco AI Defenseの検査APIキーとエンドポイントを保存するためのシークレットを作成する `kubectl create secret` コマンドが含まれています。

ドキュメントから `kubectl create secret` コマンドをコピーし、
sshターミナルに貼り付けて実行してください。

### Kubernetesマニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開き、
AI Defenseが含まれるイメージを使用するようにイメージを更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

環境変数セクションの末尾に、以下の環境変数を追加します。

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

{{% notice title="先に進む前に作業を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を想定される完成形と比較してください。

```bash
diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-ai-defense/k8s.yaml
```

{{% / notice %}}

### 更新したアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新後のアプリケーションをデプロイできます。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでのアプリケーションのテスト

新しいアプリケーションPodが正常に起動し、古いPodが残っていないことを確認します。

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

ここでは、アプリケーションが引き続き動作していることを確認するだけで構いません。
次のセクションでは、セキュリティリスクを追加し、それがどのように検知されるかを示します。
