---
title: Detect Quality Issue
linkTitle: 9. Detect Quality Issue
weight: 9
time: 15 minutes
---

> 注意: このワークショップのセクションでは、複数のファイルを変更する必要があります。
> 変更箇所が分からない場合や、アプリケーションが動作しなくなった場合は、
> このセクションのモデルソリューションを `~/workshop/agentic-ai/app-with-quality-issue` フォルダーで参照してください。

これまでのセクションでは、アプリケーションを OpenTelemetry で計装し、
エージェント応答の意味的な品質を評価するように構成しました。

このセクションでは、アプリケーションにいくつかの品質問題を追加し、
Splunk Observability Cloud がこれらの問題をどのように検出できるかを確認しましょう。

## About the Poisoned Chat Wrapper

このセクションでは、既存の `ChatModel` をラップして出力を傍受し「ポイズン」する、
`PoisonedChatWrapper` というカスタムクラスを使用します。このアプローチを採用したのは、
OpenTelemetry の計装で出力がキャプチャされる前に、出力を傍受できるようにするためです。

このしくみについて詳しく知りたい場合は、`poison_chat_wrapper.py` ファイルを確認してください。

## Poison the Hotel Specialist Output

次に、hotel specialist エージェントを変更して、このラッパーを使用し、LLM の出力を改変します。
まず、`~/workshop/agentic-ai/base-app/main.py` ファイルを変更し、
`Begin: Add Import Statements` と `End: Add Import Statements` の行の間に、
以下の import 文を追加します。

```python
from poison_chat_wrapper import PoisonedChatWrapper
```

> 注意: この新しい import 文は、これまでに追加した他の import 文に加えて追加します。

次に、`hotel_specialist_node` 関数の定義を以下の内容で置き換えます。

> ヒント: `vi` エディターで一括して大量の行を削除するには、`Shift` + `v` を押して `Visual Line` モードに入り、
> 下矢印キーで削除したい行をすべて選択してから、`d` を押して選択した行を削除します。

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

{{% notice title="Check your work before proceeding" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を期待されるソリューションと比較します。

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-quality-issue/main.py
```

{{% / notice %}}

## Build an Updated Docker Image

新しいタグで更新された Docker イメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-quality-issue .
docker push localhost:9999/agentic-ai-app:app-with-quality-issue
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みイメージを使用することを検討してください。
> その場合、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内のイメージ名を、
> `localhost:9999/agentic-ai-app:app-with-quality-issue` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-quality-issue` に更新してください。

### Update the Kubernetes Manifest

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、
品質問題のあるイメージを使用するように、イメージを更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-quality-issue
```

### Deploy the Updated Application

以下のように、マニフェストファイルを使用して、更新されたアプリケーションをデプロイできます。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Test the Application in Kubernetes

新しいアプリケーションの Pod が正常に起動し、古い Pod がもう存在しないことを確認します。

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

次に、以下のコマンドを実行してアプリケーションをテストします。

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

Splunk Observability Cloud に戻り、トレースが現在どのように見えるかを確認しましょう。

`hotel_specialist` エージェントの `invoke_agent` スパンを見ると、
このエージェントにはいくつかの品質問題があることが分かります。ホテルを推奨したうえで、
それを `pretty terrible` と呼んでいるからです。

![Trace With Quality Issue](../images/TraceWithQualityIssue.png)

> 注意: ワークショップの組織では 20% の頻度でのみ評価するように設定されているため、
> すべてのエージェント呼び出しが評価されるわけではありません。これは組織レベルで構成可能です。
> `hotel_specialist` エージェントの `invoke_agent` スパンに評価が表示されない場合は、
> もう一度リクエストを送信してみてください。
