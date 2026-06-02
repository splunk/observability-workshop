---
title: 4.3 Orchestration
linkTitle: 4.3 Orchestration
weight: 3
---
### 実行が始まる場所

メインのオーケストレーションは `plan_travel_internal()` で行われます。

```python
def plan_travel_internal(
    origin: str,
    destination: str,
    user_request: str,
    travellers: int,
    ) -> Dict[str, object]:
    session_id = str(uuid4())
    departure, return_date = _compute_dates()

    initial_state: PlannerState = {
        "messages": [HumanMessage(content=user_request)],
        "user_request": user_request,
        "session_id": session_id,
        "origin": origin,
        "destination": destination,
        "departure": departure,
        "return_date": return_date,
        "travellers": travellers,
        "flight_summary": None,
        "hotel_summary": None,
        "activities_summary": None,
        "final_itinerary": None,
        "current_agent": "start",
    }

    workflow = build_workflow()
    compiled_app = workflow.compile()

    for step in compiled_app.stream(initial_state, config):
        node_name, node_state = next(iter(step.items()))
        final_state = node_state
```

この関数は、次のアプリケーションライフサイクルを実装しています。

* 初期状態 (initial state) を構築する
* グラフを構築する
* コンパイルする
* ステップごとに実行をストリーミングする

### 理解度チェック

#### 質問 1

このコードでは、なぜグラフを一度だけ呼び出して最終結果を取得するのではなく、
`compiled_app.stream(initial_state, config)` を使用しているのでしょうか?

<details>
  <summary><b>回答を表示するにはここをクリック</b></summary>

ストリーミングを使用すると、**各ノードが実行されるたびにステップごとに**ワークフローが実行されるためです。
これにより、アプリケーションは中間状態を観測し、どのノードが実行中かを追跡し、
最終的な出力を待つだけでなく、リアルタイムでワークフローを監視できます。

</details>

#### 質問 2

なぜグラフを実行する前に `initial_state` を作成するのでしょうか?

<details>
  <summary><b>回答を表示するにはここをクリック</b></summary>

LangGraph のワークフローは共有されたステートオブジェクトに対して動作するためです。`initial_state` は、
ワークフローが進行する中でノードが読み取り、更新し、引き継いでいくための開始データを
提供します。

</details>
