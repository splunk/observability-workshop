---
title: Agentic AIアプリケーションのデプロイ
linkTitle: 5. Agentic AIアプリケーションのデプロイ
weight: 5
time: 15 minutes
---

## Agentic AIアプリケーションのデプロイ（Linux）

まず、Linux EC2インスタンス上で直接アプリケーションを実行します。

### 環境変数の設定

EC2インスタンスには、以下の環境変数が事前に設定されています。これらは、Azure上でホストされているOpenAIモデル（Lite LLM Proxy経由）への接続方法をアプリケーションに伝えます。

* `OPENAI_API_KEY`
* `OPENAI_BASE_URL`

### 仮想環境の作成

次に、Python仮想環境を作成し、アプリケーションの実行に必要なパッケージをインストールします。

``` bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### アプリケーションの実行

以下のコマンドでアプリケーションを実行します。

``` bash
python3 main.py
```

### アプリケーションのテスト

EC2インスタンスに接続した2つ目のターミナルセッションを開き、以下のコマンドを実行してアプリケーションをテストします。推奨される旅行プランがJSON形式で返されます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl http://localhost:8080/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Seattle",
    "destination": "Tokyo",
    "user_request": "We are planning a week-long trip to Seattle from Tokyo. Looking for boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"activities_summary":"Sure! Here are signature activities for a week in Tokyo:\n\n1. Day 1: Explore Asakusa and Senso-ji Temple, then stroll Nakamise Shopping Street.\n2. Day 2: Visit Tsukiji Outer Market for fresh sushi breakfast, then tour Ginza for upscale shopping.\n3. Day 3: Spend the day in Shibuya—cross the famous scramble, visit Hachiko statue, and shop in trendy boutiques.\n4. Day 4: Explore Harajuku’s Takeshita Street and Meiji Shrine, followed by Omotesando’s stylish cafes.\n5. Day 5: Discover Akihabara’s electronics and anime culture, with a visit to a themed café.\n6. Day 6: Take a day trip to Odaiba for teamLab Borderless digital art museum and waterfront views.\n7. Day 7: Relax in Ueno Park, visit museums, and shop at Ameya-Yokocho market.\n\nWould you like hotel or dining recommendations as well?","agent_steps":[{"agent":"coordinator","status":"completed"},{"agent":"flight_specialist","status":"completed"},{"agent":"hotel_specialist","status":"completed"}
```

{{% /tab %}}
{{< /tabs >}}

### アプリケーションの停止

アプリケーションが正常に動作していることを確認したら、最初のターミナルに戻ってアプリケーションを停止します。

## Agentic AIアプリケーションのデプロイ（Kubernetes）

アプリケーションが正常に動作することを確認できたので、Kubernetesにデプロイしましょう。

### Dockerイメージのビルド

このセクションでは、`~/workshop/agentic-ai/base-app/Dockerfile` にあるDockerfileを使用して、アプリケーションのDockerイメージをビルドします。以下のコマンドを実行してイメージをビルドします。

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:base-app .
docker push localhost:9999/agentic-ai-app:base-app
```

> [!TIP]
> イメージのビルドに時間がかかりすぎる場合は、事前にビルドされたイメージの使用を検討してください。その場合、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内のイメージ名を `localhost:9999/agentic-ai-app:base-app` の代わりに `ghcr.io/splunk/agentic-ai-app:base-app` に変更します。

### アプリケーションNamespaceの作成

アプリケーションをホストする新しいNamespaceを作成します。

``` bash
kubectl create ns travel-agent
```

### OpenAI認証情報のSecret作成

KubernetesのSecretを使用して、OpenAIのエンドポイントとキーを保存します。

``` bash
{ [ -z "$OPENAI_API_KEY" ] || \
  [ -z "$OPENAI_BASE_URL" ]; } && \
  echo "Error: Missing variables" || \
  kubectl create secret generic openai-api \
  -n travel-agent \
  --from-literal=openai-api-endpoint=$OPENAI_BASE_URL \
  --from-literal=openai-api-key=$OPENAI_API_KEY
```

> [!NOTE]
> Missing variablesというエラーが表示された場合は、このコマンドを実行する前にOpenAI APIに接続するための環境変数を手動で定義する必要があります。

### Kubernetesマニフェストファイルを使用したアプリケーションのデプロイ

事前に作成されたKubernetesマニフェストは `~/workshop/agentic-ai/base-app/k8s.yaml` にあります。

以下のようにマニフェストファイルを使用してアプリケーションをデプロイします。

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### アプリケーションの実行確認

以下のコマンドを使用して、アプリケーションPodのステータスが `Running` であることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods -n travel-agent
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
NAME                                        READY   STATUS    RESTARTS   AGE
travel-planner-langchain-68977dc5c4-4w7p9   1/1     Running   0          41s
```

{{% /tab %}}
{{< /tabs >}}

### Kubernetes上でのアプリケーションテスト

以下のコマンドを実行してアプリケーションをテストします。

{{< tabs >}}
{{% tab title="Script" %}}

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

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{"activities_summary":"Sure! Here are signature activities for a week in Tokyo:\n\n1. Day 1: Explore Asakusa and Senso-ji Temple, then stroll Nakamise Shopping Street.\n2. Day 2: Visit Tsukiji Outer Market for fresh sushi breakfast, then tour Ginza for upscale shopping.\n3. Day 3: Spend the day in Shibuya—cross the famous scramble, visit Hachiko statue, and shop in trendy boutiques.\n4. Day 4: Explore Harajuku’s Takeshita Street and Meiji Shrine, followed by Omotesando’s stylish cafes.\n5. Day 5: Discover Akihabara’s electronics and anime culture, with a visit to a themed café.\n6. Day 6: Take a day trip to Odaiba for teamLab Borderless digital art museum and waterfront views.\n7. Day 7: Relax in Ueno Park, visit museums, and shop at Ameya-Yokocho market.\n\nWould you like hotel or dining recommendations as well?","agent_steps":[{"agent":"coordinator","status":"completed"},{"agent":"flight_specialist","status":"completed"},{"agent":"hotel_specialist","status":"completed"}
```

{{% /tab %}}
{{< /tabs >}}

## トラブルシューティング

トラブルシューティングが必要な場合は、以下のコマンドを使用してアプリケーションログを確認します。

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```
