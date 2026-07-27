---
title: トラフィックの生成
linkTitle: 3. トラフィックの生成
weight: 3
time: 4 minutes
---

コールバックを接続した状態で、計装済みアプリを実行していくつかのリクエストを送信します。これにより、各ターンでSplunk Agent Observabilityにトレースが生成されます。次の章でこれらのトレースを詳しく確認します。

{{< exercise title="アプリの実行とトレースの生成" >}}

{{< step title="新しいDockerイメージのビルド" >}}

アプリのベースディレクトリに移動し、以下のコマンドを実行して最近の変更を含むアプリケーションの新しいDockerイメージをビルドします。

```bash
cd ~/workshop/healthcare-assistant
docker build -f 2-app-with-instrumentation/Dockerfile -t localhost:9999/healthcare-assistant:app-with-instrumentation .
docker push localhost:9999/healthcare-assistant:app-with-instrumentation
```

{{% notice title="うまくいかない場合" style="info" %}}

Dockerイメージのビルドに問題がある場合、またはビルドに5分以上かかる場合は、ビルド済みのDockerイメージを代わりに使用できます。その場合、`~/workshop/healthcare-assistant/2-app-with-instrumentation/k8s.yaml` ファイルを編集し、イメージを `ghcr.io/splunk/healthcare-assistant:app-with-instrumentation` に変更してください。

{{% /notice %}}

{{< /step >}}

{{< step title="ヘルスケアアシスタントアプリのデプロイ" >}}

以下のコマンドを実行してヘルスケアアシスタントアプリをデプロイします。

```bash
cd ~/workshop/healthcare-assistant/2-app-with-instrumentation
kubectl apply -f k8s.yaml
```

新しいアプリケーションPodが実行中であることを確認します。

{{< tabs id="healthcare-app-monitor" >}}
{{% tab title="Script" %}}

```bash
kubectl get pods -l app=healthcare-assistant
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
NAME                                   READY   STATUS    RESTARTS   AGE
healthcare-assistant-d764fc757-l9fxt   1/1     Running   0          20s
````

{{% /tab %}}
{{< /tabs >}}

EC2インスタンスのIPアドレスとポート81を使用して、ブラウザでヘルスケアアシスタントアプリを開きます。
例:

```text
  External URL: http://98.86.181.9:81
```

{{< /step >}}

{{< step title="リクエストの送信" >}}

RAGトレースとtext-to-SQLトレースの両方を生成するために、両方のツールパスを実行します。

> What is the dosage and common side effects of Lisinopril?

> Can you look up information for patient P001?

各プロンプトは計装前と同じ回答を返します。コールバックはアプリの動作を変更せず、記録するだけです。

{{% notice title="Tip" style="tip" icon="exclamation-triangle" %}}

他の薬について質問したい場合は、以下のドキュメントを参照してください。

```bash
cat ~/workshop/healthcare-assistant/docs/qa.csv
```

{{% /notice %}}

{{< /step >}}

{{< step title="ハルシネーションのトリガー" >}}

次に、アプリケーションの左側にある `Log Hallucination` ボタンをクリックします。これにより、先ほどと同じ質問が送信されます。

> What is the dosage and common side effects of Lisinopril?

しかし今回は、ヘルスケアアシスタントが一般的な投与量を1日100mgと回答します。これは実際の推奨投与量である1日10-40mgよりもはるかに高い値です。

これは不正確で、潜在的に危険な回答であり、必ず把握しておきたい問題です。

{{< /step >}}

{{< step title="アプリケーションログの確認" >}}

以下のコマンドを使用してアプリケーションログを表示します。

```bash
kubectl logs -l app=healthcare-assistant
```

すべてが正常に動作していれば、ログに以下のように表示されます。

````
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

2026-07-07 17:52:39.433 Uvicorn server started on :::8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.42.0.18:8501
  External URL: http://98.92.157.71:8501
````

{{% notice title="Tip" style="tip" icon="exclamation-triangle" %}}

SDKが何を行っているかを正確に確認するには、`agent.py` の先頭付近に以下を一時的に追加します。

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

その後、Dockerイメージを再ビルドします。

```bash
cd ~/workshop/healthcare-assistant
docker build -f 2-app-with-instrumentation/Dockerfile -t localhost:9999/healthcare-assistant:app-with-instrumentation .
docker push localhost:9999/healthcare-assistant:app-with-instrumentation
```

そしてアプリケーションを再デプロイします。

```bash
kubectl rollout restart deploy/healthcare-assistant
```

以下のコマンドを使用してアプリケーションログを表示します。

{{< tabs id="healthcare-app-logs" >}}
{{% tab title="Script" %}}

```bash
kubectl logs -l app=healthcare-assistant
```

{{% /tab %}}
{{% tab title="Example Output" %}}

````
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.42.2.14:8501
  External URL: http://35.175.237.123:8501

INFO - galileo.logger - Ingest service healthy at https://api.multitenant.galileocloud.io, using IngestTraces client
INFO - galileo.logger - Searching for session with external ID: ca0f30ed-9b69-401a-8258-b9c043bdc73a ...
INFO - galileo.logger - Starting a new session...
INFO - galileo.logger - Session started with ID: ec03c538-cf9e-4bed-b97e-4b3c2e46ffbc
````

{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{% notice title="今回実現したこと" style="info" %}}

1つの小さな変更で、ブラックボックスから完全なキャプチャへと移行しました。すべてのプロンプト、レスポンス、ツール呼び出し、検索、トークン数、レイテンシーが各ターンごとに記録されるようになりました。次の章では、このデータを活用してエージェントが何を行ったかを正確に調査します。

{{% /notice %}}

{{< checkpoint title="理解度チェック" >}}

3つのメッセージを送信しました。おおよそいくつのトレースが作成され、何がそれを決定しますか？

{{< details summary="クリックして回答を表示" >}}
**3つのトレース（ユーザーのターンごとに1つ）。** 呼び出しごとに新しいコールバックが接続され、LangGraphのターン全体が単一のルート実行として動作するため、各メッセージがネストされたLLMおよびツールのSpanを含む1つのトレースになります。次のセクションでトレースをより詳しく確認します。
{{< /details >}}
