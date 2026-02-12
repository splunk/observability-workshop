---
title: メトリクス、トレース、およびログの確認
linkTitle: 11. メトリクス、トレース、およびログの確認
weight: 11
time: 10 minutes
---

## Splunk Observability Cloud でトレースデータを表示する

Splunk Observability Cloud で `APM` に移動し、`Service Map` を選択します。
お使いの環境名が選択されていることを確認してください（例: `ai-pod-workshop-participant-1`）。
以下のようなサービスマップが表示されるはずです:

![Service Map](../../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間の長いトレースを1つ選択します。以下の例のように表示されるはずです:

![Trace](../../images/Trace.png)

このトレースは、ユーザーの質問（例: 「How much memory does the NVIDIA H200 have?」）に対する回答を返すために、アプリケーションが実行したすべてのインタラクションを示しています。

例えば、アプリケーションが Weaviate ベクトルデータベースで質問に関連するドキュメントを検索するために類似度検索を実行した箇所を確認できます。

また、ベクトルデータベースから取得したコンテキストを含め、アプリケーションが LLM に送信するプロンプトをどのように作成したかも確認できます:

![Prompt Template](../../images/PromptTemplate.png)

最後に、LLM からのレスポンス、所要時間、および使用された入力トークンと出力トークンの数を確認できます:

![LLM Response](../../images/LLMResponse.png)

## メトリクスが Splunk に送信されていることを確認する

Splunk Observability Cloud で `Dashboards` に移動し、`Built-in dashboard groups` に含まれる `Cisco AI PODs Dashboard` を検索します。
`NIM FOR LLMS` タブに移動し、お使いの OpenShift クラスター名でダッシュボードがフィルタリングされていることを確認します。以下の例のようにチャートにデータが表示されているはずです:

![NIM LLMS Dashboard](../../images/NIMLLM.png)
