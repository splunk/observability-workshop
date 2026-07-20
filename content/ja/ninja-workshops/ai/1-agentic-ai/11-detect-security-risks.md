---
title: セキュリティリスクの検出
linkTitle: 11. セキュリティリスクの検出
weight: 11
time: 15 minutes
---

> 注意: このワークショップのセクションでは、複数のファイルを変更する必要があります。
> どこを変更すればよいか分からない場合や、アプリケーションが動作しなくなった場合は、
> `~/workshop/agentic-ai/app-with-security-risk` フォルダにあるこのセクションのモデルソリューションを参照してください。

前のセクションでは、アプリケーションエージェントの1つの出力に品質問題を注入するラッパーを追加しました。

このセクションでは、同様の手順でセキュリティリスクを作成します。

その後、これらのリスクがSplunk Observability Cloudでどのように表示されるかを紹介します。

## Activity Specialistの出力を汚染する

Activity Specialistエージェントがこのラッパーを使用してLLMの出力を変更するように修正します。

`~/workshop/agentic-ai/base-app/main.py` ファイルを編集用に開きます。

`activity_specialist_node` 関数の定義を以下のバージョンに置き換えます。
これはLLMがレスポンスの一部としてユーザーのクレジットカード番号を含めたシナリオを効果的にシミュレートするもので、明らかなセキュリティリスクおよびPCI違反です。

> [!TIP]
> `vi` エディタで大量の行を一括削除するには、`Shift` + `v` を押して `Visual
> Line` モードにし、下矢印キーで削除したい行をすべて選択してから、`d` を押して選択した行を削除します。

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

{{% notice title="先に進む前に作業を確認してください" style="primary" icon="running" %}}

次のコマンドを実行して、変更内容を期待されるソリューションと比較します。

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-security-risk/main.py
```

{{% / notice %}}

## 更新されたDockerイメージをビルドする

新しいタグで更新されたDockerイメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、事前ビルド済みのイメージを使用することを検討してください。
> その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルのイメージ名を
> `localhost:9999/agentic-ai-app:app-with-security-risk` の代わりに `ghcr.io/splunk/agentic-ai-app:app-with-security-risk` に更新します。

### Kubernetesマニフェストを更新する

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、セキュリティリスクを含むイメージを使用するようにイメージを更新します。

```yaml
          image: localhost:9999/agentic-ai-app:app-with-security-risk
```

### 更新されたアプリケーションをデプロイする

マニフェストファイルを使用して、更新されたアプリケーションを次のようにデプロイします。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetesでアプリケーションをテストする

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

## Cisco AI Defenseでイベントを表示する

ワークショップ参加者はAI Defenseアプリケーションに直接ログインすることはできません。
しかし、AI Defenseダッシュボードを表示できた場合、このリクエストに対してイベントが記録され、プロンプトに含まれるクレジットカード番号が自動的にマスクされていることが確認できます。

![AI Defense Events](../images/AIDefenseEvents.png)

AI Defenseではポリシーを設定して、特定の種類のセキュリティ問題をモニタリングするかブロックするかを指定できます。この場合、PCI関連の問題はモニタリングのみを選択しています。

## Splunk Observability Cloudでデータを表示する

Splunk Observability Cloudに戻って、トレースがどのように表示されるか確認しましょう。

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認します（例: `agentic-ai-$INSTANCE`）。ページにセキュリティリスクが表示されるようになっています。

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

> `AI overview` ページや `plan_synthesizer` エージェントの `AI agent` ページでもセキュリティリスクが表示されます。

`APM -> AI trace data` に移動し、最新のトレースを読み込みます。

エージェントフローで、セキュリティリスクが検出されたことを確認できます。

![Agent Flow With Security Risk](../images/AgentFlowWithSecurityRisk.png)

`activity_specialist` エージェントの `invoke_agent` Spanを見ると、LLMがレスポンスで顧客のクレジットカード番号を平文で開示したことにより、PCIセキュリティリスクが検出されブロックされたことが確認できます。

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)

セキュリティリスクをクリックすると、追加の詳細情報とCisco AI Defenseでイベントを表示するためのリンクが表示されます。

![Security Risk Details](../images/SecurityRiskDetails.png)

このSpanの `Span details` を表示すると、`gen_ai.security.event_id` 属性がこのSpanに含まれていることが確認できます。

![Security Event Span Attribute](../images/SecurityEventSpanAttribute.png)

この属性により、Splunk Observability CloudのSpanとCisco AI Defenseの対応するイベントを関連付けることができます。
