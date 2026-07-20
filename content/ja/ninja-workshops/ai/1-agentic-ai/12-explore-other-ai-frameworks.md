---
title: その他のAgentic AIフレームワークの探索
linkTitle: 12. その他のAgentic AIフレームワークの探索
weight: 12
time: 15 minutes
---

このワークショップの前のセクションでは、**LangChain** と **LangGraph** で構築されたAgentic AIアプリケーションをOpenTelemetryで計装することに焦点を当てました。

このセクションでは、**その他の一般的なAgentic AIフレームワーク** に範囲を広げ、利用可能な計装アプローチを概説します。

大まかに言うと、Agentic AIアプリケーションをOpenTelemetryで計装するには **2つの主要なオプション** があります。最適なアプローチは、使用するフレームワークとアプリケーションに既存の計装があるかどうかによって異なります。

## 適切な計装アプローチの選択

### オプション1: Splunk OpenTelemetry計装（利用可能な場合に推奨）

Splunkは、以下を含むいくつかの広く使用されているAgentic AIフレームワーク向けにOpenTelemetry計装パッケージを提供しています。

* CrewAI
* LangChain/LangGraph
* LlamaIndex
* OpenAI SDK
* OpenAI Agents SDK

このアプローチを選択する場合:

* アプリケーションが上記のフレームワークのいずれかを使用している場合
* 最小限の設定でSplunk Observability Cloud向けに最適化された **OpenTelemetry計装** が必要な場合
* **ゼロコード** の計装体験を好む場合

#### 仕組み

