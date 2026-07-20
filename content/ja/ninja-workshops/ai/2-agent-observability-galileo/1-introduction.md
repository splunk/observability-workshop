---
title: はじめに
linkTitle: 1. Introduction
weight: 1
time: 5 minutes
---

[Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/)では、**agentic AI travel planner** の計装と観測を行いました。このアプリケーションは **LangGraph** ワークフローをラップした **Flask API** であり、各ノード（coordinator、flight specialist、hotel specialist、activity specialist、synthesizer）が **LangChain** の `ChatOpenAI` を通じてLLMを呼び出します。

この後続のワークショップでは、同じアプリケーションに **Splunk Agent Observability instrumentation** を追加します。ゼロから再計装するのではなく、LangGraphワークフローに単一のSplunk Agent Observabilityコールバックをアタッチすることで、すべてのエージェントのLLM呼び出しをキャプチャします。これにより、すでに理解しているワークロードを使用して、ツール間でAIトレースの可視性を比較・検証できます。

{{% prerequisites title="前提条件" %}}

* ワークショップ18のtravel plannerアプリ（`~/workshop/agentic-ai/base-app`）、またはそのコピー
* Splunk Agent Observabilityアカウントおよび APIキー
* OpenAI APIキー（アプリがすでに使用している `OPENAI_API_KEY` と同じもの）
* パッケージインストールが可能なPython 3.10以上の環境

{{% /prerequisites %}}
