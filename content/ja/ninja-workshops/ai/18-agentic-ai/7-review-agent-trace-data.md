---
title: エージェントトレースデータの確認
linkTitle: 7. エージェントトレースデータの確認
weight: 7
time: 10 minutes
---

## LLM プロバイダー設定の確認

Splunk Observability Cloud には、Large Language Model（LLM）を接続するためのインテグレーションが含まれています。Splunk はこの接続を使用して、アプリケーションが生成した LLM レスポンスの**セマンティック品質**を評価します。

このインテグレーションは、ワークショップの組織で既に設定されています。

設定を確認するには、**Data Management → Deployed Integrations** に移動し、**Categories** フィルターを `LLMs` に設定します。

**LLM Providers** を検索して選択します。以下のプロバイダーが表示されるはずです

![LLM Providers](../images/LLMProviders.png)

`Azure OpenAI O11y Specialists` プロバイダーをクリックして詳細を確認します

![LLM Provider Details](../images/LLMProviderDetails.png)

この組織では、サンプリングレートが **20%** に設定されています。これは、平均して Splunk がアプリケーションによって生成された **LLM レスポンスの 20%** のセマンティック品質を評価することを意味します。

**1分あたり50評価のレート制限**も設定されています。サンプリングレートとレート制限の両方は、お客様のニーズに応じて調整できます。サンプリングレートを高くするとより多くの評価データが得られますが、トークン使用量と関連コストも増加します。

## AI Agent Monitoring 設定の確認

Splunk Observability Cloud には、AI Agent Monitoring に関連する詳細の保存に使用するデータソースを設定するためのページも含まれています。選択肢は以下の通りです

* Data source – Splunk Observability Cloud
* Data source – Splunk logs

これらの設定は、**Settings -> AI Agent Monitoring** に移動して確認できます

![AI Agent Monitoring Configuration](../images/AIAgentMonitoringConfiguration.png)

Splunk は、AI Agent Monitoring 関連の詳細の保存に Splunk Observability Cloud を利用することを推奨しています。このワークショップではこの設定を使用しています。

## AI Monitoring 権限の確認

LLM 会話データの潜在的に機密性の高い性質のため、この情報にアクセスして表示できるユーザーを制御する `ai_monitoring` という新しいロールが Splunk Observability Cloud に追加されています

![AI Monitoring Role](../images/AIMonitoringRole.png)

## Splunk Observability Cloud でのトレースデータの表示

Splunk Observability Cloud で `APM` に移動し、`Service Map` を選択します。環境名が選択されていることを確認してください（例`agentic-ai-$INSTANCE`）。

> [!TIP]
> インスタンス名を忘れた場合は `echo $INSTANCE` コマンドを使用してください

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
