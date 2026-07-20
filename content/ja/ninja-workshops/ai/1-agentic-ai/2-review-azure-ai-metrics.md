---
title: Azure OpenAI Metrics、Dashboards、Navigatorsの確認
linkTitle: 2. Azure OpenAI Metrics、Dashboards、Navigatorsの確認
weight: 2
time: 10 minutes
---

このワークショップでは、Azureで実行されるOpenAIモデルを使用します。

Azure OpenAIアプリケーションからSplunk Observability Cloudにメトリクスを送信するよう設定することで、Azure OpenAIアプリケーションのパフォーマンスをモニタリングできます。

このワークショップのSplunk Observability Cloudインスタンスには、[ドキュメント](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cloud-services/azure-openai)に記載された手順に従って、すでにAzureアカウントを統合済みです。

Azure OpenAIメトリクスが含まれるようにするため、接続は `Cognitive Services` からメトリクスを取得するよう設定されています。

![Azure connection](../images/AzureConnection.png)

## Azure OpenAI Metrics

Azure OpenAIでは、以下のメトリクスが取得されます。

* ProcessedPromptTokens
* GeneratedTokens
* AzureOpenAIRequests
* AzureOpenAITimeToResponse
* AzureOpenAIAvailabilityRate
* AzureOpenAITokenPerSecond
* AzureOpenAIContextTokensCacheMatchRate

**Metrics** -> **Metric finder** に移動し、`ProcessedPromptTokens` メトリクスを検索して **View in chart** をクリックします。

> [!NOTE]
> [このリンク](https://app.us1.signalfx.com/#/chart/v2/new?template=default&filters=sf_metric:ProcessedPromptTokens)を使用して **Metric finder** でこのメトリクスを表示することもできます。

![Processed Prompt Tokens Metric](../images/ProcessedPromptTokensMetric.png)

## Azure OpenAI Navigator

Splunk Observability Cloudは、OpenTelemetryの生成AIクライアントおよびモデルサーバーメトリクスを収集し、Azureで実行されているOpen AI大規模言語モデル（LLM）サービスのトークン使用量を追跡します。

これらのメトリクスはAzure OpenAI Navigatorを使用して確認できます。**Infrastructure** -> **Overview** -> **AI Frameworks** に移動し、**Azure OpenAI** をクリックします。

**Table** タブが選択されていることを確認し、テーブル内の `gpt-4.1-mini` モデルをクリックします。以下のようなNavigatorが表示されます。

![Azure OpenAI Navigator](../images/AzureOpenAINavigator.png)

## Azure OpenAI Dashboard

Splunk Observability Cloudは、Azure OpenAI用の組み込みダッシュボードを提供しており、以下の項目を即座に可視化できます。

* アクティブなAzure OpenAIモデル
* トークン使用量
* 呼び出しレイテンシー
* モデル別の呼び出し数
* 最初のバイトまでの時間
* 合計レスポンス時間
* モデルの可用性
* リクエストあたりのトークン数
* モデル別の処理済みトークン数
* モデル別の生成済みトークン数

**Dashboards** に移動し、**Azure OpenAI** を検索してダッシュボードを表示します。

![Azure OpenAI Dashboard](../images/AzureOpenAIDashboard.png)
