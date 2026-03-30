---
title: ツール呼び出しの追加
linkTitle: 8. ツール呼び出しの追加
weight: 8
time: 10 minutes
---

前のセクションでは、エージェントが新しい **Agents** ページやトレース上部の **Agent flow** に表示されていないことを確認しました。

その理由は、現在のアプリケーションがエージェントを使用しておらず、代わりにLLMを直接呼び出しているからです。

このセクションでは、まずエージェントが使用できるツールを追加し、その後、各ノードのコードを更新してLLMを直接使用するのではなくエージェントを作成して利用するようにします。

また、各エージェントがツールを使用するように設定します。

## ツールの追加

まず、`main.py` ファイルの先頭付近に以下のimport文を追加します：

```python
from langchain_core.tools import tool
```

次に、ツールの定義を追加します：

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

## AI Agent Monitoring 用のアプリケーション設定

現在、アプリケーションは以下のようにLLMを作成して呼び出しています：

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    ...
    result = llm.invoke(messages)
    ...
```

AI Agent Monitoringのためには、代わりにエージェント名を含むメタデータを持つエージェントを作成し、LLMではなくエージェントを呼び出す必要があります。

まず、`main.py` ファイルの先頭付近に以下のimportを追加します：

```python
from langchain.agents import (
create_agent as _create_react_agent,  # type: ignore[attr-defined]
)
```

次に、`coordinator_node`、`flight_specialist_node`、`hotel_specialist_node`、`activity_specialist_node` 関数の定義を以下のように置き換えます：

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
```

> フライト、ホテル、アクティビティの各スペシャリストエージェントを作成する際にツールを渡していることに注目してください。エージェントが呼び出されると、LLM はリクエストを実行するためにツールを呼び出すべきかどうかを判断します。

## 更新された Docker イメージのビルド

新しいタグで更新されたDockerイメージをビルドします：

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-agents-and-tools .
docker push localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

### Kubernetes マニフェストの更新

OpenTelemetryのインストルメンテーション、特にAI Agent Monitoringでは、インストルメンテーションデータの収集、処理、エクスポート方法を定義するいくつかの環境変数を設定する必要があります。

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、エージェントとツールを含むイメージを使用するようにイメージを更新します：

```yaml
          image: localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して更新されたアプリケーションをデプロイできます：

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

以下のコマンドを実行してアプリケーションをテストします：

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

## Splunk Observability Cloud でのデータ確認

Splunk Observability Cloudに戻って、トレースがどのように表示されるか確認しましょう。

`APM` に移動し、`Agents` を選択します。環境名が選択されていることを確認してください（例：`agentic-ai-$INSTANCE`）。ページにデータが表示されるようになりました！

![Agents](../images/Agents-v2.png)

`APM -> Trace Analyzer` に移動します。

環境名が選択されていることを確認してください（例：`agentic-ai-$INSTANCE`）。新しいトレースの1つを選択します。すべてのエージェントがAgent flowに表示されるようになりました！

![Trace](../images/Trace-v2.png)

ツール呼び出しも確認できます：

![Trace](../images/TraceWithToolCalls.png)
