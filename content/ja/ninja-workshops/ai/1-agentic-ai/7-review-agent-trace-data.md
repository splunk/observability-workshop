---
title: エージェントトレースデータの確認
linkTitle: 7. エージェントトレースデータの確認
weight: 7
time: 10 minutes
---

## LLM プロバイダー設定の確認

Splunk Observability Cloud には、Large Language Model (LLM) を接続するためのインテグレーションが含まれています。Splunk はこの接続を使用して、アプリケーションが生成した LLM レスポンスの**セマンティック品質**を評価します。

このインテグレーションは、ワークショップの組織ですでに設定済みです。

設定を確認するには、**Data Management → Deployed Integrations** に移動し、**LLM Providers** を検索して選択します。以下のプロバイダーが表示されるはずです

![LLM Providers](../images/LLMProviders.png)

`Azure OpenAI O11y Specialists` プロバイダーをクリックして詳細を表示します

![LLM Provider Details](../images/LLMProviderDetails.png)

この組織では、サンプリングレートが **20%** に設定されています。これは、平均してアプリケーションが生成した **LLM レスポンスの 20%** に対して Splunk がセマンティック品質を評価することを意味します。

**1分あたり50件の評価というレート制限**も設定されています。サンプリングレートとレート制限はどちらも、お客様のニーズに応じて調整できます。サンプリングレートを高くすると、より多くの評価データが得られますが、トークン使用量と関連コストも増加します。

## AI Agent Monitoring 設定の確認

Splunk Observability Cloud には、AI Agent Monitoring に関連する詳細の保存に使用するデータソースを設定するページも含まれています。選択肢は以下の通りです

* Data source – Splunk Observability Cloud
* Data source – Splunk logs

これらの設定は **Settings -> AI Agent Monitoring** に移動すると確認できます

![AI Agent Monitoring Configuration](../images/AIAgentMonitoringConfiguration.png)

Splunk は、AI Agent Monitoring 関連の詳細の保存に Splunk Observability Cloud を使用することを推奨しています。このワークショップではこの設定を使用しています。

## AI Monitoring 権限の確認

LLM の会話データは機密性が高い可能性があるため、この情報にアクセスして表示できるユーザーを制御するための `ai_monitoring` という新しいロールが Splunk Observability Cloud に追加されています

![AI Monitoring Role](../images/AIMonitoringRole.png)

## Splunk Observability Cloud でのトレースデータの表示

Splunk Observability Cloud で `APM` に移動し、`Service Map` を選択します。環境名が選択されていることを確認します（例: `agentic-ai-$INSTANCE`）。以下のようなサービスマップが表示されるはずです

![Service Map](../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間が長いトレースの1つを選択します。以下の例のように表示されるはずです

![Trace](../images/Trace.png)

**Agent flow** セクションにエージェント名（coordinator、flight-specialist など）が表示されていないことに注目してください。

下にスクロールして、トレース内の AI インタラクションの1つをクリックしましょう。ここでは、プロンプトとレスポンスがキャプチャされていることが確認できます。また、このトレースのセマンティック品質評価の結果も確認できます

![Trace Details](../images/TraceDetails.png)

次に、`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認します（例: `agentic-ai-$INSTANCE`）。ページが空であることに気付くでしょう。

![Agents](../images/Agents.png)

これらのインストルメンテーションの問題は、次のセクションで対処します。
