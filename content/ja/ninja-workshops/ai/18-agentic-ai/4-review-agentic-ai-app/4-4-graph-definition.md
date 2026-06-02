---
title: 4.4 グラフの定義
linkTitle: 4.4 グラフの定義
weight: 4
---

## グラフの定義方法

グラフは `build_workflow()` の中で明示的に構築されています。

```python
def build_workflow() -> StateGraph:
    graph = StateGraph(PlannerState)
    graph.add_node("coordinator", lambda state: coordinator_node(state))
    graph.add_node("flight_specialist", lambda state: flight_specialist_node(state))
    graph.add_node("hotel_specialist", lambda state: hotel_specialist_node(state))
    graph.add_node("activity_specialist", lambda state: activity_specialist_node(state))
    graph.add_node("plan_synthesizer", lambda state: plan_synthesizer_node(state))
    graph.add_conditional_edges(START, should_continue)
    graph.add_conditional_edges("coordinator", should_continue)
    graph.add_conditional_edges("flight_specialist", should_continue)
    graph.add_conditional_edges("hotel_specialist", should_continue)
    graph.add_conditional_edges("activity_specialist", should_continue)
    graph.add_conditional_edges("plan_synthesizer", should_continue)
    return graph
```

ルーティングロジックは次のとおりです。

```python
def should_continue(state: PlannerState) -> str:
    mapping = {
    "start": "coordinator",
    "flight_specialist": "flight_specialist",
    "hotel_specialist": "hotel_specialist",
    "activity_specialist": "activity_specialist",
    "plan_synthesizer": "plan_synthesizer",
    }
    return mapping.get(state["current_agent"], END)
```

このグラフは条件付きエッジを使っていますが、ワークフローは実質的に直線的な流れです。

* start
* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer
* end

### 理解度チェック

ワークフローが実質的に直線的であるにもかかわらず、なぜグラフは
`add_conditional_edges` と `should_continue()` ルーターを使っているのでしょうか？

<details>
  <summary><b>クリックして回答を表示</b></summary>

ワークフローを **柔軟かつ拡張可能** にするためです。現在の流れは直線的ですが、
ルーティング関数によってグラフは状態に基づいて次のノードを動的に決定できます。
これにより、グラフを再設計することなく、後から分岐やリトライ、異なる実行パスを
追加することが容易になります。

</details>
