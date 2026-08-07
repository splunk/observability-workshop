---
title: セットアップと設定
linkTitle: 1. セットアップと設定
weight: 1
time: 10 minutes
---

この章では `1-base-app` フォルダで作業します。以下の手順でPython環境の作成、シークレットの設定、データベースの起動、エージェントが必要とするサンプルデータの読み込みを行います。

{{< exercise title="ベースアプリケーションのセットアップ" >}}

{{< step title="ラボインスタンスにログイン" >}}

ワークショップのEC2インスタンスに接続します（接続情報はインストラクターから提供されます）。
ヘルスケアアシスタントは `~/workshop/healthcare-assistant/` に事前にロードされており、`OPENAI_API_KEY` は環境に設定済みです。

{{< /step >}}

{{< step title="Kubernetes Secretの作成" >}}

以下のコマンドを実行してKubernetes Secretを作成します。アプリケーションはこれを使用してOpenAIモデルに接続します。

```bash
kubectl create secret generic openai-api \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  --from-literal=openai-api-endpoint="$OPENAI_BASE_URL"
```

{{< /step >}}

{{< step title="Kubernetes Config Mapの作成" >}}

以下のコマンドを実行してKubernetes Config Mapを作成します。アプリケーションが使用する追加の設定パラメータが格納されます。

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f healthcare-assistant-config.yaml
```

{{< /step >}}

{{< step title="PostgreSQLデータベースの起動" >}}

ヘルスケアアシスタントは、薬のFAQエンベディングと患者レコードを `pgvector` 拡張機能付きのPostgreSQLに保存します。以下のコマンドでKubernetes上にPostgreSQLを起動します。

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f postgres.yaml
```

PostgreSQLが実行中であることを確認します。

{{< tabs id="postgres-check" >}}
{{% tab title="スクリプト" %}}

```bash
kubectl get pods -l app=postgres
```

{{% /tab %}}
{{% tab title="出力例" %}}

```bash
NAME                        READY   STATUS    RESTARTS   AGE
postgres-66ffcf4b8c-8s5lp   1/1     Running   0          16s
```

{{% /tab %}}
{{< /tabs >}}

{{< /step >}}

{{< step title="Dockerイメージのビルド" >}}

ベースアプリディレクトリに移動し、以下のコマンドを実行してアプリケーションのDockerイメージをビルドします。

```bash
cd ~/workshop/healthcare-assistant
docker build -f 1-base-app/Dockerfile -t localhost:9999/healthcare-assistant:base-app .
docker push localhost:9999/healthcare-assistant:base-app
```

{{% notice title="ヒント" style="info" %}}

Dockerイメージのビルドに問題がある場合、またはビルドに5分以上かかる場合は、ビルド済みのDockerイメージを使用できます。その場合は、`~/workshop/healthcare-assistant/1-base-app/k8s.yaml` ファイルを編集し、イメージを `ghcr.io/splunk/healthcare-assistant:base-app` に変更してください。

{{% /notice %}}

{{< /step >}}

{{< step title="ベクトルデータとリレーショナルテーブルの読み込み" >}}

薬のFAQをpgvectorにエンベディングし、患者レジストリをPostgreSQLに読み込みます。ヘルパースクリプトが両方を実行します。

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f setup-job.yaml 
```

これにより `python helpers/setup_vectordb.py local` が実行され、`docs/qa.csv` から `healthcare_local_index` pgvectorコレクションが作成され、`docs/relational_patient.csv` から `healthcare_patient` テーブルが作成されます。

以下のコマンドでジョブを監視します（ジョブの開始まで30〜60秒かかる場合があります）。

{{< tabs id="vectordb-monitor" >}}
{{% tab title="スクリプト" %}}

```bash
kubectl logs -f job/vectordb-setup
```

{{% /tab %}}
{{% tab title="出力例" %}}

````
Setting up vector database for healthcare in hosted environment
🔧 Environment setup complete
Using chunk_size: 1000, chunk_overlap: 200
Using embedding model: text-embedding-3-large
Creating PostgreSQL/pgvector collection: healthcare_hosted_index
Adding documents to vector store...
Loading relational tables for healthcare...
✓ Loaded relational table healthcare_patient (30 rows) from relational_patient.csv
✅ Successfully created vector database for healthcare
📊 Total documents embedded: 15
🔗 PostgreSQL collection: healthcare_hosted_index
````

{{% /tab %}}
{{< /tabs >}}

{{< /step >}}

{{< /exercise >}}
