---
title: Agentic AI アプリケーションのデプロイ
linkTitle: 5. Agentic AI アプリケーションのデプロイ
weight: 5
time: 20 minutes
---

## Agentic AI アプリケーションのデプロイ（Linux）

まず、Linux EC2インスタンス上で直接アプリケーションを実行します。

### 環境変数の設定

コマンドターミナルで、以下の環境変数を設定します：

> 注: `AZURE_OPENAI_ENDPOINT` と `AZURE_OPENAI_API_KEY` の値はワークショップのインストラクターから提供されます。

``` bash
export AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
export AZURE_OPENAI_API_VERSION=2024-12-01-preview
export AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
export AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

### 仮想環境の作成

次に、Python仮想環境を作成し、アプリケーションの実行に必要なパッケージをインストールします：

``` bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### アプリケーションの実行

以下のコマンドでアプリケーションを実行します：

``` bash
python3 main.py
```

### アプリケーションのテスト

EC2インスタンスに接続された2つ目のターミナルセッションを開き、以下のコマンドを実行してアプリケーションをテストします：

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

## Agentic AI アプリケーションのデプロイ（Kubernetes）

アプリケーションが正常に動作していることを確認できたので、Kubernetesにデプロイしましょう。

### Dockerfile の作成

ビルド済みのDockerfileは `~/workshop/agentic-ai/base-app/Dockerfile` にあります。Dockerイメージのビルド時に `requirements.txt` ファイル内のすべてのパッケージがインストールされることがわかります：

````
RUN pip install --no-cache-dir -r requirements.txt
````

コンテナは以下のコマンドで起動されます：

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

Kubernetes Secretを使用してAzure OpenAIエンドポイントとキーを保存します：

> 注: `AZURE_OPENAI_ENDPOINT` と `AZURE_OPENAI_API_KEY` の値はワークショップのインストラクターから提供されます。

``` bash
kubectl create ns travel-agent

kubectl create secret generic azure-openai-api -n travel-agent --from-literal=azure-openai-api-endpoint=your_azure_openai_api_endpoint --from-literal=azure-openai-api-key=your_azure_openai_api_key
```

### Kubernetes マニフェストファイルを使用したアプリケーションのデプロイ

ビルド済みのKubernetesマニフェストは `~/workshop/agentic-ai/base-app/k8s.yaml` にあります。

以下のようにマニフェストファイルを使用してアプリケーションをデプロイできます：

``` bash
kubectl apply -f ~/workshop/agentic-ai/base-app/k8s.yaml
```

### Kubernetes でのアプリケーションのテスト

以下のコマンドを実行してアプリケーションをテストします：

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