[Zero-code instrumentation integrations](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation#zero-code-instrumentation-integrations-0)の手順に従ってアプリケーションを計装します。

フレームワークによっては、以下が必要になる場合があります。

* 追加のSplunk OpenTelemetryパッケージのインストール
* 以下のようなオプション機能を有効にするための特定の環境変数の設定
  * LLMのプロンプトと補完のキャプチャ
  * LLMレスポンスのセマンティック品質の評価
  * Cisco AI Defenseとの統合

**注意**: これは、ワークショップの前半でLangChainとLangGraphに使用したのと同じアプローチであり、オプションのプロンプトと補完のキャプチャも含まれます。

### オプション2: サードパーティ計装ライブラリ

フレームワークがSplunk OpenTelemetry計装で **直接サポートされていない** 場合、より広いフレームワークカバレッジを提供するサードパーティライブラリを使用できます。

一般的に使用されるサードパーティ計装ライブラリには以下が含まれます。

* [LangSmith](https://docs.langchain.com/langsmith/observability):
* [OpenLIT](https://docs.openlit.io/latest/sdk/overview)
* [Traceloop / OpenLLMetry](https://www.traceloop.com/docs/openllmetry/introduction)

このアプローチが適している場合:

* アプリケーションがオプション1に記載されていないAgentic AIフレームワークを使用している場合
* アプリケーションがサードパーティ計装ライブラリで **既に計装されている** 場合
* 既存のコードを再計装したくない場合

サードパーティライブラリは通常、独自のフォーマットまたは以前のOpenTelemetryスキーマでテレメトリを出力します。このデータをSplunk Observability Cloudと統合するには、以下を行います。

1. 出力されたテレメトリを最新のOpenTelemetryセマンティック規約に変換する **変換レイヤー** を有効にします。
2. OpenTelemetry Collectorを以下のように設定します。
    * 変換されたデータを受信する
    * Splunk Observability Cloudにエクスポートする

詳細な手順については、以下を参照してください。
[Translate and collect data from AI applications instrumented with third-party libraries](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/translate-data-from-third-party-instrumentation-libraries)

### まとめ

| シナリオ                             | 推奨オプション                          |
|--------------------------------------|-----------------------------------------|
| サポートされているフレームワーク、最小限のセットアップ | Splunk OpenTelemetry計装    |
| サポートされていないフレームワーク                | サードパーティ計装ライブラリ     |
| 既存のサードパーティ計装 | サードパーティ + OpenTelemetry変換 |

## CrewAIの例

CrewAIを使用した例を見ていきましょう。ワークショップで使用してきたトラベルプランナーアプリケーションは、CrewAIを使用して書き直されています。ソースコードは `~/workshop/agentic-ai/crewai` フォルダにあります。

CrewAIはエージェントとタスクを定義するために宣言的アプローチを使用していることに注目してください。例えば、`~/workshop/agentic-ai/crewai/config/agents.yaml` ファイルでは以下のようなエージェントが定義されています。

```yaml
coordinator:
  role: Travel Coordinator
  goal: Extract traveler intent and define a clear execution plan for specialists.
  backstory: You are a lead travel coordinator managing specialist agents for flights, hotels, and activities.
  verbose: true
  allow_delegation: false

flight_specialist:
  role: Flight Booking Specialist
  goal: Find an appealing and practical round-trip flight option.
  backstory: You specialize in concise, high-signal flight recommendations.
  verbose: true
  allow_delegation: false
```

また、`~/workshop/agentic-ai/crewai/config/tasks.yaml` ファイルでは以下のようなタスクが定義されています。

```yaml
coordinate_trip:
  description: >
  Read the user request and extract key trip details:
    origin, destination, travel style, and constraints.
    Provide a short execution brief for specialists.
  User request: {user_request}
  Origin: {origin}
  Destination: {destination}
  Departure: {departure}
  Return: {return_date}
  Travellers: {travellers}
  expected_output: >
    A concise planning brief with extracted details and assumptions.
  agent: coordinator
```

CrewAIアプリケーションを計装するために、以下のパッケージが `requirements.txt` ファイルに追加されていることに注目してください。

```text
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-crewai==0.1.3
splunk-otel-instrumentation-openai==0.1.0
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
```

### CrewAIの例をデプロイする

まず新しいDockerイメージをビルドして、CrewAIの例をデプロイしましょう。

``` bash
cd ~/workshop/agentic-ai/crewai
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:crewai .
docker push localhost:9999/agentic-ai-app:crewai
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを使用することを検討してください。その場合は、`~/workshop/agentic-ai/crewai/k8s.yaml` ファイルのイメージ名を `localhost:9999/agentic-ai-app:crewai` の代わりに `ghcr.io/splunk/agentic-ai-app:crewai` に更新します。

このバージョンのアプリケーションには別の環境名を使用しましょう。

```bash
kubectl create configmap instance-config-crewai \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-crewai-$INSTANCE \
-n travel-agent
```

次に、以下のようにマニフェストファイルを使用してCrewAIアプリケーションをデプロイします。

``` bash
kubectl apply -f ~/workshop/agentic-ai/crewai/k8s.yaml
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

### Splunk Observability Cloudでデータを表示する

Splunk Observability Cloudに戻り、CrewAIアプリケーションのTraceを表示しましょう。

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認します（例: `agentic-ai-crewai-$INSTANCE`）。エージェント名が少し異なることに気づくでしょう。

![CrewAI Agents](../images/CrewAiAgents.png)

`APM -> AI trace data` に移動し、最新のTraceを読み込みます。

Traceでは、LangChain/LangGraphバージョンのアプリケーションでキャプチャしたものと同様の詳細が表示されます。

![CrewAI Trace Details](../images/CrewAiTraceDetails.png)

CrewAIのTraceとLangChain/LangGraphのTraceで何か違いに気づきましたか？

{{< details summary="CrewAIのTraceとLangChain/LangGraphのTraceで何か違いに気づきましたか？" >}}

いくつかの違いがあります。

* エージェント名が異なります（`Hotel Booking Specialist` vs. `hotel_specialist`）
* CrewAIバージョンではcoordinatorとplan synthesizerエージェントがリストされていません
* `travel-planner-crewai` サービスのSpanには、ウォーターフォールビューの一部としてエージェントの指示が含まれています

{{< /details >}}
