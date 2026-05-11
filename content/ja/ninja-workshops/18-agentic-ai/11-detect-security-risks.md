---
title: セキュリティリスクの検出
linkTitle: 11. Detect Security Risks
weight: 11
time: 15 minutes
---

> 注意: このワークショップのセクションでは、複数のファイルを変更する必要があります。
> どこを変更すべきか分からない場合や、アプリケーションが正常に
> 動作しなくなった場合は、`~/workshop/agentic-ai/app-with-security-risk` フォルダにある
> このセクションの模範解答を参照してください。

前のセクションでは、アプリケーションエージェントの1つの出力に品質問題を注入するラッパーを追加しました。

このセクションでは、同様の手順でセキュリティリスクを作成します。

その後、これらのリスクが Splunk Observability Cloud でどのように表示されるかを紹介します。

## Activity Specialist の出力を汚染する

Activity Specialist エージェントがこのラッパーを使用して LLM の出力を変更するように修正しましょう。

`~/workshop/agentic-ai/base-app/main.py` ファイルを編集用に開きます。

`activity_specialist_node` 関数の定義を以下のバージョンに置き換えます。
これは、LLM がレスポンスの一部としてユーザーのクレジットカード番号を
含めてしまうシナリオを効果的にシミュレートするもので、明らかなセキュリティリスクおよび PCI 違反です。

> ヒント: `vi` エディタで大量の行を一括削除するには、`Shift` + `v` を押して `Visual
> Line` モードにし、下矢印キーで削除したい行をすべて選択してから、`d`
> を押して選択した行を削除します。

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

> ヒント: 以下のコマンドを実行して、変更内容を模範解答と比較できます:
>
> `diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-security-risk/main.py`

## 更新された Docker イメージのビルド

新しいタグで更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みの
> イメージの使用を検討してください。その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルの
> イメージ名を `localhost:9999/agentic-ai-app:app-with-security-risk` の代わりに
> `ghcr.io/splunk/agentic-ai-app:app-with-security-risk` に更新してください。

### Kubernetes マニフェストの更新

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、
セキュリティリスクを含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-security-risk
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

## Cisco AI Defense でのイベントの確認

ワークショップの参加者は AI Defense アプリケーションに直接ログインすることはできません。
しかし、AI Defense ダッシュボードを表示できた場合、このリクエストに対してイベントが
記録されており、プロンプトに含まれるクレジットカード番号が自動的にマスクされていることが確認できます。

![AI Defense Events](../images/AIDefenseEvents.png)

AI Defense ではポリシーを設定して、特定の種類のセキュリティ問題を監視するかブロックするかを指定できます。今回のケースでは、PCI 関連の問題を監視のみする設定にしています。

## Splunk Observability Cloud でのデータの確認

Splunk Observability Cloud に戻って、トレースがどのように表示されるか確認しましょう。

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認してください
（例: `agentic-ai-$INSTANCE`）。ページにセキュリティリスクが表示されるようになったことが分かります。

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

> `AI overview` ページや、`plan_synthesizer` エージェントの `AI agent` ページでも
> セキュリティリスクが表示されるはずです。

`APM -> AI trace data` に移動し、最新のトレースを読み込みます。

エージェントフローで、セキュリティリスクが検出されたことが確認できます:

![Agent Flow With Security Risk](../images/AgentFlowWithSecurityRisk.png)

`activity_specialist` エージェントの `invoke_agent` スパンを見ると、LLM がレスポンスで
顧客のクレジットカード番号を平文で開示したため、PCI セキュリティリスクが検出されブロックされたことが分かります:

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)

セキュリティリスクをクリックすると、追加の詳細情報と Cisco AI Defense でイベントを表示するためのリンクが表示されます:

![Security Risk Details](../images/SecurityRiskDetails.png)

このスパンの `Span details` を表示すると、`gen_ai.security.event_id` 属性がこのスパンに含まれていることが確認できます:

![Security Event Span Attribute](../images/SecurityEventSpanAttribute.png)

この属性により、Splunk Observability Cloud のスパンと Cisco AI Defense の対応するイベントを関連付けることができます。
