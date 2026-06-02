---
title: Review Agent Trace Data
linkTitle: 7. Review Agent Trace Data
weight: 7
time: 10 minutes
---

## LLMプロバイダー設定の確認

Splunk Observability Cloudには、大規模言語モデル (LLM) と接続するためのインテグレーションが含まれています。Splunkはこの接続を利用して、アプリケーションが生成したLLMレスポンスの **セマンティック品質** を評価します。

このインテグレーションは、ワークショップの組織にすでに設定済みです。

設定を確認するには、**Data Management → Deployed Integrations** に移動し、**Categories** フィルターを `LLMs` に設定します。

**LLM Providers** を検索して選択します。次のプロバイダーが表示されます。

![LLM Providers](../images/LLMProviders.png)

`Azure OpenAI O11y Specialists` プロバイダーをクリックして詳細を表示します。

![LLM Provider Details](../images/LLMProviderDetails.png)

この組織では、サンプリングレートが **20%** に設定されています。これは、Splunkがアプリケーションで生成されたLLMレスポンスの **平均20%** についてセマンティック品質を評価することを意味します。

また、**1分あたり50回の評価レート制限** も設定されています。サンプリングレートとレート制限は、顧客のニーズに応じて調整できます。サンプリングレートが高いほど評価データは多く得られますが、トークン使用量とそれに伴うコストも増加します。

## AI Agent Monitoring設定の確認

Splunk Observability Cloudには、AI Agent Monitoringに関連する詳細情報の保存に使用するデータソースを設定するページも用意されています。選択肢は次のとおりです。

* Data source – Splunk Observability Cloud
* Data source – Splunk logs

これらの設定は、**Settings -> AI Agent Monitoring** に移動して確認できます。

![AI Agent Monitoring Configuration](../images/AIAgentMonitoringConfiguration.png)

SplunkはAI Agent Monitoring関連の詳細情報の保存にSplunk Observability Cloudの利用を推奨しています。本ワークショップでもこの設定を採用しています。

## AI Monitoring権限の確認

LLMの会話データは機密性を持つ可能性があるため、この情報へのアクセスと閲覧を制御するための新しいロール `ai_monitoring` がSplunk Observability Cloudに追加されました。

![AI Monitoring Role](../images/AIMonitoringRole.png)

## Splunk Observability Cloudでトレースデータを表示する

Splunk Observability Cloudで `APM` に移動し、`Service Map` を選択します。環境名 (例: `agentic-ai-$INSTANCE`) が選択されていることを確認してください。

> ヒント: インスタンス名を忘れた場合は、`echo $INSTANCE` コマンドを使用してください

次のようなサービスマップが表示されます。

![Service Map](../images/ServiceMap.png)

右側のメニューから `Traces` をクリックします。次に、実行時間が長めのトレースのいずれかを選択します。次の例のような表示になります。

![Trace](../images/Trace.png)

**Agent flow** セクションにエージェント名 (coordinator、flight-specialist など) が表示されていないことに注目してください。

下にスクロールし、トレース内のAIインタラクションのいずれかをクリックします。プロンプトとレスポンスがキャプチャされていることが確認できます。また、このトレースに対するセマンティック品質評価の結果も確認できます。

![Trace Details](../images/TraceDetails.png)

次に、`APM` に移動し、`AI agents` を選択します。環境名 (例: `agentic-ai-$INSTANCE`) が選択されていることを確認してください。ページが空になっていることに気付くでしょう。

![Agents](../images/Agents.png)

これらの計装の問題については、次のセクションで対処します。
