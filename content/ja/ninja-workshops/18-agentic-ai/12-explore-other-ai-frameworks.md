---
title: その他のエージェント AI フレームワークの探索
linkTitle: 12. その他のエージェント AI フレームワークの探索
weight: 12
time: 15 minutes
---

このワークショップの前のセクションでは、**LangChain** と **LangGraph** を使用して構築されたエージェント AI アプリケーションを OpenTelemetry で計装することに焦点を当てました。

このセクションでは、範囲を広げて**その他の一般的なエージェント AI フレームワーク**を取り上げ、利用可能な計装アプローチの概要を説明します。

大まかに言うと、エージェント AI アプリケーションを OpenTelemetry で計装するには**2つの主要なオプション**があります。最適なアプローチは、使用するフレームワークとアプリケーションに既存の計装が含まれているかどうかによって異なります。

## 適切な計装アプローチの選択

### オプション 1: Splunk OpenTelemetry 計装（利用可能な場合に推奨）

Splunk は、以下を含む広く使用されているエージェント AI フレームワーク向けに OpenTelemetry 計装パッケージを提供しています:

* CrewAI
* LangChain/LangGraph
* LlamaIndex
* OpenAI SDK
* OpenAI Agents SDK

#### このオプションを使用する場合

以下の場合にこのアプローチを選択します:

* アプリケーションが上記のフレームワークのいずれかを使用している場合。
* 最小限の設定で Splunk Observability Cloud 向けに最適化された **OpenTelemetry 計装**が必要な場合。
* **ゼロコード**の計装体験を希望する場合。

#### 仕組み

[Zero-code instrumentation integrations](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation#zero-code-instrumentation-integrations-0) の手順に従ってアプリケーションを計装します。

フレームワークによっては、以下が必要になる場合があります:

* 追加の Splunk OpenTelemetry パッケージのインストール
* 以下のようなオプション機能を有効にするための特定の環境変数の設定:
  * LLM のプロンプトと補完のキャプチャ
  * LLM レスポンスのセマンティック品質の評価
  * Cisco AI Defense との統合

**注**: これは、ワークショップの前半で LangChain と LangGraph に使用したアプローチと同じであり、オプションのプロンプトおよび補完キャプチャも含まれています。

### オプション 2: サードパーティ計装ライブラリ

フレームワークが Splunk OpenTelemetry 計装で**直接サポートされていない**場合は、より広範なフレームワークカバレッジを提供するサードパーティライブラリを使用できます。

一般的に使用されるサードパーティ計装ライブラリには以下があります:

* [LangSmith](https://docs.langchain.com/langsmith/observability):
* [OpenLIT](https://docs.openlit.io/latest/sdk/overview)
* [Traceloop / OpenLLMetry](https://www.traceloop.com/docs/openllmetry/introduction)

#### このオプションを使用する場合

このアプローチは以下の場合に適しています:

* アプリケーションがオプション 1 に記載されていないエージェント AI フレームワークを使用している場合
* アプリケーションがサードパーティ計装ライブラリで**すでに計装されている**場合
* 既存のコードの再計装を避けたい場合

#### 仕組み

サードパーティライブラリは通常、独自のフォーマットまたは以前の OpenTelemetry スキーマでテレメトリを出力します。このデータを Splunk Observability Cloud と統合するには:

1. 出力されたテレメトリを最新の OpenTelemetry セマンティック規約に変換する**変換レイヤー**を有効にします。
2. OpenTelemetry Collector を以下のように設定します:

* 変換されたデータを受信する
* Splunk Observability Cloud にエクスポートする

手順の詳細については、以下を参照してください:
[Translate and collect data from AI applications instrumented with third-party libraries](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/translate-data-from-third-party-instrumentation-libraries)

### まとめ

| シナリオ                             | 推奨オプション                          |
|--------------------------------------|-----------------------------------------|
| サポートされているフレームワーク、最小限のセットアップ   | Splunk OpenTelemetry 計装    |
| サポートされていないフレームワーク                | サードパーティ計装ライブラリ     |
| 既存のサードパーティ計装 | サードパーティ + OpenTelemetry 変換 |

## CrewAI の例

CrewAI を使用した例を見ていきましょう。ワークショップで使用してきた旅行プランナーアプリケーションは、CrewAI を使用して書き直されています。ソースコードは `~/workshop/agentic-ai/crewai` フォルダにあります。

CrewAI は宣言的なアプローチを使用してエージェントとタスクを定義することに注意してください。例えば、`~/workshop/agentic-ai/crewai/config/agents.yaml` ファイルでは、以下のようなエージェントが定義されています:

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

また、`~/workshop/agentic-ai/crewai/config/tasks.yaml` ファイルでは、以下のようなタスクが定義されています:

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

CrewAI アプリケーションを計装するために、以下のパッケージが `requirements.txt` ファイルに追加されていることに注目してください:

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-crewai==0.1.3
splunk-otel-instrumentation-openai==0.1.0
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

### CrewAI の例をデプロイする

まず、新しい Docker イメージをビルドして CrewAI の例をデプロイしましょう:

``` bash
cd ~/workshop/agentic-ai/crewai
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:crewai .
docker push localhost:9999/agentic-ai-app:crewai
```

このバージョンのアプリケーションには別の環境名を使用しましょう:

```bash
kubectl create configmap instance-config-crewai \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-crewai-$INSTANCE \
-n travel-agent
```

次に、以下のようにマニフェストファイルを使用して CrewAI アプリケーションをデプロイします:

``` bash
kubectl apply -f ~/workshop/agentic-ai/crewai/k8s.yaml
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

### Splunk Observability Cloud でデータを表示する

Splunk Observability Cloud に戻り、CrewAI アプリケーションのトレースを表示しましょう。

`APM` に移動し、`AI agents` を選択します。環境名が選択されていることを確認してください（例: `agentic-ai-crewai-$INSTANCE`）。エージェント名が若干異なることに気づくでしょう:

![CrewAI Agents](../images/CrewAiAgents.png)

`APM -> AI trace data` に移動し、最新のトレースを読み込みます。

トレースには、LangChain/LangGraph バージョンのアプリケーションでキャプチャしたものと同様の詳細が表示されるはずです:

![CrewAI Trace Details](../images/CrewAiTraceDetails.png)

CrewAI のトレースと LangChain/LangGraph のトレースで異なる点に気づきましたか？

<details>
  <summary><b>ここをクリックして回答を表示</b></summary>

いくつかの違いがあります:

* エージェント名が異なります（`Hotel Booking Specialist` と `hotel_specialist`）
* CrewAI バージョンでは coordinator と plan synthesizer エージェントが表示されません
* `crewai` 推定サービスのスパンには、ウォーターフォールビューの一部としてエージェントの指示が含まれています

</details>
