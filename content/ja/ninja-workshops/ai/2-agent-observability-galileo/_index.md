---
title: LangChainアプリ向けSplunk Agent Observability計装
linkTitle: LangChainアプリ向けSplunk Agent Observability計装
weight: 2
layout: chapter
time: 40 minutes
authors: ["Sam Goldfield"]
description: LangChainアプリにSplunk Agent Observabilityトレーシングを追加し、コンソールUIでトレースを確認します。
aliases:
  - /ninja-workshops/19-agent-observability-galileo/
product: "Observability Cloud"
---

このワークショップはワークショップ18の続きで、LangChainアプリにSplunk Agent Observability（Galileo搭載）を計装する最短の方法を示します。

ワークショップ [Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/) の **マルチエージェント旅行プランナー** を再利用します。これはLangGraphワークフローに支えられたFlask APIで、各ノード（coordinator、flight specialist、hotel specialist、activity specialist、synthesizer）がLangChainを通じてLLMを呼び出します。テレメトリをSplunk Observability Cloudに送信する代わりに、Splunk Agent Observabilityでトレースします。

{{< objectives title="目標" >}}

* Splunk Agent Observability SDKをインストールし、必要な環境変数を設定します。
* 旅行プランナーにSplunk Agent Observabilityのコンテキスト初期化と単一のLangChainコールバックを追加します。
* 実際の旅行計画リクエストを実行し、Splunk Agent Observabilityコンソールで完全なマルチエージェントトレースを確認します。

{{< /objectives >}}

{{% notice style="info" title="主要リファレンス" %}}

* [Splunk Agent Observability Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Splunk Agent Observability LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{% /notice %}}
