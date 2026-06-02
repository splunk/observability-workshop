---
title: 4.5 ノードの定義
linkTitle: 4.5 ノードの定義
weight: 5
---

## ノードの動作の仕組み

このアプリケーションにおける LangGraph のノードは、状態を受け取って更新後の状態を返す Python 関数にすぎません。

例えば、flight specialist は次のようになります。

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

このコードは、ノードに共通するパターンを示しています。

1. LLM を作成またはアクセスする
2. 構造化された状態からプロンプトを組み立てる
3. モデルを呼び出す
4. 結果を状態に保存する
5. 次のノードを設定する

hotel ノードと activity ノードも同じ構造に従っているため、ワークフローを説明しやすくなっています。

### 理解度チェック

`flight_specialist` ノード用の LLM を作成する際、temperature を `0.4` に指定しました。これは何を意味しているでしょうか。

<details>
  <summary><b>クリックして回答を表示</b></summary>

temperature は、モデルの応答がどの程度ランダム、または創造的になるかを制御するパラメーターです。

* **低い temperature（例：0.0〜0.3）**：より決定論的で一貫性のある応答になります
* **中程度（およそ 0.4〜0.7）**：正確性と創造性のバランスが取れた応答になります
* **高い temperature（0.8 以上）**：より多様で創造的になりますが、予測しづらくなります

つまり **temperature=0.4** に設定することは、`flight_specialist` エージェントが **大部分は一貫性があり信頼できる応答を生成しつつ、わずかなばらつきも含む** 応答を返すことを意味します。これは、正確性を求めつつも完全に固定的な回答にはしたくないタスクに適しています。

</details>
