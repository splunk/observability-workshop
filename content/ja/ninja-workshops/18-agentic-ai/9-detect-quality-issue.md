---
title: 品質問題の検出
linkTitle: 9. 品質問題の検出
weight: 9
time: 15分
---

前のセクションでは、アプリケーションにOpenTelemetryを実装し、エージェントの応答の意味的な品質を評価するように設定しました。

このセクションでは、アプリケーションに意図的に品質問題を追加し、Splunk Observability Cloudがそのような問題を検出できることを確認します。

## Poisoned Chat Wrapper について

このセクションでは、`PoisonedChatWrapper` というカスタムクラスを使用します。このクラスは既存の `ChatModel` をラップして、出力をインターセプトし「汚染」します。このアプローチを採用したのは、OpenTelemetryの計装でキャプチャされる前に出力をインターセプトできるようにするためです。

この仕組みに興味がある場合は、`poison_chat_wrapper.py` ファイルを確認してください。

## Hotel Specialist の出力を汚染する

次に、hotel specialistエージェントを修正してこのラッパーを使用し、LLMの出力を変更します。まず、`main.py` ファイルを修正してラッパークラスをインポートします

```python
from poison_chat_wrapper import PoisonedChatWrapper
```

次に、`hotel_specialist_node` 関数を以下のように修正してラッパーを使用します

```python
def hotel_specialist_node(
    state: PlannerState
) -> PlannerState:
    base_llm = _create_llm(
        "hotel_specialist", temperature=0.5, session_id=state["session_id"]
    )

    poisoned_llm = PoisonedChatWrapper(
        inner_llm=base_llm,
        poison_snippet="Note: I think this hotel is pretty terrible, best of luck if you stay there!"
    )

    agent = _create_react_agent(poisoned_llm, tools=[mock_search_hotels]).with_config(
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
```

## 更新されたDockerイメージをビルドする

新しいタグで更新されたDockerイメージをビルドします

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-quality-issue .
docker push localhost:9999/agentic-ai-app:app-with-quality-issue
```

### Kubernetesマニフェストを更新する

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、品質問題を含むイメージを使用するようにイメージを更新します

```yaml
          image: localhost:9999/agentic-ai-app:app-with-quality-issue
```

### 更新されたアプリケーションをデプロイする

以下のようにマニフェストファイルを使用して更新されたアプリケーションをデプロイします

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでアプリケーションをテストする

新しいアプリケーションPodが正常に起動し、古いPodがなくなっていることを確認します。

次に、以下のコマンドを実行してアプリケーションをテストします

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

## Splunk Observability Cloudでデータを確認する

Splunk Observability Cloudに戻って、トレースがどのように表示されるか確認しましょう。

`hotel_specialist` エージェントの `invoke_agent` スパンを見ると、エージェントがホテルを推奨した後に `pretty terrible` と呼んでいるため、いくつかの品質問題があることがわかります

![Trace With Quality Issue](../images/TraceWithQualityIssue.png)

> 注：ワークショップの組織は20%の確率でのみ評価するように設定されているため、すべてのエージェント呼び出しが評価されるわけではありません。これは組織レベルで設定可能です。`hotel_specialist` エージェントの `invoke_agent` スパンに評価が表示されない場合は、別のリクエストを送信してみてください。
