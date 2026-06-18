---
title: LangChain Callback の追加
linkTitle: 3. LangChain Callback の追加
weight: 3
time: 5 minutes
---

Galileo の `GalileoCallback` は標準的な LangChain コールバックハンドラーです。LangChain または LangGraph の実行にアタッチすると、プロンプト、レスポンス、モデル名、トークン使用量、タイミング、および各ステップのネスト構造を自動的にキャプチャします。

トラベルプランナーは **LangGraph** ワークフローであるため、すべてのノードを編集する必要はありません。代わりに、コンパイル済みグラフをストリーミングする際に **run config** で単一のコールバックを渡します。これにより、Galileo はリクエストごとに1つのトレースを記録し、各エージェントノード（coordinator、flight、hotel、activity、synthesizer）にネストされた LLM スパンを作成します。

{{< exercise title="LangChain callback の追加" >}}

{{< step title="コールバックのインポート"  >}}

`main.py` の他の LangChain インポートと一緒に、コールバックのインポートを追加します

```python
from galileo.handlers.langchain import GalileoCallback
```

{{< /step >}}

{{< step title="グラフの run config にコールバックをアタッチする"  >}}
`plan_travel_internal()` 内で、コールバックを作成し、`compiled_app.stream(...)` に渡される run config にアタッチします。既存のコードは次のようになっているはずです

```python
    for step in compiled_app.stream(initial_state, config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
        agent_steps.append({"agent": node_name, "status": "completed"})
```

Galileo コールバックを含む config を構築するように更新します（アプリが既に渡している既存の config とマージします）。これにより、エージェント内の各ノードの実行が Galileo に渡されます

```python
    # One callback per request keeps each travel plan in its own trace.
    callback = GalileoCallback()
    run_config = {**config, "callbacks": [callback]}

    for step in compiled_app.stream(initial_state, run_config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
        agent_steps.append({"agent": node_name, "status": "completed"})
```

グラフレベルでコールバックを渡すことで、すべてのノードの `llm.invoke(...)` 呼び出しに自動的に伝播されます。追加の計装は必要ありません。

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認テスト" >}}

サンプルアプリケーションで使用されている Galileo コールバックは同期型ですか、それとも非同期型ですか？

{{< details summary="ここをクリックして回答を確認" >}}
サンプルアプリケーションは同期型のコールバックを使用しています。

アプリがグラフを非同期にストリーミングする場合（`compiled_app.astream(...)`）は、`GalileoCallback` の代わりに `GalileoAsyncCallback` を使用します。トラベルプランナーは同期的に実行されるため、ここでは `GalileoCallback` が正しい選択です。
{{< /details >}}
