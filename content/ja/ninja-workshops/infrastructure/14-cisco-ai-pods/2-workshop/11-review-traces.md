---
title: メトリクス、トレース、ログの確認
linkTitle: 11. メトリクス、トレース、ログの確認
weight: 11
time: 10 minutes
---

## Splunk Observability Cloud でトレースデータを表示する

Splunk Observability Cloud で `APM` に移動し、`Service Map` を選択します。
環境名（例：`ai-pod-workshop-participant-1`）が選択されていることを確認します。
以下のようなサービスマップが表示されるはずです。

![Service Map](../../images/ServiceMap.png)

右側のメニューにある `Traces` をクリックします。次に、実行時間が比較的長いトレースの 1 つを選択します。以下の例のように表示されるはずです。

![Trace](../../images/Trace.png)

このトレースは、ユーザーの質問（例：「How much memory does the NVIDIA H200 have?」）に回答を返すためにアプリケーションが実行したすべてのインタラクションを示しています。

例えば、Weaviate ベクトルデータベース内で当該質問に関連するドキュメントを探すために、アプリケーションが類似検索を実行した箇所を確認できます。

また、ベクトルデータベースから取得したコンテキストを含めて、アプリケーションが LLM に送信するプロンプトをどのように作成したかも確認できます。

![Prompt Template](../../images/PromptTemplate.png)

> 注：トレースのウォーターフォールビューに `chat` および `invoke_workflow` の AI インタラクションが表示されない場合、または右側に `AI details` タブが表示されない場合は、有効化が必要な superpowers について講師に確認してください。

最後に、LLM からのレスポンス、所要時間、および使用された入出力トークン数を確認できます。

![LLM Response](../../images/LLMResponse.png)

## メトリクスが Splunk に送信されていることを確認する

Splunk Observability Cloud で `Dashboards` に移動し、`Built-in dashboard groups` に含まれている `Cisco AI PODs Dashboard` を検索します。
`NIM FOR LLMS` タブに移動し、ダッシュボードが自分の OpenShift クラスター名でフィルタリングされていることを確認します。以下の例のようにチャートにデータが表示されるはずです。

![NIM LLMS Dashboard](../../images/NIMLLM.png)
