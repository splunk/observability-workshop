---
title: Azure OpenAI のメトリクス、ダッシュボード、Navigator を確認する
linkTitle: 2. Azure OpenAI のメトリクス、ダッシュボード、Navigator を確認する
weight: 2
time: 10 minutes
---

このワークショップでは、Azure 上で動作する OpenAI モデルを使用します。

Azure OpenAI アプリケーションのパフォーマンスは、Azure OpenAI アプリケーションが Splunk Observability Cloud にメトリクスを送信するように構成することで監視できます。

[ドキュメント](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-infrastructure-monitoring/set-up-data-integrations/cloud-services/azure-openai) に記載されている手順に従って、Azure アカウントはすでにワークショップ用の Splunk Observability Cloud インスタンスと連携済みです。

Azure OpenAI のメトリクスが含まれるようにするため、`Cognitive Services` からメトリクスを取得するよう接続が構成されています。

![Azure connection](../images/AzureConnection.png)

## Azure OpenAI のメトリクス

Azure OpenAI では、以下のような複数のメトリクスが取得されます。

* ProcessedPromptTokens
* GeneratedTokens
* AzureOpenAIRequests
* AzureOpenAITimeToResponse
* AzureOpenAIAvailabilityRate
* AzureOpenAITokenPerSecond
* AzureOpenAIContextTokensCacheMatchRate

**Metrics** -> **Metric finder** に移動し、`ProcessedPromptTokens` メトリクスを検索して **View in chart** をクリックします。

> 注: [このリンク](https://app.us1.signalfx.com/#/chart/v2/new?template=default&filters=sf_metric:ProcessedPromptTokens) からも、このメトリクスを **Metric finder** で表示できます。

![Processed Prompt Tokens Metric](../images/ProcessedPromptTokensMetric.png)

## Azure OpenAI Navigator

Splunk Observability Cloud は、OpenTelemetry の生成 AI クライアントおよびモデルサーバーのメトリクスを収集し、Azure 上で動作する Open AI 大規模言語モデル (LLM) サービスのトークン使用量を追跡します。

これらのメトリクスは、Azure OpenAI navigator で確認できます。**Infrastructure** -> **Overview** -> **AI Frameworks** に移動し、**Azure OpenAI** をクリックします。

**Table** タブが選択されていることを確認し、テーブル内の `gpt-4.1-mini` モデルをクリックします。次のような navigator が表示されるはずです。

![Azure OpenAI Navigator](../images/AzureOpenAINavigator.png)

## Azure OpenAI ダッシュボード

Splunk Observability Cloud には、Azure OpenAI 用の組み込みダッシュボードが用意されており、以下の情報をすぐに確認できます。

* アクティブな Azure OpenAI モデル
* トークン使用量
* 呼び出しのレイテンシ
* モデル別の呼び出し回数
* Time to first byte
* 合計レスポンス時間
* モデルの可用性
* リクエストあたりのトークン数
* モデルが処理したトークン数
* モデルが生成したトークン数

**Dashboards** に移動し、**Azure OpenAI** を検索してダッシュボードを表示します。

![Azure OpenAI Dashboard](../images/AzureOpenAIDashboard.png)
