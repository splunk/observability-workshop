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

このワークショップは、ワークショップ[Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/)の続きとして、LangChainアプリにSplunk Agent Observability（Galileo搭載）を計装する最短の手順を紹介します。

ワークショップ[Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/)で使用した **マルチエージェント旅行プランナー** を再利用します。これはLangGraphワークフローで構成されたFlask APIであり、各ノード（coordinator、flight specialist、hotel specialist、activity specialist、synthesizer）がLangChainを通じてLLMを呼び出します。テレメトリをSplunk Observability Cloudに送信する代わりに、Splunk Agent Observabilityでトレースします。

{{< objectives title="目標" >}}

* Splunk Agent Observability SDKをインストールし、必要な環境変数を設定します。
* 旅行プランナーにSplunk Agent Observabilityのコンテキスト初期化と単一のLangChainコールバックを追加します。
* 実際の旅行プランニングリクエストを実行し、Splunk Agent Observabilityコンソールでマルチエージェントのフルトレースを確認します。

{{< /objectives >}}

{{% notice style="info" title="主要リファレンス" %}}

* [Splunk Agent Observability Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Splunk Agent Observability LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{% /notice %}}
