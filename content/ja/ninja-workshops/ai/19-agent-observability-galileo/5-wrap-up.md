---
title: まとめ
linkTitle: 5. まとめ
weight: 5
time: 20 minutes
---

[Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/) のマルチエージェント旅行プランナーに、`galileo_context.init(...)` と LangGraph の run config への `GalileoCallback` の追加という2つの変更だけで、Galileo（Splunk Agent Observability）によるインストルメンテーションを実装しました。

これにより、各エージェントノードの LLM 呼び出しが、リクエストごとに1つの Galileo トレース内のネストされたスパンとして表示されるようになりました。ノードごとの変更は不要で、メンテナンスコストも非常に低くなっています。

同じワークロードが **2つ** のオブザーバビリティツール（[Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/) での Splunk Observability Cloud と、ここでの Galileo）でトレースされるようになり、比較のための有用な基盤ができました。

次のステップでは、以下の内容に取り組みます

* キャプチャされたトレースに Galileo メトリクス（例`Context Adherence`）を追加する。
* Galileo がエージェントのより良いオブザーバビリティをサポートする機能を活用する。
* Signals などの強力な機能を活用する。
* 専用の `GalileoLogger(project=..., log_stream=...)` を使用して、特定の実行を異なるログストリームにルーティングする。
* エージェントにさらなる複雑さを追加する。

## 参考資料

* [Galileo Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{< checkpoint title="Workshop complete -- **nice work!**" >}}
