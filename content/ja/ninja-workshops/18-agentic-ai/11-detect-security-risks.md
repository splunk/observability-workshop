---
title: セキュリティリスクの検出
linkTitle: 11. セキュリティリスクの検出
weight: 11
time: 15分
---

> 注：このセクションのワークショップでは、複数のファイルを変更する必要があります。
> 変更箇所がわからない場合やアプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-security-risk` フォルダにあるこのセクションの
> モデルソリューションを参照してください。

前のセクションでは、アプリケーションエージェントの1つの出力に品質問題を注入するラッパーを追加しました。

このセクションでは、同様の手順でセキュリティリスクを作成します。

そして、これらのリスクがSplunk Observability Cloudでどのように表示されるかを紹介します。

## Activity Specialist の出力を汚染する

activity specialistエージェントを修正してこのラッパーを使用し、LLMの出力を変更しましょう。

`~/workshop/agentic-ai/base-app/main.py` ファイルを編集用に開きます。

`activity_specialist_node` 関数を以下のようにラッパーを使用するように修正します。これは、LLMがレスポンスの一部としてユーザーのクレジットカード番号を含めるシナリオを効果的にシミュレートするもので、明確なセキュリティリスクおよびPCI違反です。

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

> ヒント：以下のコマンドを実行して、変更内容をモデルソリューションと比較できます
>
> `diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-security-risk/main.py`

## 更新されたDockerイメージをビルドする

新しいタグで更新されたDockerイメージをビルドします

``` bash
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

### Kubernetesマニフェストを更新する

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、セキュリティリスクを含むイメージを使用するようにイメージを更新します

```yaml
          image: localhost:9999/agentic-ai-app:app-with-security-risk
```

### 更新されたアプリケーションをデプロイする

以下のようにマニフェストファイルを使用して更新されたアプリケーションをデプロイできます

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでアプリケーションをテストする

新しいアプリケーションPodが正常に起動し、古いPodがなくなっていることを確認します

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

## Cisco AI Defenseでイベントを確認する

AI Defenseアプリケーションに直接ログインすると、リクエストに対してイベントが記録され、AI Defenseがプロンプトに含まれたクレジットカード番号を自動的にマスキングしたことが確認できます

![AI Defense Events](../images/AIDefenseEvents.png)

AI Defenseではポリシーを設定して、特定の種類のセキュリティ問題を監視するかブロックするかを指定できます。この場合、PCI関連の問題を監視するのみに設定しています。

## Splunk Observability Cloudでデータを確認する

Splunk Observability Cloudに戻って、トレースがどのように表示されるか確認しましょう。

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認してください（例`agentic-ai-$INSTANCE`）。ページにセキュリティリスクが表示されるようになっていることがわかります。

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

> `AI overview` ページや `plan_synthesizer` エージェントの `AI agent` ページでもセキュリティリスクが表示されるはずです。

`APM -> AI trace data` に移動し、最新のトレースを読み込みます。

エージェントフローで、セキュリティリスクが検出されたことが確認できます

![Agent Flow With Security Risk](../images/AgentFlowWithSecurityRisk.png)

`activity_specialist` エージェントの `invoke_agent` スパンを見ると、LLMがレスポンスにお客様のクレジットカード番号を平文で含めたため、PCIセキュリティリスクが検出されブロックされたことがわかります

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)

セキュリティリスクをクリックすると、追加の詳細情報と、Cisco AI Defenseでイベントを表示するためのリンクが表示されます

![Security Risk Details](../images/SecurityRiskDetails.png)

また、このスパンの `Span details` を表示すると、`gen_ai.security.event_id` 属性がこのスパンに含まれていることが確認できます

![Security Event Span Attribute](../images/SecurityEventSpanAttribute.png)

この属性により、Splunk Observability Cloudのスパンと、Cisco AI Defenseの対応するイベントを関連付けることができます。
