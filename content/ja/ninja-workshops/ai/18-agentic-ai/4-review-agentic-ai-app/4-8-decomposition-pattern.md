---
title: 4.8 Decomposition Pattern
linkTitle: 4.8 Decomposition Pattern
weight: 8
---

### Synthesizer が decomposition パターンを示す

最後のノードは、各スペシャリストの出力を1つの回答に統合します。

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

これは agentic アプリにおける典型的なパターンです。

* 作業をスペシャリストへ分解する
* 中間出力を収集する
* 最終的なレスポンスへ統合する

これは、この概要から押さえておくべき主要なアーキテクチャ上の考え方の1つです。

### Knowledge Check

なぜこのアプリは1つのエージェントに旅行プラン全体を生成させるのではなく、別の `plan_synthesizer` ノードを使うのでしょうか?

<details>
  <summary><b>Click here to see the answer</b></summary>

このシステムは、まず問題を**専門化されたタスク**(フライト、ホテル、アクティビティ)へ分割するためです。各スペシャリストは焦点を絞ったサマリーを作成し、その後 `plan_synthesizer` ノードが**それらの出力を1つの一貫した旅程に統合します**。

このパターンは**モジュール性、信頼性、可観測性**を向上させます。各エージェントがより小さな問題を扱い、最終ノードが結果を統合するためです。

</details>
