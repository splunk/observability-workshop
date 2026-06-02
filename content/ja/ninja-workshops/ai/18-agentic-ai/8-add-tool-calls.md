---
title: Add Tool Calls
linkTitle: 8. Add Tool Calls
weight: 8
time: 15 minutes
---

> 注意: ワークショップのこのセクションでは、複数のファイルを変更する必要があります。
> どこを変更すればよいかわからない場合や、アプリケーションが
> 動作しなくなった場合は、このセクションのモデルソリューションを参照してください。
> モデルソリューションは `~/workshop/agentic-ai/app-with-agents-and-tools` フォルダにあります。

前のセクションでは、エージェントが新しい **Agents** ページにも、
トレース上部の **Agent flow** にも表示されないことがわかりました。

その理由は、現在のアプリケーションがエージェントを使用しておらず、代わりに
LLM を直接呼び出しているためです。

つまり、現時点では、私たちのアプリは台本通りの劇のようなものです。すべてのセリフとすべての動作は
コード内に書かれています。LLM を呼び出すときは、特定のセリフを読むようにお願いしているだけです。
LLM が選択を行わないため、Observability for AI のインストルメンテーションは
LLM を自律的なエージェントとして認識しません。

次のセクションでは、LLM に **tools** と、それらをどのように使用するかを
決定する権限を与えます。エージェント型モデルに移行することで、LLM は
**Tool Calls** を生成し始めます。OpenTelemetry インストルメンテーションがこれらの
やり取りをキャプチャすることで、LLM の思考プロセスとツールの使用状況を確認でき、
各エージェントが Splunk Observability Cloud で表現されるようになります。

## Direct Invocation vs. Agentic Traces

これらの変更を行う前に、LLM を直接呼び出す場合とエージェント経由で呼び出す場合とで、
トレースがどのようにキャプチャされるかをもう少し詳しく見てみましょう。

**直接呼び出しのトレース:**

`llm.invoke()` を呼び出すと、インストルメンテーションは標準的な「Chat」または「Completion」スパンを認識します。
プロンプトとレスポンスを記録します。エージェントフレームワークによって管理される
「ループ」や「ツール呼び出し」のロジックが存在しないため、Splunk Observability Cloud は
そのスパンを「エージェント」として分類するために必要なメタデータを認識しません。

**エージェント型のトレース:**

エージェント（例: `create_react_agent`）を使用すると、
フレームワークは実行を特定の「Agent」スパンと「Tool」スパンでラップします。これらの
スパンには、OpenTelemetry に「これは単なるチャットではなく、特定のツールを使用した
推論ループである」と伝えるメタデータが含まれています。これによって、
Agents ページとトレース可視化の Agent Flow 図が表示されるようになります。

## Make a Backup

Python コードを変更する前に、次のコマンドを使用して `main.py` ファイルの
バックアップを作成してください:

```bash
cp ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/base-app/main.py.bak
```

## Add Import Statements

`~/workshop/agentic-ai/base-app/main.py` ファイルを開いて編集します。

`Begin: Add Import Statements` と `End: Add Import Statements` と書かれた行の間に、
次の import 文を追加してください:

```python
# Begin: Add Import Statements

from langchain_core.tools import tool
from langchain.agents import (
    create_agent as _create_react_agent,  # type: ignore[attr-defined]
)

# End: Add Import Statements
```

## Add Tools

同じ `main.py` ファイル内で、`Begin: Tool Definitions` と `End: Tool Definitions` と
書かれた行の間に、ツール定義を追加してください:

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

## Configure the Application for AI Agent Monitoring

現在、私たちのアプリケーションは LLM を作成し、次のように呼び出しています:

```python
def flight_specialist_node(state: PlannerState) -> PlannerState:
    llm = _create_llm(
    "flight_specialist", temperature=0.4, session_id=state["session_id"]
    )
    ...
    result = llm.invoke(messages)
    ...
```

AI Agent Monitoring のためには、代わりにエージェント名を含むメタデータを伴うエージェントを作成し、
LLM ではなくエージェントを呼び出す必要があります。

