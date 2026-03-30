---
title: Agentic AI アプリケーションアーキテクチャ
linkTitle: 4. Agentic AI アプリケーションアーキテクチャ
weight: 4
time: 20 minutes
---

## アプリケーション概要

このワークショップでは、旅行予約用の **Agentic AI** アプリケーションを使用します。
**OpenTelemetry** でアプリケーションを計装する前に、アプリケーションがどのように動作するかを理解しておくと役立ちます。

このアプリケーションは、旅行計画リクエストを受け付け、LangChainを活用した複数のLLMノードで構成される **LangGraph** ワークフローを通じて処理する **Flask API** です。各ノードは特定の役割を果たし、共有状態を更新して、次のステップに引き継ぎます。

このパートでは、以下の内容を確認します：

* リクエストのライフサイクル
* 共有状態モデル
* LangGraphノードの動作方法
* コードで使用されているLangChainの抽象化
* 後でオブザーバビリティが重要になる箇所

### アプリケーションの機能

大まかに言うと、このアプリケーションはリクエストを受け取り、マルチステップワークフローに変換します：

* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer

メインフローは次のようになります：

```python
@app.route("/travel/plan", methods=["POST"])
def plan():
    data = request.get_json()

    origin = data.get("origin", "Seattle")
    destination = data.get("destination", "Paris")
    user_request = data.get(
        "user_request",
        f"Planning a week-long trip from {origin} to {destination}. "
        "Looking for boutique hotel, flights and unique experiences.",
    )
    travellers = int(data.get("travellers", 2))

    result = plan_travel_internal(
        origin=origin,
        destination=destination,
        user_request=user_request,
        travellers=travellers
    )

    return jsonify(result), 200
```

これを分かりやすく説明すると：

1. Flaskがリクエストを受信します
2. `plan_travel_internal()` がワークフローの状態を構築します
3. LangGraphがノードを実行します
4. 各ノードが状態を更新します
5. 最終的な旅程がJSONとして返されます

### LangGraph の共有状態

このアプリで最も重要なLangGraphの概念は、共有状態オブジェクトです：

```python
class PlannerState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_request: str
    session_id: str
    origin: str
    destination: str
    departure: str
    return_date: str
    travellers: int
    flight_summary: Optional[str]
    hotel_summary: Optional[str]
    activities_summary: Optional[str]
    final_itinerary: Optional[str]
    current_agent: str
```

この状態はグラフ内をノードからノードへと移動します。

各ノードは：

* 状態から値を読み取ります
* 何らかの処理を行います
* 新しい値を状態に書き戻します
* 次に何が起こるかを制御するためにcurrent_agentを設定します

これがLangGraphの重要なメンタルモデルです：**ステートフルなワークフローオーケストレーション**。

また、このフィールドにも注目する価値があります：

```python
messages: Annotated[List[AnyMessage], add_messages]
```

これはLangGraphに対して、リストを上書きするのではなく、新しいメッセージを追加するよう指示します。これにより、アプリケーションはステップ間で会話履歴を保持します。

### 実行の開始位置

メインのオーケストレーションは `plan_travel_internal()` で行われます：

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

この関数は次のアプリケーションライフサイクルを実装しています：

* 初期状態を構築
* グラフを構築
* コンパイル
* ステップごとにストリーム実行

### グラフの定義方法

グラフは `build_workflow()` で明示的に構築されます：

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

ルーティングロジックはここにあります：

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

条件付きエッジを使用していますが、ワークフローは実質的に線形です：

* start
* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer
* end

### ノードの動作方法

このアプリのLangGraphノードは、状態を受け取り、更新された状態を返す単なるPython関数です。

たとえば、flight specialist：

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

これは一般的なノードパターンを示しています：

1. LLMを作成またはアクセスします
2. 構造化された状態からプロンプトを構築します
3. モデルを呼び出します
4. 結果を状態に保存します
5. 次のノードを設定します

hotelノードとactivityノードも同じ構造に従っているため、ワークフローの説明が容易です。

### ノードで使用されている LangChain の概念

アプリケーションは、1つの長いプロンプト文字列ではなく、LangChainのメッセージ抽象化を使用しています。

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

これが重要なのは、各ノードで以下を分離できるためです：

* システムロール
* ユーザータスク
* モデルの応答

たとえば：

```python
messages = [
    SystemMessage(content="You are a flight booking specialist. Provide concise options."),
    HumanMessage(content=step),
]
result = llm.invoke(messages)
```

LLM自体はここで作成されます：

```python
def _create_llm(agent_name: str, *, temperature: float, session_id: str) -> AzureChatOpenAI:
    azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    return AzureChatOpenAI(
        azure_deployment=azure_deployment_name,
        openai_api_version=azure_openai_api_version,
        temperature=temperature,
    )
```

このアプローチにより、モデル構成とワークフローロジックが分離されます。
ノードごとに、どの程度決定論的または創造的であるべきかに応じて、異なるtemperatureを使用できます。

### synthesizer が示す分解パターン

最後のノードは、specialistの出力を1つの回答にまとめます。

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

これはagenticアプリの典型的なパターンです：

* 作業をspecialistに分解する
* 中間出力を収集する
* 最終的な応答に統合する

これが、この概要から持ち帰るべき主要なアーキテクチャのアイデアの1つです。
