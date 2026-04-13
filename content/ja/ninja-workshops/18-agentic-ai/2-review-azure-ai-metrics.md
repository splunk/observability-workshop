---
title: Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
linkTitle: 2. Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
weight: 2
time: 10 minutes
---

このワークショップでは、Azure で実行されている OpenAI モデルを使用します。

Azure OpenAI アプリケーションのパフォーマンスを監視するには、Azure OpenAI アプリケーションを設定して Splunk Observability Cloud にメトリクスを送信します。

ワークショップ用の Splunk Observability Cloud インスタンスと Azure アカウントの連携は、[ドキュメント](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cloud-services/azure-openai)に記載されている手順に従って、すでに完了しています。

Azure OpenAI メトリクスが含まれるようにするため、`Cognitive Services` からメトリクスを取得するように接続を設定しました

![Azure connection](../images/AzureConnection.png)

## Azure OpenAI メトリクス

Azure OpenAI では、以下のメトリクスが収集されます

* ProcessedPromptTokens
* GeneratedTokens
* AzureOpenAIRequests
* AzureOpenAITimeToResponse
* AzureOpenAIAvailabilityRate
* AzureOpenAITokenPerSecond
* AzureOpenAIContextTokensCacheMatchRate

**Metrics** -> **Metric finder** に移動し、`ProcessedPromptTokens` メトリクスを検索して **View in chart** をクリックします

![Processed Prompt Tokens Metric](../images/ProcessedPromptTokensMetric.png)

## Azure OpenAI ナビゲーター

Splunk Observability Cloud は、Azure で実行されている OpenAI 大規模言語モデル（LLM）サービスのトークン使用量を追跡するために、OpenTelemetry の生成 AI クライアントおよびモデルサーバーのメトリクスを収集します。

これらのメトリクスは Azure OpenAI ナビゲーターを使用して確認できます。**Infrastructure** -> **Overview** -> **AI Frameworks** に移動し、**Azure OpenAI** をクリックします

![Azure OpenAI Navigator](../images/AzureOpenAINavigator.png)

## Azure OpenAI ダッシュボード

Splunk Observability Cloud は、Azure OpenAI 用の組み込みダッシュボードを提供しており、以下の項目をすぐに可視化できます

* アクティブな Azure OpenAI モデル
* トークン使用量
* 呼び出しレイテンシ
* モデル別の呼び出し回数
* 最初のバイトまでの時間
* 合計応答時間
* モデルの可用性
* リクエストあたりのトークン数
* モデルが処理したトークン数
* モデルが生成したトークン数

**Dashboards** に移動し、**Azure OpenAI** を検索してダッシュボードを表示します

![Azure OpenAI Dashboard](../images/AzureOpenAIDashboard.png)
