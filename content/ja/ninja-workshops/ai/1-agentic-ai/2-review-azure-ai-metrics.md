---
title: Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
linkTitle: 2. Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
weight: 2
time: 10 minutes
---

このワークショップでは、Azure で動作する OpenAI モデルを使用します。

Azure OpenAI アプリケーションから Splunk Observability Cloud にメトリクスを送信するように設定することで、Azure OpenAI アプリケーションのパフォーマンスを監視できます。

[ドキュメント](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cloud-services/azure-openai)に記載されている手順に従って、ワークショップ用の Splunk Observability Cloud インスタンスと Azure アカウントの統合は既に完了しています。

Azure OpenAI メトリクスが含まれるようにするため、`Cognitive Services` からメトリクスを取得するように接続を設定しました

![Azure connection](../images/AzureConnection.png)

## Azure OpenAI メトリクス

Azure OpenAI では、以下のメトリクスが取得されます

* ProcessedPromptTokens
* GeneratedTokens
* AzureOpenAIRequests
* AzureOpenAITimeToResponse
* AzureOpenAIAvailabilityRate
* AzureOpenAITokenPerSecond
* AzureOpenAIContextTokensCacheMatchRate

**Metrics** -> **Metric finder** に移動し、`ProcessedPromptTokens` メトリクスを検索して **View in chart** をクリックします

> 注: [このリンク](https://app.us1.signalfx.com/#/chart/v2/new?template=default&filters=sf_metric:ProcessedPromptTokens)を使用して **Metric finder** でこのメトリクスを表示することもできます。

![Processed Prompt Tokens Metric](../images/ProcessedPromptTokensMetric.png)

## Azure OpenAI ナビゲーター

Splunk Observability Cloud は、OpenTelemetry の生成 AI クライアントおよびモデルサーバーのメトリクスを収集し、Azure で動作する Open AI 大規模言語モデル（LLM）サービスのトークン使用量を追跡します。

これらのメトリクスは Azure OpenAI ナビゲーターを使用して確認できます。**Infrastructure** -> **Overview** -> **AI Frameworks** に移動し、**Azure OpenAI** をクリックします

![Azure OpenAI Navigator](../images/AzureOpenAINavigator.png)

## Azure OpenAI ダッシュボード

Splunk Observability Cloud は、Azure OpenAI 用の組み込みダッシュボードを提供しており、以下の項目を即座に可視化できます

* アクティブな Azure OpenAI モデル
* トークン使用量
* 呼び出しレイテンシー
* モデル別の呼び出し数
* 最初のバイトまでの時間
* 合計レスポンス時間
* モデルの可用性
* リクエストあたりのトークン数
* モデルごとの処理済みトークン数
* モデルごとの生成済みトークン数

**Dashboards** に移動し、**Azure OpenAI** を検索してダッシュボードを表示します

![Azure OpenAI Dashboard](../images/AzureOpenAIDashboard.png)
