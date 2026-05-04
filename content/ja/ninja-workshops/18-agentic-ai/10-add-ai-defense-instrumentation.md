---
title: AI Defense 計装の追加
linkTitle: 10. AI Defense 計装の追加
weight: 10
time: 15 minutes
---

> 注意: このセクションでは複数のファイルを変更する必要があります。
> 変更箇所がわからない場合やアプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-ai-defense` フォルダにある
> モデルソリューションを参照してください。

Splunk Observability Cloud は
[Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html)
と統合し、AI エージェントの実行時に検出された[セキュリティおよびプライバシーリスク](https://securitydocs.cisco.com/docs/ai-def/user/105473.dita)の統合ビューを提供します。これにより、パフォーマンスとリスクを一か所で監視できます。

これは **Splunk AI Security Monitoring** と呼ばれ、以下のことが可能になります:

* プロンプトインジェクションや PII 漏洩など、検出またはブロックされたセキュリティおよびプライバシーリスクに関与するエージェント、インタラクション、サービスを特定する
* リスクの傾向をレイテンシー、エラー、その他のパフォーマンスメトリクスとともに経時的に追跡する
* トレースコンテキストでリスクのあるインタラクションを、特定のプロンプトとレスポンスのレベルまで調査する

このセクションでは、Agentic AI アプリケーションに AI Defense インテグレーションを追加し、Splunk Observability Cloud で得られたデータを確認します。

## 仕組み

Splunk AI Security Monitoring は、Python ベースの AI エージェントのセキュリティおよびプライバシーリスクのトレーシングを自動化する計装ライブラリ
[opentelemetry-instrumentation-aidefense](https://github.com/signalfx/splunk-otel-python-contrib/tree/main/instrumentation-genai/opentelemetry-instrumentation-aidefense)
を提供しています。このライブラリは、AI エージェントが LLM（OpenAI など）やオーケストレーションフレームワーク（LangChain など）に対して行う呼び出しにセキュリティテレメトリーをキャプチャして付与し、すべてのプロンプトとレスポンスがセキュリティガードレールに対して監査され、統合された OpenTelemetry トレース内に記録されるようにします。これは、LLM またはワークフロースパンに `gen_ai.security.event_id attribute` を追加することで実現されます。

## SDK モードと Gateway モード

`opentelemetry-instrumentation-aidefense` ライブラリは、SDK モードまたは Gateway モードのいずれかで動作できます:

* SDK モードでは、開発者が `inspect_prompt()` を使用して明示的なセキュリティチェックを追加します。このオプションは、セキュリティチェックの実装方法と問題への対処方法を完全に制御したい開発者に最適です。
* Gateway モードでは、LLM 呼び出しが Cisco AI Defense Gateway を経由してプロキシされるため、アプリケーションコードの変更は不要です。このモードは、OpenAI、Anthropic などの一般的な商用 LLM でサポートされています。

このワークショップでは、Azure OpenAI を使用した Gateway モードを利用します。

## Cisco AI Defense インテグレーションのセットアップ

最初のステップは、[Cisco AI Defense とのインテグレーションのセットアップ](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-security-monitoring/set-up-an-integration-with-cisco-ai-defense)です。

**Data Management -> Deployed integrations** に移動し、`AI Defense` を検索すると、このインテグレーションが既に設定されていることが確認できます:

> 注意: このインテグレーションを表示するには、`aiDefenseIntegration` フィーチャーフラグが有効になっている必要があります

![AI Defense Config](../images/AIDefenseConfig.png)

## 計装パッケージの追加

次に、いくつかの計装パッケージをインストールする必要があります。`~/workshop/agentic-ai/base-app/requirements.txt` を開いて編集し、以下のパッケージを追加します:

````
# AI Defense instrumentation (Gateway Mode support in v0.2.0+)
splunk-otel-instrumentation-aidefense>=0.2.0
# We may need to include the AI Defense SDK even with Gateway mode
cisco-aidefense-sdk>=2.0.0
# HTTP client (httpx is required for Gateway Mode to work)
httpx>=0.24.0
````

> ヒント: 以下のコマンドを実行して、変更内容をモデルソリューションと比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/requirements.txt ~/workshop/agentic-ai/app-with-ai-defense/requirements.txt`

### 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-ai-defense .
docker push localhost:9999/agentic-ai-app:app-with-ai-defense
```

### AI Defense Gateway 用の Secret の作成

AI Defense Gateway の URL を保存するための Secret を作成します:

> 注意: Secret の作成時に使用する実際の AI Defense URL はワークショップの講師から提供されます

```bash
kubectl create secret generic ai-defense-secret -n travel-agent --from-literal=ai-defense-gateway-url='https://us.gateway.aidefense.security.cisco.com/{tenant}/connections/{conn}'
```

### Kubernetes マニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、`AZURE_OPENAI_ENDPOINT` 環境変数の定義を以下のように置き換えます。これにより、Azure OpenAI 宛てのリクエストが代わりに AI Defense Gateway を経由して送信されるようになります:

```yaml
            - name: AZURE_OPENAI_ENDPOINT
              valueFrom:
                secretKeyRef:
                  name: ai-defense-secret
                  key: ai-defense-gateway-url
```

同じファイルで、計装を含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-ai-defense
```

> ヒント: 以下のコマンドを実行して、変更内容をモデルソリューションと比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/k8s.yaml ~/workshop/agentic-ai/app-with-ai-defense/k8s.yaml`

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

新しいアプリケーション Pod が正常に起動し、古い Pod がなくなっていることを確認します:

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

現時点では、アプリケーションが引き続き動作していることを確認してください。次のセクションでは、セキュリティリスクを追加し、それがどのように検出されるかを確認します。
