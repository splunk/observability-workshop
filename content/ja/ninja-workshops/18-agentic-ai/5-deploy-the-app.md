---
title: Agentic AI アプリケーションのデプロイ
linkTitle: 5. Agentic AI アプリケーションのデプロイ
weight: 5
time: 15 minutes
---

## Agentic AI アプリケーションのデプロイ (Linux)

まず、Linux EC2 インスタンス上でアプリケーションを直接実行します。

### 環境変数の設定

ワークショップのインストラクターから提供されたドキュメントには、以下の環境変数を設定するための `export` コマンドが記載されています:

* `AZURE_OPENAI_DEPLOYMENT_NAME`
* `AZURE_OPENAI_API_VERSION`
* `AZURE_OPENAI_ENDPOINT`
* `AZURE_OPENAI_API_KEY`

これらの環境変数は、Azure でホストされている OpenAI モデルへの接続方法をアプリケーションに伝えます。

ドキュメントからこれらの `export` コマンドをコピーして、SSH ターミナルに貼り付けて実行してください。

### 仮想環境の作成

次に、Python 仮想環境を作成し、アプリケーションの実行に必要なパッケージをインストールします:

``` bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### アプリケーションの実行

以下のコマンドでアプリケーションを実行します:

``` bash
python3 main.py
```

### アプリケーションのテスト

EC2 インスタンスに接続された2つ目のターミナルセッションを開き、以下のコマンドを実行してアプリケーションをテストします。提案された旅行プランが JSON 形式で返されるはずです:

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

アプリケーションが正常に動作していることを確認したら、最初のターミナルに戻ってアプリケーションを停止してください。

## Agentic AI アプリケーションのデプロイ (Kubernetes)

アプリケーションが正常に動作することを確認できたので、Kubernetes にデプロイしましょう。

### Docker イメージのビルド

このセクションでは、`~/workshop/agentic-ai/base-app/Dockerfile` にある Dockerfile を使用して、アプリケーションの Docker イメージをビルドします。以下のコマンドを実行してイメージをビルドしてください:

``` bash
cd ~/workshop/agentic-ai/base-app
docker build --platform linux/amd64 -t localhost:9999/agentic-ai-app:base-app .
docker push localhost:9999/agentic-ai-app:base-app
```

> ヒント: イメージのビルドに時間がかかりすぎる場合は、ビルド済みのイメージを使用することを検討してください。その場合は、`~/workshop/agentic-ai/base-app/k8s.yaml` ファイル内のイメージ名を `localhost:9999/agentic-ai-app:base-app` から `ghcr.io/splunk/agentic-ai-app:base-app` に変更してください。

### アプリケーション用 Namespace の作成

アプリケーションをホストするための新しい Namespace を作成しましょう:

``` bash
kubectl create ns travel-agent
```

### Azure 資格情報を含む Secret の作成

Kubernetes Secret を使用して、Azure OpenAI のエンドポイントとキーを保存します:

> 注意: このコマンドは、先ほど `AZURE_OPENAI_ENDPOINT` と `AZURE_OPENAI_API_KEY` の環境変数を設定したターミナルで実行してください。

``` bash
{ [ -z "$AZURE_OPENAI_ENDPOINT" ] || \
  [ -z "$AZURE_OPENAI_API_KEY" ]; } && \
  echo "Error: Missing variables" || \
  kubectl create secret generic azure-openai-api \
  -n travel-agent \
  --from-literal=azure-openai-api-endpoint=$AZURE_OPENAI_ENDPOINT \
  --from-literal=azure-openai-api-key=$AZURE_OPENAI_API_KEY
```

> 補足: Missing variables というエラーが表示された場合は、インストラクターから提供されたドキュメントの `export` コマンドを使用して、環境変数を再度設定する必要があります。

### Kubernetes マニフェストファイルを使用したアプリケーションのデプロイ

ビルド済みの Kubernetes マニフェストは、`~/workshop/agentic-ai/base-app/k8s.yaml` というファイルにあります。

以下のようにマニフェストファイルを使用してアプリケーションをデプロイできます:

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### アプリケーションの実行確認

以下のコマンドを使用して、アプリケーションの Pod のステータスが `Running` であることを確認してください:

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

以下のコマンドを実行してアプリケーションをテストします:

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

トラブルシューティングが必要な場合は、以下のコマンドを使用してアプリケーションのログを確認してください:

```bash
kubectl logs -l app=travel-planner-langchain -n travel-agent -f
```
