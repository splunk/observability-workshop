---
title: LangChain Callbackの追加
linkTitle: 3. LangChain Callbackの追加
weight: 3
time: 5 minutes
---

Galileoの `GalileoCallback` は標準的なLangChainコールバックハンドラーです。LangChainまたはLangGraphの実行にアタッチすると、プロンプト、レスポンス、モデル名、トークン使用量、タイミング、および各ステップのネストを自動的にキャプチャします。

トラベルプランナーはLangGraphワークフローであるため、すべてのノードを編集する必要はありません。代わりに、コンパイルされたグラフをストリームする際にrun configで単一のコールバックを渡します。Splunk Agent Observabilityはリクエストごとに1つのTraceを記録し、各エージェントノード（coordinator、flight、hotel、activity、synthesizer）にネストされたLLM Spanを作成します。

{{< exercise title="LangChain Callbackの追加" >}}

{{< step title="コールバックのインポート"  >}}

`main.py` の他のLangChainインポートと一緒にコールバックのインポートを追加します。

```python
from galileo.handlers.langchain import GalileoCallback
```

{{< /step >}}

{{< step title="グラフのrun configにコールバックをアタッチ"  >}}
`plan_travel_internal()` でコールバックを作成し、`compiled_app.stream(...)` に渡すrun configにアタッチします。既存のコードは以下のようになっているはずです。

```python
    workflow = build_workflow()
    compiled_app = workflow.compile()

    for step in compiled_app.stream(initial_state, config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
```

   Splunk Agent Observabilityコールバックを含むconfigを構築するように更新します（アプリが既に渡している既存のconfigとマージします）。これにより、エージェント内の各ノードの実行がSplunk Agent Observabilityに渡されます。

```python
    workflow = build_workflow()
    compiled_app = workflow.compile()

    # One callback per request keeps each travel plan in its own trace.
    callback = GalileoCallback()
    run_config = {**config, "callbacks": [callback]}

    for step in compiled_app.stream(initial_state, run_config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
```

グラフレベルでコールバックを渡すことで、すべてのノードの `llm.invoke(...)` 呼び出しに自動的に伝播します。追加の計装は不要です。

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認テスト" >}}

LangGraphワークフローで `GalileoCallback` をどこにアタッチしますか？

{{% notice title="非同期ワークフロー" style="blue" icon="info-circle" %}}
アプリがグラフを非同期でストリームする場合（`compiled_app.astream(...)`）、`GalileoCallback` の代わりに `GalileoAsyncCallback` を使用します。トラベルプランナーは同期的に実行されるため、ここでは `GalileoCallback` が正しい選択です。
{{% /notice %}}
