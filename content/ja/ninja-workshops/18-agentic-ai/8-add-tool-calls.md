---
title: Tool Call の追加
linkTitle: 8. Tool Call の追加
weight: 8
time: 15 minutes
---

前のセクションでは、エージェントが新しい **Agents** ページやトレース上部の **Agent flow** に表示されていないことを確認しました。

その理由は、現在のアプリケーションがエージェントを使用しておらず、代わりに LLM を直接呼び出しているためです。

言い換えると、現在のアプリは台本のある演劇のようなものです。すべてのセリフとすべてのアクションがコードに書かれています。LLM を呼び出すとき、特定のセリフを読むよう依頼しているだけです。LLM が選択を行わないため、Observability for AI の計装は自律エージェントとして認識しません。

次のセクションでは、LLM に **ツール** とそれらを使用する判断権限を与えます。エージェントモデルに移行することで、LLM は **Tool Call** を生成し始めます。OpenTelemetry の計装はこれらのインタラクションをキャプチャし、LLM の思考プロセスとツールの使用状況を確認でき、各エージェントが Splunk Observability Cloud に表示されるようになります。

## 直接呼び出しとエージェントトレースの比較

これらの変更を行う前に、LLM を直接呼び出した場合とエージェント経由で呼び出した場合のトレースのキャプチャ方法をより深く理解しましょう。

**直接呼び出しのトレース:**

`llm.invoke()` を呼び出すと、計装は標準的な "Chat" または "Completion" スパンを認識します。プロンプトとレスポンスを記録します。エージェントフレームワークによって管理される "ループ" や "ツール呼び出し" ロジックがないため、Splunk Observability Cloud はスパンを "Agent" として分類するために必要なメタデータを認識しません。

**エージェントトレース:**

エージェント（例: `create_react_agent`）を使用すると、フレームワークは実行を特定の "Agent" と "Tool" スパンでラップします。これらのスパンには、OpenTelemetry に対して「これは単なるチャットではなく、特定のツールを持つ推論ループです」と伝えるメタデータが含まれています。これが、トレース可視化において Agents ページと Agent Flow ダイアグラムにデータを表示する仕組みです。

## ツールの追加

まず、`main.py` ファイルの先頭付近に以下の import 文を追加します:

```python
from langchain_core.tools import tool
```

次に、ツール定義を追加します:

```python
@tool
def mock_search_flights(origin: str, destination: str, departure: str) -> str:
    """Return mock flight options for a given origin/destination pair."""
    # create a local random.Random instance
    seed = hash((origin, destination, departure)) % (2**32)
    rng = random.Random(seed)
    airline = rng.choice(["SkyLine", "AeroJet", "CloudNine"])
    fare = rng.randint(700, 1250)

    return (
        f"Top choice: {airline} non-stop service {origin}->{destination}, "
        f"depart {departure} 09:15, arrive {departure} 17:05. "
        f"Premium economy fare ${fare} return."
    )


@tool
def mock_search_hotels(destination: str, check_in: str, check_out: str) -> str:
    """Return mock hotel recommendation for the stay."""
    seed = hash((destination, check_in, check_out)) % (2**32)
    rng = random.Random(seed)
    name = rng.choice(["Grand Meridian", "Hotel Lumière", "The Atlas"])
    rate = rng.randint(240, 410)

    return (
        f"{name} near the historic centre. Boutique suites, rooftop bar, "
        f"average nightly rate ${rate} including breakfast."
    )


@tool
def mock_search_activities(destination: str) -> str:
    """Return a short list of signature activities for the destination."""
    data = DESTINATIONS.get(destination.lower(), DESTINATIONS["paris"])
    bullets = "\n".join(f"- {item}" for item in data["highlights"])
    return f"Signature experiences in {destination.title()}:\n{bullets}"
```

## AI Agent Monitoring 用にアプリケーションを設定する

現在、アプリケーションは以下のように LLM を作成して呼び出しています:

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    ...
    result = llm.invoke(messages)
    ...