{{% notice title="LangChain Agents" style="green" icon="running" %}}

次のステップでは、アプリケーションに **agents** を追加します。しかし、LangChain の文脈において
エージェントとは正確に何でしょうか？

[LangChain ドキュメント](https://docs.langchain.com/oss/python/langchain/agents) によると:

「エージェントは、言語モデルとツールを組み合わせて、タスクについて推論し、
どのツールを使用するかを決定し、解決策に向けて反復的に
作業できるシステムを作成します。」

実際のところ、これはモデルがテキストの生成だけに限定されないことを意味します。代わりに、
利用可能な **tools**（API、データベース、コード実行など）の中から選択して
タスクを完了させることができます。

このスタイルのエージェントは、しばしば **LangChain ReAct agent** と呼ばれます。

ReAct は **Reasoning + Acting** の略です。エージェントは次のループで動作します:

* タスクについて簡単に推論する、
* 関連するツールを選択して呼び出す、
* 結果を観察する、
* 新しい情報を使用して次のステップを決定する。

このプロセスは、エージェントが最終的な回答を生成するのに十分な情報を集めるまで繰り返されます。

{{% /notice %}}

`coordinator_node`、`flight_specialist_node`、`hotel_specialist_node`、
`activity_specialist_node`、`plan_synthesizer_node` 関数の定義を以下に置き換えてください:

> ヒント: `vi` エディタで多数の行を一括削除するには、`Shift` + `v` を押して `Visual
> Line` モードに切り替え、下矢印キーを使って削除したい行をすべて選択した後、`d` を押して
> 選択した行を削除します。

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
    # 1) Extract the assistant’s final text
    final_msg = next(m for m in reversed(out["messages"]) if isinstance(m, AIMessage))
    state["final_itinerary"] = final_msg.content

    # 2) Append the new messages to your ongoing conversation
    state["messages"].extend(out["messages"])  # or append just final_msg

    state["current_agent"] = "completed"
    return state
```

flight、hotel、activity の各スペシャリストエージェントを作成する際に、ツールを渡していることに
注意してください。エージェントが呼び出されると、LLM はリクエストを満たすために
ツールを呼び出すべきかどうかを判断します。

{{% notice title="Check your work before proceeding" style="primary" icon="running" %}}

次のコマンドを実行して、変更内容を期待されるソリューションと比較してください:

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-agents-and-tools/main.py
```

{{% / notice %}}

## Build an Updated Docker Image

新しいタグで更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-agents-and-tools .
docker push localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みの
> イメージを使用することを検討してください。そのためには、
> `~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内のイメージ名を `localhost:9999/agentic-ai-app:app-with-agents-and-tools`
> ではなく `ghcr.io/splunk/agentic-ai-app:app-with-agents-and-tools` に更新します。

### Update the Kubernetes Manifest

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、
エージェントとツールを含むイメージを使用するように
イメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-agents-and-tools
```

### Deploy the Updated Application

更新されたアプリケーションは、マニフェストファイルを使用して次のようにデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

新しいアプリケーション Pod が正常に起動し、古い Pod がもう存在しないことを確認してください:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
````

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

## View Data in Splunk Observability Cloud

Splunk Observability Cloud に戻り、トレースが今どのように見えるかを確認してみましょう。

`APM` に移動し、`AI agents` を選択します。環境名（例: `agentic-ai-$INSTANCE`）が
選択されていることを確認してください。ページが表示されるようになっていることに
気付くでしょう！

![Agents](../images/Agents-v2.png)

`APM -> AI trace data` に移動します。これは、AI 関連のコンテンツを含むトレースを
検索できる新しいページです:

![Agents](../images/AI-trace-data.png)

環境名（例: `agentic-ai-$INSTANCE`）が選択されていることを確認してください。
新しいトレースの 1 つを選択します。Agent flow にすべてのエージェントが表示されているのがわかります！

![Trace](../images/Trace-v2.png)

ツール呼び出しも確認できます:

>注意: ツール呼び出しの詳細を表示するには、画面右側で `AI details` から `Span details` に
> 切り替えてください。

![Trace](../images/TraceWithToolCalls.png)
