---
title: 4.8 分解パターン
linkTitle: 4.8 Decomposition Pattern
weight: 8
---

### シンセサイザーが示す分解パターン

最後のノードは、各専門エージェントの出力を1つの回答に統合します。

```python
def plan_synthesizer_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "plan_synthesizer", temperature=0.3, session_id=state["session_id"]
    )

    content = json.dumps(
        {
            "flight": state["flight_summary"],
            "hotel": state["hotel_summary"],
            "activities": state["activities_summary"],
        },
        indent=2,
    )

    response = llm.invoke(
        [
            SystemMessage(
                content="You are the travel plan synthesiser. Combine the specialist insights into a concise, structured itinerary."
            ),
            HumanMessage(
                content=(
                    f"Traveller request: {state['user_request']}\n\n"
                    f"Origin: {state['origin']} | Destination: {state['destination']}\n"
                    f"Dates: {state['departure']} to {state['return_date']}\n\n"
                    f"Specialist summaries:\n{content}"
                )
            ),
        ]
    )
    state["final_itinerary"] = response.content
    state["messages"].append(response)
    state["current_agent"] = "completed"
    return state
```

これはエージェントアプリの典型的なパターンです

* 作業を専門エージェントに分解する
* 中間出力を収集する
* 最終的な応答に統合する

これが、この概要から学ぶべき主要なアーキテクチャのアイデアの1つです。

### 理解度チェック

なぜこのアプリは、1つのエージェントに旅行プラン全体を生成させるのではなく、
別の `plan_synthesizer` ノードを使用しているのでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
システムはまず問題を**専門的なタスク**に分割するためです（フライト、ホテル、アクティビティ）。
各専門エージェントが焦点を絞った要約を作成し、`plan_synthesizer` ノードが**それらの出力を
1つのまとまった旅程に統合**します。

このパターンは**モジュール性、信頼性、オブザーバビリティ**を向上させます。各エージェントが
より小さな問題を処理し、最終ノードが結果を統合するためです。
{{< /details >}}
