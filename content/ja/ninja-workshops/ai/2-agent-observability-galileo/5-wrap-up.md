---
title: まとめ
linkTitle: 5. まとめ
weight: 5
time: 20 minutes
---

ワークショップ18のマルチエージェント旅行プランナーに、たった2つの追加だけでSplunk Agent Observabilityを計装しました。`galileo_context.init(...)` と、LangGraphの実行設定への単一の `GalileoCallback` です。
これにより、すべてのエージェントノードのLLM呼び出しが、リクエストごとに1つのSplunk Agent Observabilityトレース内のネストされたSpanとして表示されるようになりました。ノードごとの変更は不要で、メンテナンスコストも非常に低く抑えられています。

同じワークロードが2つのオブザーバビリティツール（ワークショップ18のSplunk Observability Cloudと、ここでのSplunk Agent Observability）でトレースされている状態になりました。これは比較の良い基盤となります。Agent ObservabilityがObservability Cloudでは見えないものを何を示し、その逆はどうでしょうか？

次に、以下の内容でさらに拡張していきます。

* キャプチャされたトレースにSplunk Agent Observabilityメトリクス（例: `Context Adherence`）を追加する
* Splunk Agent Observabilityがエージェントのより良いオブザーバビリティをサポートする機能を活用する
* AI AssistantのSignalsなどの強力な機能を活用する
* 専用の `GalileoLogger(project=..., log_stream=...)` を使用して、特定の実行を異なるログストリームにルーティングする
* エージェントにさらなる複雑さを追加する

## 参考資料

* [Splunk Agent Observability Quickstart](https://docs.galileo.ai/getting-started/quickstart)
* [Splunk Agent Observability LangChain integration](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)
