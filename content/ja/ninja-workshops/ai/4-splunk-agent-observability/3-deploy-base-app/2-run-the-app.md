---
title: アプリケーションの実行
linkTitle: 2. アプリケーションの実行
weight: 2
time: 5 minutes
---

データベースのロードとシークレットの設定が完了したら、アプリを起動して2つの主要なエージェントパスを試します。

{{< exercise title="アシスタントの実行と試用" >}}

{{< step title="ヘルスケアアシスタントアプリのデプロイ" >}}

以下のコマンドを実行して、ヘルスケアアシスタントアプリをデプロイします。

```bash
cd ~/workshop/healthcare-assistant/1-base-app
kubectl apply -f k8s.yaml
```

アプリケーションのPodが実行中であることを確認します。

{{< tabs id="healthcare-app-monitor" >}}
{{% tab title="Script" %}}

```bash
kubectl get pods -l app=healthcare-assistant
```

{{% /tab %}}
{{% tab title="出力例" %}}

````
NAME                                   READY   STATUS    RESTARTS   AGE
healthcare-assistant-d764fc757-l9fxt   1/1     Running   0          20s
````

{{% /tab %}}
{{< /tabs >}}

EC2インスタンスのIPアドレスとポート81を使用して、ブラウザでヘルスケアアシスタントアプリを開きます。

```text
  External URL: http://98.86.181.9:81
```

![Healthcare assistant home screen](../../images/healthcare-assistant-ui.png?width=750px)

{{< /step >}}

{{< step title="RAGパスを試す" >}}

薬に関する質問のサンプルボタンをクリック（または入力）します。

> What is the dosage and common side effects of Lisinopril?

エージェントが `search_medicine_qa` ツールを呼び出し、pgvectorから一致するチャンクを取得して、根拠に基づいた回答を返します。

![Healthcare assistant home screen](../../images/healthcare-assistant-dosage.png?width=750px)

{{< /step >}}

{{< step title="Text-to-SQLパスを試す" >}}

次に、患者検索の質問をします。

> Can you look up information for patient P001?

エージェントが `get_patient_info` を呼び出し、`healthcare_patient` テーブルに対してSQLを生成し、患者の詳細情報を返します。

![Healthcare assistant home screen](../../images/healthcare-assistant-patient.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="何が足りないか" style="info" %}}

アプリは動作していますが、現時点ではエージェントが何をしたかの **記録がありません**。どのツールが呼び出されたか、何が取得されたか、どれだけのトークンが使用されたか、回答が正しかったかどうかさえ確認できません。もしアシスタントが患者に用量を2倍にするよう伝えたとしても、それを知るのはツールからではなくソーシャルメディアからになるでしょう。次の章でSplunk Agent Observabilityを使ってアプリを計装することで、まさにこのギャップを埋めていきます。

{{% /notice %}}

{{< checkpoint title="理解度チェック" >}}

患者検索の質問をした際、エージェントはどのツールを呼び出し、どのバックエンドにアクセスしますか？

{{< details summary="回答を表示" >}}
エージェントは **`get_patient_info`** を呼び出し、Text-to-SQLを使用してPostgreSQLの **`healthcare_patient`** テーブルに対する `SELECT` クエリを生成し、一致する行を返します。
{{< /details >}}
