---
title: Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
linkTitle: 2. Azure OpenAI メトリクス、ダッシュボード、ナビゲーターの確認
weight: 2
time: 10 minutes
---

このワークショップでは、Azure で動作する OpenAI モデルを使用します。

Azure OpenAI アプリケーションから Splunk Observability Cloud にメトリクスを送信するよう設定することで、Azure OpenAI アプリケーションのパフォーマンスを監視できます。

ワークショップ用の Splunk Observability Cloud インスタンスには、[ドキュメント](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cloud-services/azure-openai)に記載されている手順に従って、Azure アカウントとの統合が既に設定されています。

Azure OpenAI メトリクスが含まれるようにするため、`Cognitive Services` からメトリクスを取得するよう接続が設定されています

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

> 注意[このリンク](https://app.us1.signalfx.com/#/chart/v2/new?template=default&filters=sf_metric:ProcessedPromptTokens)を使用して **Metric finder** でこのメトリクスを表示することもできます。

![Processed Prompt Tokens Metric](../images/ProcessedPromptTokensMetric.png)

## Azure OpenAI Navigator

Splunk Observability Cloud は、OpenTelemetry の生成 AI クライアントおよびモデルサーバーメトリクスを収集し、Azure で動作する OpenAI 大規模言語モデル（LLM）サービスのトークン使用状況を追跡します。

これらのメトリクスは Azure OpenAI Navigator を使用して表示できます。**Infrastructure** -> **Overview** -> **AI Frameworks** に移動し、**Azure OpenAI** をクリックします。

**Table** タブが選択されていることを確認し、テーブル内の `gpt-4.1-mini` モデルをクリックします。以下のようなナビゲーターが表示されます

![Azure OpenAI Navigator](../images/AzureOpenAINavigator.png)

## Azure OpenAI Dashboard

Splunk Observability Cloud は、Azure OpenAI 用の組み込みダッシュボードを提供しており、以下の項目をすぐに可視化できます

* アクティブな Azure OpenAI モデル
* トークン使用量
* 呼び出しレイテンシー
* モデル別の呼び出し回数
* 最初のバイトまでの時間
* 合計応答時間
* モデルの可用性
* リクエストあたりのトークン数
* モデル別の処理済みトークン数
* モデル別の生成済みトークン数

**Dashboards** に移動し、**Azure OpenAI** を検索してダッシュボードを表示します

![Azure OpenAI Dashboard](../images/AzureOpenAIDashboard.png)
