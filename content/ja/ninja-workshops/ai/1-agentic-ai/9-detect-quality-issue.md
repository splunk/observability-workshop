---
title: 品質問題の検出
linkTitle: 9. 品質問題の検出
weight: 9
time: 15 minutes
---

> [!NOTE]
> このセクションでは複数のファイルを変更する必要があります。
> 変更箇所が分からない場合やアプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-quality-issue` フォルダにある
> このセクションのモデルソリューションを参照してください。

前のセクションでは、アプリケーションにOpenTelemetryを計装し、エージェントの応答のセマンティック品質を評価するように設定しました。

このセクションでは、アプリケーションにいくつかの品質問題を追加し、Splunk Observability Cloudがそのような問題をどのように検出できるかを確認します。

## Poisoned Chat Wrapperについて

このセクションでは、既存の `ChatModel` をラップして出力をインターセプトし「汚染」する `PoisonedChatWrapper` というカスタムクラスを使用します。このアプローチを採用したのは、OpenTelemetry計装でキャプチャされる前に出力をインターセプトできるようにするためです。

この仕組みに興味がある場合は、`poison_chat_wrapper.py` ファイルを確認してください。

## Hotel Specialistの出力を汚染する

次に、hotel specialistエージェントを変更して、このラッパーを使用しLLM出力を変更します。まず、`~/workshop/agentic-ai/base-app/main.py` ファイルを編集し、`Begin: Add Import Statements` と `End: Add Import Statements` の間に以下のimport文を追加します。

```python
from poison_chat_wrapper import PoisonedChatWrapper
```

> [!NOTE]
> この新しいimport文は、以前に追加した他のimport文に加えて追加するものです。

次に、`hotel_specialist_node` 関数の定義を以下に置き換えます。

> [!TIP]
> `vi` エディタで大量の行を一括削除するには、`Shift` + `v` を押して `Visual
> Line` モードにし、下矢印キーで削除したい行をすべて選択してから、`d`
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

{{% notice title="先に進む前に作業を確認してください" style="primary" icon="running" %}}

以下のコマンドを実行して、変更内容を期待されるソリューションと比較します。

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-quality-issue/main.py
```

{{% / notice %}}

## 更新されたDockerイメージのビルド

新しいタグで更新されたDockerイメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-quality-issue .
docker push localhost:9999/agentic-ai-app:app-with-quality-issue
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、事前にビルドされたイメージの使用を検討してください。
> その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内のイメージ名を
> `localhost:9999/agentic-ai-app:app-with-quality-issue` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-quality-issue` に変更します。

### Kubernetesマニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを開いて編集し、品質問題のあるイメージを使用するようにイメージを更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-quality-issue
```

### 更新されたアプリケーションのデプロイ

マニフェストファイルを使用して、更新されたアプリケーションを以下のようにデプロイします。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでのアプリケーションテスト

新しいアプリケーションPodが正常に起動し、古いPodが存在しないことを確認します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
```

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

## Splunk Observability Cloudでデータを確認する

Splunk Observability Cloudに戻り、トレースがどのように表示されるかを確認しましょう。

`hotel_specialist` エージェントの `invoke_agent` Spanを見ると、エージェントがホテルを推薦した後に `pretty terrible` と呼んでいるため、いくつかの品質問題があることが分かります。

![Trace With Quality Issue](../images/TraceWithQualityIssue.png)

> [!NOTE]
> すべてのエージェント呼び出しが評価されるわけではありません。ワークショップ組織では20%の確率でのみ
> 評価するように設定されています。これは組織レベルで設定可能です。`hotel_specialist` エージェントの
> `invoke_agent` Spanに評価が表示されない場合は、別のリクエストを送信してみてください。
