---
title: Metrics、Traces、Logsの確認
linkTitle: 11. Metrics、Traces、Logsの確認
weight: 11
time: 10 minutes
---

## Splunk Observability CloudでTraceデータを表示する

Splunk Observability Cloudで `APM` に移動し、`Service Map` を選択します。
環境名が選択されていることを確認します（例: `ai-pod-workshop-participant-1`）。
以下のようなサービスマップが表示されます。

![Service Map](../../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間が長いTraceの1つを選択します。以下の例のように表示されます。

![Trace](../../images/Trace.png)

Traceには、ユーザーの質問（例:「NVIDIA H200のメモリはどのくらいですか？」）に対する回答を返すためにアプリケーションが実行したすべてのインタラクションが表示されます。

例えば、Weaviateベクトルデータベースで質問に関連するドキュメントを検索するために、アプリケーションが類似性検索を実行した箇所を確認できます。

また、ベクトルデータベースから取得したコンテキストを含め、アプリケーションがLLMに送信するプロンプトをどのように作成したかも確認できます。

![Prompt Template](../../images/PromptTemplate.png)

> 注意: Traceのウォーターフォールビューに `chat` と `invoke_workflow` のAIインタラクションが表示されない場合、または右側に `AI details` タブが表示されない場合は、有効にする必要があるスーパーパワーについてインストラクターに確認してください。

最後に、LLMからのレスポンス、所要時間、使用された入力トークン数と出力トークン数を確認できます。

![LLM Response](../../images/LLMResponse.png)

## MetricsがSplunkに送信されていることを確認する

Splunk Observability Cloudで `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索します。
`NIM FOR LLMS` タブに移動し、ダッシュボードがOpenShiftクラスター名でフィルタリングされていることを確認します。以下の例のようにチャートにデータが表示されます。

![NIM LLMS Dashboard](../../images/NIMLLM.png)
