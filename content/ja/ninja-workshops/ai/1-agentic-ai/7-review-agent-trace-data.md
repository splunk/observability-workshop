---
title: エージェントのトレースデータを確認する
linkTitle: 7. Review Agent Trace Data
weight: 7
time: 10 minutes
---

## LLMプロバイダー設定の確認

Splunk Observability Cloudには、Large Language Model（LLM）を接続するためのインテグレーションが含まれています。Splunkはこの接続を使用して、アプリケーションが生成したLLMレスポンスの **セマンティック品質** を評価します。

このインテグレーションは、ワークショップの組織で既に設定済みです。

設定を確認するには、 **Data Management → Deployed Integrations** に移動し、 **Categories** フィルターを `LLMs` に設定します。

**LLM Providers** を検索して選択します。以下のプロバイダーが表示されます。

![LLM Providers](../images/LLMProviders.png)

`Azure OpenAI O11y Specialists` プロバイダーをクリックして詳細を表示します。

![LLM Provider Details](../images/LLMProviderDetails.png)

この組織では、サンプリングレートが **20%** に設定されています。これは、平均してアプリケーションが生成した **LLMレスポンスの20%** に対してSplunkがセマンティック品質を評価することを意味します。

**1分あたり50評価のレート制限** も設定されています。サンプリングレートとレート制限はどちらも顧客のニーズに応じて調整できます。サンプリングレートを高くすると、より多くの評価データが得られますが、トークン使用量と関連コストも増加します。

## AIエージェントモニタリング設定の確認

Splunk Observability Cloudには、AI Agent Monitoringに関連する詳細を保存するために使用するデータソースを設定するページも含まれています。選択肢は以下のとおりです。

* データソース – Splunk Observability Cloud
* データソース – Splunkログ

これらの設定は **Settings -> AI Agent Monitoring** に移動すると確認できます。

![AI Agent Monitoring Configuration](../images/AIAgentMonitoringConfiguration.png)

Splunkは、AI Agent Monitoring関連の詳細を保存するためにSplunk Observability Cloudを利用することを推奨しています。このワークショップではこの設定を使用しています。

## AIモニタリング権限の確認

LLM会話データは機密性が高い可能性があるため、この情報にアクセスして表示できるユーザーを制御する `ai_monitoring` という新しいロールがSplunk Observability Cloudに追加されています。

![AI Monitoring Role](../images/AIMonitoringRole.png)

## Splunk Observability Cloudでトレースデータを表示する

Splunk Observability Cloudで `APM` に移動し、`Service Map` を選択します。環境名が選択されていることを確認します（例: `agentic-ai-$INSTANCE`）。

> [!TIP]
> インスタンス名を忘れた場合は `echo $INSTANCE` コマンドを使用してください

以下のようなサービスマップが表示されます。

![Service Map](../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間が長いTraceの1つを選択します。以下の例のように表示されます。

![Trace](../images/Trace.png)

**Agent flow** セクションにエージェント名（coordinator、flight-specialistなど）が表示されていないことに注目してください。

下にスクロールして、Trace内のAIインタラクションの1つをクリックします。ここでは、プロンプトとレスポンスがキャプチャされていることを確認できます。また、このTraceのセマンティック品質評価の結果も確認できます。

![Trace Details](../images/TraceDetails.png)

次に、`APM` に移動して `AI agents` を選択します。環境名が選択されていることを確認します（例: `agentic-ai-$INSTANCE`）。ページが空であることに気付くでしょう。

![Agents](../images/Agents.png)

これらの計装の問題については、次のセクションで対処します。
