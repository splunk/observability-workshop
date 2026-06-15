---
title: LangChain アプリ向け Galileo 計装
linkTitle: LangChain アプリ向け Galileo 計装
weight: 19
layout: chapter
time: 40 minutes
authors: ["Sam Goldfield"]
description: LangChain アプリに Galileo（Splunk Agent Observability）トレーシングを追加し、コンソール UI でトレースを確認します。
draft: false
hidden: false
aliases:
  - /ninja-workshops/19-agent-observability-galileo/
product: "Observability Cloud"
---

このワークショップはワークショップ 18 の続きで、LangChain アプリに Galileo を計装する最短の手順を紹介します。

ワークショップ [Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/) で使用した**マルチエージェント旅行プランナー**を再利用します。これは LangGraph ワークフローで構成された Flask API であり、各ノード（coordinator、flight specialist、hotel specialist、activity specialist、synthesizer）が LangChain を通じて LLM を呼び出します。テレメトリを Splunk Observability Cloud に送信する代わりに、Galileo（Splunk Agent Observability）でトレースします。

{{< objectives title="目標" >}}

* Galileo SDK をインストールし、必要な環境変数を設定します。
* 旅行プランナーに Galileo コンテキストの初期化と LangChain コールバックを追加します。
* 実際の旅行計画リクエストを実行し、Galileo コンソールでマルチエージェントのフルトレースを確認します。

{{< /objectives >}}

{{% notice style="info" title="主な参考資料" %}}

* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{% /notice %}}
