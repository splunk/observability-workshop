---
title: はじめに
linkTitle: 1. はじめに
weight: 1
time: 5 minutes
---

[Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/) では、**agentic AI travel planner** を計装し、観測しました。このアプリケーションは **LangGraph** ワークフローをラップした **Flask API** であり、各ノード（coordinator、flight specialist、hotel specialist、activity specialist、synthesizer）が **LangChain** の `ChatOpenAI` を通じて LLM を呼び出します。

このフォローアップワークショップでは、同じアプリケーションに **Galileo instrumentation** を追加します。ゼロから再計装するのではなく、LangGraph ワークフローに単一の Galileo コールバックをアタッチすることで、すべてのエージェントの LLM 呼び出しをキャプチャします。これにより、すでに理解しているワークロードを使用して、ツール間で AI トレースの可視性を比較・検証できます。

{{% prerequisites title="前提条件" %}}

* Workshop 18 の travel planner アプリ（`~/workshop/agentic-ai/base-app`）、またはそのコピー。
* Galileo アカウントと API キー。
* OpenAI API キー（ワークショップインスタンスには `OPENAI_API_KEY` が事前定義されています）。
* パッケージインストールが可能な Python 3.10+ 環境。

{{% /prerequisites %}}
