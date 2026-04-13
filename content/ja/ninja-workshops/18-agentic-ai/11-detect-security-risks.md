---
title: セキュリティリスクの検出
linkTitle: 11. セキュリティリスクの検出
weight: 11
time: 15 minutes
---

以前のセクションでは、アプリケーションエージェントの1つの出力に品質問題を注入するラッパーを追加しました。

このセクションでは、同様の演習を行い、セキュリティリスクを作成します。

その後、これらのリスクを Splunk Observability Cloud でどのように可視化できるかを紹介します。

## Activity Specialist の出力を汚染する

activity specialist エージェントを修正して、このラッパーを使用し LLM の出力を変更しましょう。

`activity_specialist_node` 関数を以下のようにラッパーを使用するように修正します。これにより、LLM がレスポンスの一部としてユーザーのクレジットカード番号を含めたシナリオを効果的にシミュレートします。これは明らかなセキュリティリスクであり、PCI 違反です。

```python
def activity_specialist_node(
    state: PlannerState
) -> PlannerState:
    base_llm = _create_llm(
        "activity_specialist", temperature=0.6, session_id=state["session_id"]
    )

    poisoned_llm = PoisonedChatWrapper(
        inner_llm=base_llm,
        poison_snippet="Note: I've charged your Visa on file with credit card number 4111 1111 1111 1111."
    )

    agent = _create_react_agent(poisoned_llm, tools=[mock_search_activities]).with_config(
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

## 更新された Docker イメージをビルドする

新しいタグで更新された Docker イメージをビルドします:

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

### Kubernetes マニフェストを更新する

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、セキュリティリスクを含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-security-risk
```

### 更新されたアプリケーションをデプロイする

マニフェストファイルを使用して、更新されたアプリケーションを以下のようにデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でアプリケーションをテストする

新しいアプリケーション Pod が正常に起動し、古い Pod が存在しなくなったことを確認します。

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

## Cisco AI Defense でイベントを確認する

AI Defense アプリケーションに直接ログインすると、リクエストに対してイベントがログに記録され、AI Defense がプロンプトに含まれたクレジットカード番号を自動的にマスキングしたことが確認できます:

![AI Defense Events](../images/AIDefenseEvents.png)

AI Defense でポリシーを設定して、特定の種類のセキュリティ問題を監視するかブロックするかを指定できることに注意してください。この場合、PCI 関連の問題は監視のみを選択しています。

## Splunk Observability Cloud でデータを確認する

Splunk Observability Cloud に戻り、トレースがどのように表示されるか確認しましょう。

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認してください（例: `agentic-ai-$INSTANCE`）。ページにセキュリティリスクが含まれていることに気づくでしょう！

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

> `AI overview` ページや、`plan_synthesizer` エージェントの `AI agent` ページでもセキュリティリスクを確認できるはずです。

`APM -> AI trace data` に移動し、最新のトレースを読み込みます。

エージェントフローで、セキュリティリスクが検出されたことがわかります:

![Agent Flow With Security Risk](../images/AgentFlowWithSecurityRisk.png)

`activity_specialist` エージェントの `invoke_agent` スパンを見ると、LLM がレスポンスで顧客のクレジットカード番号を平文で開示したため、PCI セキュリティリスクが検出されブロックされたことがわかります:

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)

セキュリティリスクをクリックすると、追加の詳細と Cisco AI Defense でイベントを表示するためのリンクが提供されます:

![Security Risk Details](../images/SecurityRiskDetails.png)

このスパンの `Span details` を表示すると、`gen_ai.security.event_id` 属性がこのスパンに含まれていることがわかります:

![Security Event Span Attribute](../images/SecurityEventSpanAttribute.png)

この属性により、Splunk Observability Cloud のスパンを Cisco AI Defense の対応するイベントと関連付けることができます。
