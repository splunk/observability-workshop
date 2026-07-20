---
title: 4.3 オーケストレーション
linkTitle: 4.3 オーケストレーション
weight: 3
---
### 実行の起点

メインのオーケストレーションは `plan_travel_internal()` で行われます:

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

この関数は以下のアプリケーションライフサイクルを実装しています:

* 初期状態を構築する
* グラフを構築する
* グラフをコンパイルする
* ステップごとにストリーム実行する

### 知識チェック

#### 質問 1

なぜこのコードでは、グラフを一度呼び出して最終結果を取得するのではなく、`compiled_app.stream(initial_state, config)` を使用しているのでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
ストリーミングはワークフローを **各ノードの実行ごとにステップバイステップで** 実行するためです。これにより、アプリケーションは中間状態を観察し、どのノードが実行中かを追跡し、最終出力を待つだけでなくリアルタイムでワークフローをモニタリングできます。
{{< /details >}}

#### 質問 2

なぜグラフを実行する前に `initial_state` を作成するのでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
LangGraphのワークフローは共有状態オブジェクト上で動作するためです。`initial_state` は、ワークフローの進行に伴ってノードが読み取り、更新し、受け渡す開始データを提供します。
{{< /details >}}
