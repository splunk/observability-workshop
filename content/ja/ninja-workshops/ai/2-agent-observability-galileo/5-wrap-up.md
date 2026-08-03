---
title: まとめ
linkTitle: 5. まとめ
weight: 5
time: 20 minutes
---

ワークショップ [Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/) のマルチエージェント旅行プランナーに、たった2つの追加（`galileo_context.init(...)` と LangGraph の run config への `GalileoCallback`）だけで Splunk Agent Observability の計装を行いました。
これにより、各エージェントノードの LLM 呼び出しが、リクエストごとに1つの Splunk Agent Observability トレース内のネストされた Span として表示されるようになりました。ノードごとの変更は不要で、メンテナンスコストも非常に低く抑えられます。

これで、同じワークロードが2つのオブザーバビリティツール（[Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/) で使用した Splunk Observability Cloud と、ここでの Splunk Agent Observability）でトレースされる状態になりました。これは比較の基盤として有用です。Agent Observability で確認できて Observability Cloud では確認できないもの、またその逆は何でしょうか？

次のステップでは、以下の内容に取り組みます。

* キャプチャされたトレースに Splunk Agent Observability のメトリクス（例: `Context Adherence`）を追加する
* Splunk Agent Observability がエージェントのオブザーバビリティをより良くサポートする機能を確認する
* AI Assistant の Signals などの強力な機能を活用する
* 専用の `GalileoLogger(project=..., log_stream=...)` を使用して、特定の実行を異なるログストリームにルーティングする
* エージェントにさらなる複雑性を追加する

## リファレンス

* [Splunk Agent Observability Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Splunk Agent Observability LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)
