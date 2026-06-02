---
title: Detect Security Risks
linkTitle: 11. Detect Security Risks
weight: 11
time: 15 minutes
---

> 注: ワークショップのこのセクションでは、複数のファイルへの変更が必要です。
> どこに変更を加えればよいかわからない場合や、アプリケーションが
> 動作しなくなった場合は、このセクションのモデルソリューションを参照してください。
> モデルソリューションは `~/workshop/agentic-ai/app-with-security-risk` フォルダにあります。

前のセクションでは、アプリケーションエージェントの1つの出力に品質問題を注入するためのラッパーを追加しました。

このセクションでは、同様の演習を行ってセキュリティリスクを作成します。

その後、これらのリスクが Splunk Observability Cloud にどのように表示されるかを紹介します。

## Activity Specialistの出力を汚染する

このラッパーを使用するように Activity Specialist エージェントを変更し、
LLM の出力を改変しましょう。

`~/workshop/agentic-ai/base-app/main.py` ファイルを編集用に開きます。

`activity_specialist_node` 関数の定義を、以下に示すバージョンに置き換えます。
これは、LLM がレスポンスの一部としてユーザーのクレジットカード番号を含めてしまったシナリオを
シミュレートしており、明確なセキュリティリスクであり PCI 違反となります。

> ヒント: `vi` エディターで多数の行を一括削除するには、`Shift` + `v` を押して `Visual
> Line` モードに入り、下矢印キーで削除したいすべての行を選択してから `d` を押して
> 選択した行を削除します。

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

{{% notice title="次に進む前に作業内容を確認してください" style="primary" icon="running" %}}

次のコマンドを実行して、変更内容を期待されるソリューションと比較します:

```bash
diff ~/workshop/agentic-ai/base-app/main.py ~/workshop/agentic-ai/app-with-security-risk/main.py
```

{{% / notice %}}

## 更新された Docker イメージをビルドする

新しいタグを付けて、更新された Docker イメージをビルドします:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:app-with-security-risk .
docker push localhost:9999/agentic-ai-app:app-with-security-risk
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを
> 使用することを検討してください。そのためには、`~/workshop/agentic-ai/base-app/k8s.yaml`
> ファイルのイメージ名を `localhost:9999/agentic-ai-app:app-with-security-risk` ではなく
> `ghcr.io/splunk/agentic-ai-app:app-with-security-risk` に更新します。

### Kubernetes マニフェストを更新する

`~/workshop/agentic-ai/base-app/k8s.yaml` ファイルを編集用に開き、
セキュリティリスクを含むイメージを使用するようにイメージを更新します:

```yaml
          image: localhost:9999/agentic-ai-app:app-with-security-risk
```

### 更新されたアプリケーションをデプロイする

次のようにマニフェストファイルを使用して、更新されたアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でアプリケーションをテストする

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

## Cisco AI Defense でイベントを表示する

ワークショップ参加者は AI Defense アプリケーションに直接ログインすることはできません。
ただし、AI Defense ダッシュボードを表示できれば、このリクエストに対してイベントが
ログに記録され、プロンプトに含まれていたクレジットカード番号が自動的に編集（マスク）
されていることを確認できます。

![AI Defense Events](../images/AIDefenseEvents.png)

AI Defense では、特定の種類のセキュリティ問題を監視するかブロックするかを指定する
ポリシーを設定できることに注意してください。今回の場合、PCI 関連の問題は監視のみを
行うように選択しています。

## Splunk Observability Cloud でデータを表示する

Splunk Observability Cloud に戻って、トレースが今どのように見えるかを確認しましょう。

`APM` に移動し、`AI agents` を選択します。環境名（例: `agentic-ai-$INSTANCE`）が
選択されていることを確認してください。ページにセキュリティリスクが含まれていることが
わかります！

![Agents with Security Risks](../images/AgentsWithSecurityRisks.png)

> セキュリティリスクは `AI overview` ページや、`plan_synthesizer` エージェントの
> `AI agent` ページにも表示されるはずです。

`APM -> AI trace data` に移動し、最新のトレースを読み込みます。

エージェントフローでは、セキュリティリスクが検出されたことがわかります:

![Agent Flow With Security Risk](../images/AgentFlowWithSecurityRisk.png)

`activity_specialist` エージェントの `invoke_agent` スパンを見ると、LLM がレスポンスの中で
顧客のクレジットカード番号を平文で開示したため、PCI セキュリティリスクが検出されてブロック
されたことがわかります:

![Trace With Security Risk](../images/TraceWithSecurityRisk.png)

セキュリティリスクをクリックすると、追加の詳細と Cisco AI Defense でイベントを表示する
ためのリンクが提供されます:

![Security Risk Details](../images/SecurityRiskDetails.png)

このスパンの `Span details` を表示すると、`gen_ai.security.event_id` 属性がこのスパンに
含まれていることがわかります:

![Security Event Span Attribute](../images/SecurityEventSpanAttribute.png)

この属性により、Splunk Observability Cloud のスパンを Cisco AI Defense の対応するイベントと
関連付けることができます。
