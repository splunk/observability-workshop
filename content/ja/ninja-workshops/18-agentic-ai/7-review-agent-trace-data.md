---
title: エージェントトレースデータの確認
linkTitle: 7. エージェントトレースデータの確認
weight: 7
time: 10分
---

## Splunk Observability Cloud でトレースデータを確認する

Splunk Observability Cloud で、`APM` に移動し、`Service Map` を選択します。
環境名が選択されていることを確認してください（例`agentic-ai-$INSTANCE`）。
以下のようなサービスマップが表示されるはずです

![Service Map](../images/ServiceMap.png)

右側のメニューで `Traces` をクリックします。次に、実行時間が長いトレースの1つを選択します。以下の例のように表示されるはずです

![Trace](../images/Trace.png)

**Agent flow** セクションにエージェント名（coordinator、flight-specialist など）が表示されていないことに注目してください。

下にスクロールして、トレース内の AI インタラクションの1つをクリックしましょう。ここでは、プロンプトとレスポンスがキャプチャされていることが確認できます。また、このトレースのセマンティック品質評価の結果も確認できます

![Trace Details](../images/TraceDetails.png)

次に、`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認してください（例`agentic-ai-$INSTANCE`）。ページが空であることに気づくでしょう！

![Agents](../images/Agents.png)

これらの計装の問題については、次のセクションで対処します。
