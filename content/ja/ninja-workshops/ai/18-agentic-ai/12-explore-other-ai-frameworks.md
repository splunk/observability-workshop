---
title: その他の Agentic AI フレームワークを試す
linkTitle: 12. その他の Agentic AI フレームワークを試す
weight: 12
time: 15 minutes
---

このワークショップのこれまでのセクションでは、**LangChain** と **LangGraph** で構築された Agentic AI アプリケーションを OpenTelemetry でインスツルメンテーションすることに焦点を当ててきました。

このセクションでは、対象範囲を広げて**その他の人気のある Agentic AI フレームワーク**を取り上げ、利用可能なインスツルメンテーション手法を概説します。

大まかに言うと、Agentic AI アプリケーションを OpenTelemetry でインスツルメンテーションするには、**主に 2 つの選択肢**があります。最適な手法は、使用しているフレームワークと、アプリケーションに既存のインスツルメンテーションが含まれているかどうかによって異なります。

## 適切なインスツルメンテーション手法の選択

### オプション 1: Splunk OpenTelemetry Instrumentation（利用可能な場合に推奨）

Splunk は、広く使われているいくつかの Agentic AI フレームワーク向けに OpenTelemetry インスツルメンテーションパッケージを提供しています。対応フレームワークは以下のとおりです。

* CrewAI
* LangChain/LangGraph
* LlamaIndex
* OpenAI SDK
* OpenAI Agents SDK

#### このオプションを使用する場面

このアプローチは、次のような場合に選択してください。

* アプリケーションが上記のいずれかのフレームワークを使用している。
* 最小限の構成で Splunk Observability Cloud に最適化された **OpenTelemetry インスツルメンテーション** を利用したい。
* **zero-code** によるインスツルメンテーションを好む。

#### 仕組み