```

AI Agent Monitoring のためには、エージェント名を含むメタデータを持つエージェントを作成し、LLM ではなくエージェントを呼び出す必要があります。

まず、`main.py` ファイルの先頭付近に以下の import を追加します:

```python
from langchain.agents import (
create_agent as _create_react_agent,  # type: ignore[attr-defined]
)
```

次に、`coordinator_node`、`flight_specialist_node`、`hotel_specialist_node`、`activity_specialist_node`、`plan_synthesizer_node` 関数の定義を以下のように置き換えます:

> ヒント: `vi` エディタで大量の行を一括削除するには、`Shift` + `v` を押して `Visual Line` モードにし、下矢印キーで削除したい行をすべて選択し、`d` を押して選択した行を削除します。

```python
def coordinator_node(
    state: PlannerState
) -> PlannerState:
    llm = _create_llm("coordinator", temperature=0.2, session_id=state["session_id"])
    agent = _create_react_agent(llm, tools=[]).with_config(
        {
            "run_name": "coordinator",
            "tags": ["agent", "agent:coordinator"],
            "metadata": {
                "agent_name": "coordinator",
                "session_id": state["session_id"],
            },
        }
    )
    system_message = SystemMessage(
        content=(
            "You are the lead travel coordinator. Extract the key details from the "
            "traveller's request and describe the plan for the specialist agents."
        )
    )

    result = agent.invoke({"messages": [system_message] + list(state["messages"])})
    final_message = result["messages"][-1]
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "flight_specialist"
    return state


def flight_specialist_node(
    state: PlannerState
) -> PlannerState:
    llm = _create_llm(
        "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    agent = _create_react_agent(llm, tools=[mock_search_flights]).with_config(
        {
            "run_name": "flight_specialist",
            "tags": ["agent", "agent:flight_specialist"],
            "metadata": {
                "agent_name": "flight_specialist",
                "session_id": state["session_id"],
            },
        }
    )
    step = (
        f"Find an appealing flight from {state['origin']} to {state['destination']} "
        f"departing {state['departure']} for {state['travellers']} travellers."
    )

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a flight booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = agent.invoke({"messages": messages})
    final_message = result["messages"][-1]
    state["flight_summary"] = final_message.content if isinstance(final_message, BaseMessage) else str(final_message)
    state["messages"].append(final_message if isinstance(final_message, BaseMessage) else AIMessage(content=str(final_message)))
    state["current_agent"] = "hotel_specialist"
    return state


def hotel_specialist_node(
    state: PlannerState
) -> PlannerState:
    llm = _create_llm(
        "hotel_specialist", temperature=0.5, session_id=state["session_id"]
    )
    agent = _create_react_agent(llm, tools=[mock_search_hotels]).with_config(
        {
            "run_name": "hotel_specialist",
            "tags": ["agent", "agent:hotel_specialist"],
            "metadata": {
                "agent_name": "hotel_specialist",
                "session_id": state["session_id"],
            },
        }
    )
    step = (
        f"Recommend a boutique hotel in {state['destination']} between {state['departure']} "
        f"and {state['return_date']} for {state['travellers']} travellers."
    )

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a hotel booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = agent.invoke({"messages": messages})

    final_message = result["messages"][-1]
    state["hotel_summary"] = (
        final_message.content
        if isinstance(final_message, BaseMessage)
        else str(final_message)
    )
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "activity_specialist"
    return state


