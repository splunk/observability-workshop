---
title: Tool Call の追加
linkTitle: 8. Add Tool Calls
weight: 8
time: 15 minutes
---

> [!NOTE]
> このセクションでは、複数のファイルを変更する必要があります。
> どこを変更すればよいかわからない場合や、アプリケーションが
> 動作しなくなった場合は、このセクションのモデルソリューション
> （`~/workshop/agentic-ai/app-with-agents-and-tools` フォルダ内）を参照してください。

前のセクションでは、エージェントが新しい **Agents** ページやトレース上部の **Agent flow** に
表示されないことを確認しました。

その理由は、アプリケーションが現在エージェントを使用しておらず、LLM を直接呼び出しているためです。

つまり、現在のアプリは台本のある演劇のようなものです。すべてのセリフとアクションがコードに
書かれています。LLM を呼び出す際、特定のセリフを読み上げるよう指示しているだけです。
LLM が自ら判断を行っていないため、Observability for AI の計装はこれを自律的なエージェントとして
認識しません。

次のセクションでは、LLM に**ツール**とそれを使用する権限を与えます。
エージェントモデルに移行することで、LLM は **Tool Call** を生成するようになります。
OpenTelemetry の計装がこれらのインタラクションをキャプチャし、LLM の思考プロセスと
ツールの使用状況を確認できるようになり、各エージェントが Splunk Observability Cloud 上で
表示されるようになります。

## 直接呼び出しとエージェントトレースの比較

これらの変更を行う前に、LLM を直接呼び出した場合とエージェント経由で呼び出した場合で、
トレースがどのようにキャプチャされるかを詳しく見てみましょう。

**直接呼び出しのトレース:**

`llm.invoke()` を呼び出すと、計装は標準的な「Chat」または「Completion」スパンを検出します。
プロンプトとレスポンスが記録されます。エージェントフレームワークによって管理される
「ループ」や「ツール呼び出し」のロジックがないため、Splunk Observability Cloud はスパンを
「Agent」として分類するために必要なメタデータを検出できません。

**エージェントトレース:**

エージェント（例: `create_react_agent`）を使用すると、
フレームワークは実行を特定の「Agent」および「Tool」スパンでラップします。
これらのスパンには、OpenTelemetry に「これは単なるチャットではなく、
特定のツールを持つ推論ループです」と伝えるメタデータが含まれています。
これが Agents ページとトレース可視化の Agent Flow ダイアグラムに
データを表示する仕組みです。

## バックアップの作成

Python コードを変更する前に、以下のコマンドで `main.py` ファイルのバックアップを作成します:

```bash
cp ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/base-app/main.py.bak
```

## Import 文の追加

`~/workshop/agentic-ai/base-app/main.py` ファイルを開いて編集します。

`Begin: Add Import Statements` と `End: Add Import Statements` の間に
以下の import 文を追加します:

```python
# Begin: Add Import Statements

from langchain_core.tools import tool
from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)

# End: Add Import Statements
```

## ツールの追加

同じ `main.py` ファイルで、`Begin: Tool Definitions` と `End: Tool Definitions` の間に
ツール定義を追加します:

```python
# Begin: Tool Definitions

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
    
# End: Tool Definitions
```

## AI Agent Monitoring 用にアプリケーションを設定する

現在、アプリケーションは LLM を作成して以下のように呼び出しています:

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    ...
    result = llm.invoke(messages)
    ...
```

AI Agent Monitoring では、エージェント名のメタデータを含むエージェントを作成し、
LLM ではなくエージェントを呼び出す必要があります。

{{% notice title="LangChain Agents" style="green" icon="running" %}}

次のステップでは、アプリケーションに**エージェント**を追加します。しかし、LangChain における
エージェントとは正確には何でしょうか？

[LangChain のドキュメント](https://docs.langchain.com/oss/python/langchain/agents)によると:

「エージェントは、言語モデルとツールを組み合わせて、タスクについて推論し、
どのツールを使用するかを決定し、反復的に解決策に向かって作業するシステムを作成します。」

実際には、これはモデルがテキスト生成に限定されなくなることを意味します。代わりに、
タスクを完了するために利用可能な**ツール**のセット（API、データベース、コード実行など）から
選択できるようになります。

このスタイルのエージェントは **LangChain ReAct agent** と呼ばれることが多いです。

ReAct は **Reasoning + Acting**（推論 + 行動）の略です。エージェントは以下のループで動作します:

* タスクについて簡潔に推論し、
* 関連するツールを選択して呼び出し、
* 結果を観察し、
* その新しい情報を使って次のステップを決定します。

このプロセスは、エージェントが最終的な回答を生成するのに十分な情報を収集するまで繰り返されます。

{{% /notice %}}

`coordinator_node`、`flight_specialist_node`、`hotel_specialist_node`、`activity_specialist_node`、`plan_synthesizer_node` 関数の定義を以下に置き換えます:

> [!TIP]
> `vi` エディタで大量の行をまとめて削除するには、`Shift` + `v` を押して `Visual
> Line` モードにし、下矢印キーで削除したい行をすべて選択してから、`d`
> を押して選択した行を削除します。

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

フライト、ホテル、アクティビティの各スペシャリストエージェントの作成時にツールを渡していることに
注目してください。エージェントが呼び出されると、LLM はリクエストを満たすためにツールを
呼び出すべきかどうかを判断します。

{{% notice title="次に進む前に作業を確認する" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を期待されるソリューションと比較します:

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-agents-and-tools/main.py
```

{{% / notice %}}

## 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-agents-and-tools .
docker push localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを使用することを
> 検討してください。そのためには、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルの
> イメージ名を `localhost:9999/agentic-ai-app:app-with-agents-and-tools` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-agents-and-tools` に更新します。

### Kubernetes マニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、
エージェントとツールを含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

### 更新されたアプリケーションのデプロイ

マニフェストファイルを使用して、更新されたアプリケーションを以下のようにデプロイします:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションテスト

新しいアプリケーション Pod が正常に起動し、古い Pod がなくなっていることを確認します:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
```

{{% /tab %}}
{{< /tabs >}}

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

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを
確認してください（例: `agentic-ai-$INSTANCE`）。ページにデータが
表示されるようになったことがわかります！

![Agents](../images/Agents-v2.png)

`APM -> AI trace data` に移動します。これは AI 関連のコンテンツを含む
トレースを検索できる新しいページです:

![Agents](../images/AI-trace-data.png)

環境名が選択されていることを確認してください（例: `agentic-ai-$INSTANCE`）。  
新しいトレースの 1 つを選択します。Agent flow にすべてのエージェントが表示されるようになりました！

![Trace](../images/Trace-v2.png)

Tool Call も確認できます:

> [!NOTE]
> Tool Call の詳細を確認するには、画面右側の `AI details` から `Span details` に
> 切り替えてください。

![Trace](../images/TraceWithToolCalls.png)
