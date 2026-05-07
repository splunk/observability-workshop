---
title: 品質問題の検出
linkTitle: 9. 品質問題の検出
weight: 9
time: 15 minutes
---

> 注意: このセクションでは複数のファイルを変更する必要があります。
> 変更箇所がわからない場合やアプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-quality-issue` フォルダにある
> モデルソリューションを参照してください。

前のセクションでは、アプリケーションを OpenTelemetry で計装し、
エージェントの応答のセマンティック品質を評価するように設定しました。

このセクションでは、アプリケーションにいくつかの品質問題を追加し、
Splunk Observability Cloud がそのような問題をどのように検出できるかを確認します。

## Poisoned Chat Wrapper について

このセクションでは、既存の `ChatModel` をラップして出力をインターセプトし「汚染」する `PoisonedChatWrapper` というカスタムクラスを使用します。このアプローチを採用したのは、OpenTelemetry 計装でキャプチャされる前に出力をインターセプトできるようにするためです。

この仕組みに興味がある場合は、`poison_chat_wrapper.py` ファイルを確認してください。

## Hotel Specialist の出力を汚染する

次に、hotel specialist エージェントがこのラッパーを使用して LLM の出力を変更するように修正します。まず、`~/workshop/agentic-ai/base-app/main.py` ファイルを編集し、`Begin: Add Import Statements` と `End: Add Import Statements` の間に以下の import 文を追加します:

```python
from poison_chat_wrapper import PoisonedChatWrapper
```

次に、`hotel_specialist_node` 関数の定義を以下に置き換えます:

> ヒント: `vi` エディタで大量の行を一括削除するには、`Shift` + `v` を押して `Visual
> Line` モードに入り、下矢印キーで削除したい行をすべて選択してから、`d`
> を押して選択した行を削除します。

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

> ヒント: 以下のコマンドを実行して、変更内容をモデルソリューションと比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-quality-issue/main.py`

## 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-quality-issue .
docker push localhost:9999/agentic-ai-app:app-with-quality-issue
```

### Kubernetes マニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、品質問題を含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-quality-issue
```

### 更新されたアプリケーションのデプロイ

以下のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

新しいアプリケーション Pod が正常に起動し、古い Pod が存在しないことを確認します:

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

## Splunk Observability Cloud でデータを確認する

Splunk Observability Cloud に戻り、トレースがどのように表示されるかを確認しましょう。

`hotel_specialist` エージェントの `invoke_agent` スパンを見ると、エージェントがホテルを推薦した後に `pretty terrible` と呼んでいることから、いくつかの品質問題があることがわかります:

![Trace With Quality Issue](../images/TraceWithQualityIssue.png)

> 注意: すべてのエージェント呼び出しが評価されるわけではありません。ワークショップの組織では 20% の確率でのみ評価するように設定されています。これは組織レベルで設定可能です。`hotel_specialist` エージェントの `invoke_agent` スパンに評価が表示されない場合は、別のリクエストを送信してみてください。