def activity_specialist_node(
    state: PlannerState
) -> PlannerState:
    llm = _create_llm(
        "activity_specialist", temperature=0.6, session_id=state["session_id"]
    )
    agent = _create_react_agent(llm, tools=[mock_search_activities]).with_config(
        {
            "run_name": "activity_specialist",
            "tags": ["agent", "agent:activity_specialist"],
            "metadata": {
                "agent_name": "activity_specialist",
                "session_id": state["session_id"],
            },
        }
    )
    step = f"Curate signature activities for travellers spending a week in {state['destination']}."

    # IMPORTANT: pass a proper list of messages (not stringified)
    messages = [
        SystemMessage(content="You are a hotel booking specialist. Provide concise options."),
        HumanMessage(content=step),
    ]

    result = agent.invoke({"messages": messages})

    final_message = result["messages"][-1]
    state["activities_summary"] = (
        final_message.content
        if isinstance(final_message, BaseMessage)
        else str(final_message)
    )
    state["messages"].append(
        final_message
        if isinstance(final_message, BaseMessage)
        else AIMessage(content=str(final_message))
    )
    state["current_agent"] = "plan_synthesizer"
    return state
    
def plan_synthesizer_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
        "plan_synthesizer", temperature=0.3, session_id=state["session_id"]
    )

    agent = _create_react_agent(llm, tools=[]).with_config(
        {
            "run_name": "plan_synthesizer",
            "tags": ["agent", "agent:plan_synthesizer"],
            "metadata": {
                "agent_name": "plan_synthesizer",
                "session_id": state["session_id"],
            },
        }
    )

    system_content = (
        "You are the travel plan synthesiser. Combine the specialist insights into a "
        "concise, structured itinerary covering flights, accommodation and activities."
    )

    content = json.dumps(
        {
            "flight": state["flight_summary"],
            "hotel": state["hotel_summary"],
            "activities": state["activities_summary"],
        },
        indent=2,
    )

    out = agent.invoke(
        {
            "messages": [
                SystemMessage(content=system_content),
                HumanMessage(
                    content=(
                        f"Traveller request: {state['user_request']}\n\n"
                        f"Origin: {state['origin']} | Destination: {state['destination']}\n"
                        f"Dates: {state['departure']} to {state['return_date']}\n\n"
                        f"Specialist summaries:\n{content}"
                    )
                ),
            ]
        }
    )
    # 1) Extract the assistant's final text
    final_msg = next(m for m in reversed(out["messages"]) if isinstance(m, AIMessage))
    state["final_itinerary"] = final_msg.content

    # 2) Append the new messages to your ongoing conversation
    state["messages"].extend(out["messages"])  # or append just final_msg

    state["current_agent"] = "completed"
    return state
```

> フライト、ホテル、アクティビティのスペシャリストエージェントを作成する際にツールを渡していることに注目してください。エージェントが呼び出されると、LLM がリクエストを満たすためにツールを呼び出すべきかどうかを判断します。

## 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします:

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-agents-and-tools .
docker push localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

### Kubernetes マニフェストの更新

OpenTelemetry の計装、特に AI Agent Monitoring では、計装データの収集、処理、エクスポート方法を定義する多数の環境変数を設定する必要があります。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、エージェントとツールを含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

### 更新されたアプリケーションのデプロイ

マニフェストファイルを使用して、以下のように更新されたアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

新しいアプリケーション Pod が正常に起動し、古い Pod がなくなっていることを確認します。

次に、以下のコマンドを実行してアプリケーションをテストします:

``` bash
curl http://travel-planner.localhost/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```

## Splunk Observability Cloud でデータを確認する

Splunk Observability Cloud に戻って、トレースがどのように表示されるか確認しましょう。

`APM` に移動し、`AI agents` を選択します。環境名（例: `agentic-ai-$INSTANCE`）が選択されていることを確認します。ページにデータが表示されるようになりました！

![Agents](../images/Agents-v2.png)

`APM -> AI trace data` に移動します。これは AI 関連のコンテンツを含むトレースを検索できる新しいページです:

![Agents](../images/AI-trace-data.png)

環境名（例: `agentic-ai-$INSTANCE`）が選択されていることを確認します。新しいトレースの 1 つを選択します。すべてのエージェントが Agent flow に表示されるようになりました！

![Trace](../images/Trace-v2.png)

Tool Call も確認できます:

![Trace](../images/TraceWithToolCalls.png)
