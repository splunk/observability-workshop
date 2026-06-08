---
title: 4.4 グラフの定義
linkTitle: 4.4 グラフの定義
weight: 4
---

## グラフの定義方法

グラフは `build_workflow()` で明示的に構築されます

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

ルーティングロジックは以下の通りです

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

条件付きエッジを使用していますが、ワークフローは実質的にリニア（直線的）です

* start
* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer
* end

### 理解度チェック

ワークフローが実質的にリニアであるなら、なぜグラフは `add_conditional_edges` と `should_continue()` ルーターを使用しているのでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
ワークフローを**柔軟で拡張可能**にするためです。現在のフローはリニアですが、ルーティング関数によりグラフはステートに基づいて次のノードを動的に決定できます。これにより、グラフを再設計することなく、将来的に分岐、リトライ、または異なる実行パスを簡単に追加できるようになります。
{{< /details >}}
