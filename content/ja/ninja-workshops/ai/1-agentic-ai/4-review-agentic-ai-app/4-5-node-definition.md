---
title: 4.5 ノードの定義
linkTitle: 4.5 ノードの定義
weight: 5
---

## ノードの仕組み

このアプリにおける LangGraph のノードは、state を受け取り、更新された state を返す Python 関数です。

例えば、flight specialist は以下のようになります:

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

1. LLM を作成またはアクセスする
2. 構造化された state からプロンプトを構築する
3. モデルを呼び出す
4. 結果を state に保存する
5. 次のノードを設定する

hotel ノードと activity ノードも同じ構造に従っているため、ワークフローの説明が容易です。

### 知識チェック

`flight_specialist` ノードの LLM を作成する際に、temperature を `0.4` に指定しました。これはどういう意味でしょうか？

<details>
  <summary><b>ここをクリックして回答を確認</b></summary>

Temperature は、モデルの応答がどの程度ランダムまたは創造的になるかを制御します。

* **低い temperature（例: 0.0〜0.3）**: より決定論的で一貫した応答になります
* **中程度（約 0.4〜0.7）**: 正確性と創造性のバランスが取れています
* **高い（0.8 以上）**: より多様で創造的ですが、予測しにくくなります

つまり、**temperature=0.4** に設定すると、`flight_specialist` エージェントは**おおむね一貫性があり信頼できる応答を生成しつつ、わずかなバリエーション**を持たせることができます。これは正確性が求められるが、完全に固定的な回答は不要なタスクに適しています。

</details>
