---
title: エージェントトレースデータの確認
linkTitle: 7. エージェントトレースデータの確認
weight: 7
time: 10 minutes
---

## LLM プロバイダー設定の確認

Splunk Observability Cloud には、Large Language Model（LLM）を接続するためのインテグレーションが含まれています。Splunk はこの接続を使用して、アプリケーションが生成した LLM レスポンスの**セマンティック品質**を評価します。

このインテグレーションは、ワークショップの組織にすでに設定されています。

設定を確認するには、**Data Management → Deployed Integrations** に移動し、**LLM Providers** を検索して選択します。以下のプロバイダーが表示されるはずです

![LLM Providers](../images/LLMProviders.png)

`Azure OpenAI O11y Specialists` プロバイダーをクリックして、詳細を確認します

![LLM Provider Details](../images/LLMProviderDetails.png)

この組織では、サンプリングレートは **20%** に設定されています。これは、平均してアプリケーションが生成した **LLM レスポンスの 20%** のセマンティック品質を Splunk が評価することを意味します。

また、**1分あたり50回の評価のレートリミット**も設定されています。サンプリングレートとレートリミットは、お客様のニーズに応じて調整できます。サンプリングレートを高くするとより多くの評価データが得られますが、トークン使用量と関連コストも増加します。

## Splunk Observability Cloud でトレースデータを表示する

Splunk Observability Cloud で `APM` に移動し、`Service Map` を選択します。
環境名が選択されていることを確認してください（例`agentic-ai-$INSTANCE`）。
以下のようなサービスマップが表示されるはずです

![Service Map](../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間の長いトレースの1つを選択します。以下の例のように表示されるはずです

![Trace](../images/Trace.png)

**Agent flow** セクションにエージェント名（coordinator、flight-specialist など）が表示されていないことに注目してください。

下にスクロールして、トレース内の AI インタラクションの1つをクリックしてみましょう。ここでは、プロンプトとレスポンスがキャプチャされていることが確認できます。また、このトレースのセマンティック品質評価の結果も確認できます

![Trace Details](../images/TraceDetails.png)

次に、`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認してください（例`agentic-ai-$INSTANCE`）。ページが空であることに気づくでしょう！

![Agents](../images/Agents.png)

これらの計装の問題については、次のセクションで対処します。
