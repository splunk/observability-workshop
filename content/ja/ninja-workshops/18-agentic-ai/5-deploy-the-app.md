---
title: Agentic AI アプリケーションのデプロイ
linkTitle: 5. Agentic AI アプリケーションのデプロイ
weight: 5
time: 15 minutes
---

## Agentic AI アプリケーションのデプロイ（Linux）

まず、Linux EC2 インスタンス上で直接アプリケーションを実行します。

### 環境変数の設定

コマンドターミナルで、Azure でホストされている OpenAI モデルへの接続方法をアプリケーションに指示する以下の環境変数を設定します

> 注: `AZURE_OPENAI_ENDPOINT` と `AZURE_OPENAI_API_KEY` の値はワークショップのインストラクターから提供されます。

``` bash
export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
export AZURE_OPENAI_API_VERSION=2024-12-01-preview
export AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
export AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

### 仮想環境の作成

次に、Python 仮想環境を作成し、アプリケーションの実行に必要なパッケージをインストールします

``` bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### アプリケーションの実行

以下のコマンドでアプリケーションを実行できます

``` bash
python3 main.py
```

### アプリケーションのテスト

EC2 インスタンスに接続した2つ目のターミナルセッションを開き、以下のコマンドを実行してアプリケーションをテストします。json 形式で提案された旅行プランが返されるはずです

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
{"activities_summary":"Sure! Here are signature activities for a week in Tokyo:\n\n1. Day 1: Explore Asakusa and Senso-ji Temple, then stroll Nakamise Shopping Street.\n2. Day 2: Visit Tsukiji Outer Market for fresh sushi breakfast, then tour Ginza for upscale shopping.\n3. Day 3: Spend the day in Shibuya—cross the famous scramble, visit Hachiko statue, and shop in trendy boutiques.\n4. Day 4: Explore Harajuku's Takeshita Street and Meiji Shrine, followed by Omotesando's stylish cafes.\n5. Day 5: Discover Akihabara's electronics and anime culture, with a visit to a themed café.\n6. Day 6: Take a day trip to Odaiba for teamLab Borderless digital art museum and waterfront views.\n7. Day 7: Relax in Ueno Park, visit museums, and shop at Ameya-Yokocho market.\n\nWould you like hotel or dining recommendations as well?","agent_steps":[{"agent":"coordinator","status":"completed"},{"agent":"flight_specialist","status":"completed"},{"agent":"hotel_specialist","status":"completed"}
```

{{% /tab %}}
{{< /tabs >}}

## Agentic AI アプリケーションのデプロイ（Kubernetes）

アプリケーションが正常に動作することを確認できたので、Kubernetes にデプロイしましょう。

### Dockerfile の作成

事前に作成された Dockerfile が `~/workshop/agentic-ai/base-app/Dockerfile` にあります。Docker イメージのビルド時に `requirements.txt` ファイル内のすべてのパッケージがインストールされることがわかります

````
RUN pip install --no-cache-dir -r requirements.txt
````

コンテナは以下のコマンドで起動されます

````
CMD ["python", "main.py"]
````

### Docker イメージのビルド

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:base-app .
docker push localhost:9999/agentic-ai-app:base-app
```

### Azure 認証情報を含む Secret の作成

Kubernetes secret を使用して Azure OpenAI のエンドポイントとキーを保存します

> 注: `AZURE_OPENAI_ENDPOINT` と `AZURE_OPENAI_API_KEY` の値はワークショップのインストラクターから提供されます。

``` bash
kubectl create ns travel-agent

kubectl create secret generic azure-openai-api -n travel-agent --from-literal=azure-openai-api-endpoint=your_azure_openai_api_endpoint --from-literal=azure-openai-api-key=your_azure_openai_api_key
```

### Kubernetes マニフェストファイルを使用したアプリケーションのデプロイ

事前に作成された Kubernetes マニフェストが `~/workshop/agentic-ai/base-app/k8s.yaml` にあります。

以下のようにマニフェストファイルを使用してアプリケーションをデプロイできます

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### アプリケーションの実行確認

以下のコマンドを使用して、アプリケーション Pod のステータスが `Running` であることを確認します

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

### Kubernetes でのアプリケーションのテスト

以下のコマンドを実行してアプリケーションをテストします

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
{"activities_summary":"Sure! Here are signature activities for a week in Tokyo:\n\n1. Day 1: Explore Asakusa and Senso-ji Temple, then stroll Nakamise Shopping Street.\n2. Day 2: Visit Tsukiji Outer Market for fresh sushi breakfast, then tour Ginza for upscale shopping.\n3. Day 3: Spend the day in Shibuya—cross the famous scramble, visit Hachiko statue, and shop in trendy boutiques.\n4. Day 4: Explore Harajuku's Takeshita Street and Meiji Shrine, followed by Omotesando's stylish cafes.\n5. Day 5: Discover Akihabara's electronics and anime culture, with a visit to a themed café.\n6. Day 6: Take a day trip to Odaiba for teamLab Borderless digital art museum and waterfront views.\n7. Day 7: Relax in Ueno Park, visit museums, and shop at Ameya-Yokocho market.\n\nWould you like hotel or dining recommendations as well?","agent_steps":[{"agent":"coordinator","status":"completed"},{"agent":"flight_specialist","status":"completed"},{"agent":"hotel_specialist","status":"completed"}
```

{{% /tab %}}
{{< /tabs >}}
