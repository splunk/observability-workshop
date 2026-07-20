---
title: 4.5 ノードの定義
linkTitle: 4.5 ノードの定義
weight: 5
---

## ノードの仕組み

このアプリにおけるLangGraphのノードは、stateを受け取り、更新されたstateを返すPython関数です。

例えば、フライト専門エージェントは以下のようになります:

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )

    step = (
        f"Find an appealing flight from {state['origin']} to {state['destination']} "
        f"departing {state['departure']} for {state['travellers']} travellers."
    )

    messages = [
        SystemMessage(content="You are a flight booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = llm.invoke(messages)
    state["flight_summary"] = result.content
    state["messages"].append(result)
    state["current_agent"] = "hotel_specialist"
    return state
```

これは一般的なノードパターンを示しています:

1. LLMを作成またはアクセスする
2. 構造化されたstateからプロンプトを構築する
3. モデルを呼び出す
4. 結果をstateに保存する
5. 次のノードを設定する

ホテルノードとアクティビティノードも同じ構造に従っており、ワークフローの説明が容易になっています。

### 理解度チェック

`flight_specialist` ノードのLLMを作成する際に、temperatureを `0.4` に指定しました。これはどういう意味でしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
Temperatureは、モデルの応答がどの程度ランダムまたは創造的になるかを制御します。

* **低いtemperature（例: 0.0〜0.3）**: より決定論的で一貫した応答
* **中程度（0.4〜0.7付近）**: 正確さと創造性のバランス
* **高い（0.8以上）**: より多様で創造的だが、予測しにくい

つまり **temperature=0.4** を設定すると、`flight_specialist` エージェントは **ほぼ一貫性があり信頼性の高い、わずかなバリエーションを持つ** 応答を生成します。これは正確さが必要だが、完全に固定された回答でなくてもよいタスクに有用です。
{{< /details >}}
