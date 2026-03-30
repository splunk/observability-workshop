---
title: Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
linkTitle: 2. Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
weight: 2
time: 10 minutes
---

このワークショップでは、Azureで実行されるOpenAIモデルを使用します。

Azure OpenAIアプリケーションのパフォーマンスは、Azure OpenAIアプリケーションを設定してSplunk Observability Cloudにメトリクスを送信することで監視できます。

このワークショップのSplunk Observability Cloudインスタンスには、[ドキュメント](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cloud-services/azure-openai)に記載されている手順に従って、すでにAzureアカウントを統合しています。

Azure OpenAIメトリクスが含まれるようにするため、接続は `Cognitive Services` からメトリクスを取得するように設定されています：

![Azure connection](../images/AzureConnection.png)

## Azure OpenAI メトリクス

Azure OpenAIでは、多数のメトリクスがキャプチャされます：

* ProcessedPromptTokens
* GeneratedTokens
* AzureOpenAIRequests
* AzureOpenAITimeToResponse
* AzureOpenAIAvailabilityRate
* AzureOpenAITokenPerSecond
* AzureOpenAIContextTokensCacheMatchRate

**Metrics** -> **Metric finder** に移動し、`ProcessedPromptTokens` メトリクスを検索して **View in chart** をクリックします：

![Processed Prompt Tokens Metric](../images/ProcessedPromptTokensMetric.png)

## Azure OpenAI ナビゲーター

Splunk Observability Cloudは、OpenTelemetryの生成AIクライアントおよびモデルサーバーのメトリクスを収集し、Azureで実行されるOpenAIの大規模言語モデル（LLM）サービスのトークン使用量を追跡します。

これらのメトリクスはAzure OpenAIナビゲーターを使用して表示できます。**Infrastructure** -> **AI Frameworks** に移動し、**Azure OpenAI** をクリックします：

![Azure OpenAI Navigator](../images/AzureOpenAINavigator.png)

## Azure OpenAI ダッシュボード

Splunk Observability Cloudは、Azure OpenAI用の組み込みダッシュボードを提供しており、以下の項目をすぐに可視化できます：

* アクティブなAzure OpenAIモデル
* トークン使用量
* 呼び出しレイテンシ
* モデル別の呼び出し数
* 最初のバイトまでの時間
* 合計レスポンス時間
* モデルの可用性
* リクエストごとのトークン数
* モデルが処理したトークン数
* モデルが生成したトークン数

**Dashboards** に移動し、**Azure OpenAI** を検索してダッシュボードを表示します：

![Azure OpenAI Dashboard](../images/AzureOpenAIDashboard.png)