[Zero-code instrumentation integrations](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/zero-code-instrumentation#zero-code-instrumentation-integrations-0) の手順に従ってアプリケーションをインスツルメンテーションします。

フレームワークによっては、次の対応が必要になる場合があります。

* 追加の Splunk OpenTelemetry パッケージのインストール
* 以下のようなオプション機能を有効にするための環境変数の設定:
  * LLM のプロンプトと応答のキャプチャ
  * LLM 応答の意味的品質の評価
  * Cisco AI Defense との統合

**Note**: これは、ワークショップの前半で LangChain と LangGraph に対して使用したのと同じアプローチで、オプションのプロンプトおよび応答のキャプチャも含まれます。

### オプション 2: サードパーティーのインスツルメンテーションライブラリ

フレームワークが Splunk OpenTelemetry インスツルメンテーションで**直接サポートされていない**場合は、より広範なフレームワークをカバーするサードパーティーライブラリを使用できます。

よく使用されるサードパーティーのインスツルメンテーションライブラリには次のものがあります。

* [LangSmith](https://docs.langchain.com/langsmith/observability):
* [OpenLIT](https://docs.openlit.io/latest/sdk/overview)
* [Traceloop / OpenLLMetry](https://www.traceloop.com/docs/openllmetry/introduction)

#### このオプションを使用する場面

このアプローチは、次のような場合に適しています。

* アプリケーションがオプション 1 に記載されていない Agentic AI フレームワークを使用している
* アプリケーションが**すでに**サードパーティーのインスツルメンテーションライブラリで**インスツルメンテーション済み**である
* 既存のコードを再インスツルメンテーションしたくない

#### 仕組み

サードパーティーライブラリは通常、独自のフォーマットや古い OpenTelemetry スキーマでテレメトリーを出力します。このデータを Splunk Observability Cloud と統合するには、次の手順を行います。

1. 出力されたテレメトリーを最新の OpenTelemetry セマンティック規約に変換する**変換レイヤー**を有効にします。
2. OpenTelemetry Collector を次のように構成します。

* 変換されたデータを受信する
* Splunk Observability Cloud にエクスポートする

ステップごとの手順については、次を参照してください。
[Translate and collect data from AI applications instrumented with third-party libraries](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring/set-up-ai-agent-monitoring/translate-data-from-third-party-instrumentation-libraries)

### まとめ

| シナリオ                             | 推奨オプション                          |
|--------------------------------------|-----------------------------------------|
| サポートされているフレームワーク、最小限のセットアップ   | Splunk OpenTelemetry Instrumentation    |
| サポートされていないフレームワーク                | サードパーティーのインスツルメンテーションライブラリ     |
| 既存のサードパーティーインスツルメンテーション | サードパーティー + OpenTelemetry 変換 |

## CrewAI の例

CrewAI を使った例を見ていきましょう。ワークショップ中に使用してきたトラベルプランナーアプリケーションを CrewAI で書き直したものです。ソースコードは `~/workshop/agentic-ai/crewai` フォルダーにあります。

CrewAI ではエージェントとタスクを定義する際に宣言的なアプローチを使用する点に注意してください。たとえば、`~/workshop/agentic-ai/crewai/config/agents.yaml` ファイルでは次のようなエージェントを定義しています。

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

そして `~/workshop/agentic-ai/crewai/config/tasks.yaml` ファイルでは次のようなタスクを定義しています。

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

CrewAI アプリケーションをインスツルメンテーションするために、`requirements.txt` ファイルに次のパッケージが追加されている点に注目してください。

````
splunk-opentelemetry==2.8.0
splunk-otel-instrumentation-crewai==0.1.3
splunk-otel-instrumentation-openai==0.1.0
splunk-otel-genai-emitters-splunk==0.1.7
splunk-otel-util-genai==0.1.9
opentelemetry-instrumentation-flask==0.59b0
````

### CrewAI の例のデプロイ

まず新しい Docker イメージをビルドして、CrewAI の例をデプロイしましょう。

``` bash
cd ~/workshop/agentic-ai/crewai
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:crewai .
docker push localhost:9999/agentic-ai-app:crewai
```

> Tip: イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを使用することを検討してください。
> その場合、`~/workshop/agentic-ai/crewai/k8s.yaml` ファイル内のイメージ名を
> `localhost:9999/agentic-ai-app:crewai` から `ghcr.io/splunk/agentic-ai-app:crewai` に変更してください。

このバージョンのアプリケーションには別の environment 名を使用しましょう。

```bash
kubectl create configmap instance-config-crewai \
--from-literal=OTEL_RESOURCE_ATTRIBUTES=deployment.environment=agentic-ai-crewai-$INSTANCE \
-n travel-agent
```

それから、次のようにマニフェストファイルを使用して CrewAI アプリケーションをデプロイできます。

``` bash
kubectl apply -f ~/workshop/agentic-ai/crewai/k8s.yaml
```

### Kubernetes でアプリケーションをテスト

新しいアプリケーションの Pod が正常に起動し、古い Pod が存在しなくなっていることを確認します。

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

### Splunk Observability Cloud でデータを表示

Splunk Observability Cloud に戻って、CrewAI アプリケーションのトレースを表示しましょう。

`APM` に移動し、`AI agents` を選択します。environment 名（例: `agentic-ai-crewai-$INSTANCE`）が選択されていることを確認します。エージェント名がわずかに異なっていることに気付くはずです。

![CrewAI Agents](../images/CrewAiAgents.png)

`APM -> AI trace data` に移動して、最新のトレースを読み込みます。

トレースには、LangChain/LangGraph 版のアプリケーションでキャプチャしたものと同様の詳細が表示されているはずです。

![CrewAI Trace Details](../images/CrewAiTraceDetails.png)

LangChain/LangGraph のトレースと比較して、CrewAI のトレースで何か違いに気付きましたか？

<details>
  <summary><b>クリックして答えを表示</b></summary>

いくつかの違いがあります。

* エージェント名が異なります（`Hotel Booking Specialist` と `hotel_specialist`）
* CrewAI 版には coordinator と plan synthesizer のエージェントが表示されていません
* `travel-planner-crewai` サービスのスパンには、ウォーターフォールビューの一部としてエージェントの指示が含まれています

</details>
