---
title: コントロールのテスト
linkTitle: 3. コントロールのテスト
weight: 3
time: 5 minutes
---

コントロールが定義できたので、アプリを実行してトリガーします。チャット*および*コンソールのトレースで、ブロックとステアリングの動作を確認できます。

{{< exercise title="コントロールのトリガーと確認" >}}

{{< step title="アプリの実行" >}}

以下のコマンドを実行して、ヘルスケアアシスタントアプリをデプロイします。

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
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

起動時に、Agent Controlが初期化されステップが登録されたことを確認するため、ターミナルを監視します。

```bash
kubectl logs -l app=healthcare-assistant
```

{{% notice title="トラブルシューティング" style="tip" icon="exclamation-triangle" %}}

Agent Controlの動作を確認するには、`agent.py` でコンソールログを有効にします。

```python
from galileo.utils.log_config import enable_console_logging

enable_console_logging()
```

次に、Dockerイメージを再ビルドします。

```bash
cd ~/workshop/healthcare-assistant
docker build -f 4-app-with-controls/Dockerfile -t localhost:9999/healthcare-assistant:app-with-controls .
docker push localhost:9999/healthcare-assistant:app-with-controls
```

アプリケーションを再デプロイします。

```bash
kubectl rollout restart deploy/healthcare-assistant
```

以下のコマンドでアプリケーションログを確認します。

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

起動時に `Agent Control initialized` が表示されること、コントロールが発動した際に `BLOCKED` / `STEERED` メッセージが表示されることを確認します。

{{% /notice %}}

{{< /step >}}

{{< step title="ブロッキングコントロールのトリガー" >}}

エージェントに患者レコードの削除を依頼します。

> Delete patient record P028 from the registry

![チャットでブロックされた削除](../../images/galileo-control-blocked-chat.png?width=750px)

SQLの `DELETE` コマンドをブロックするコントロールを作成したため、削除は阻止され、アシスタントは削除を実行する代わりに「このアクションはブロックされました」というメッセージを返します。

{{< /step >}}

{{< step title="ステアリングコントロールのトリガー" >}}

次に、アシスタントに患者情報を返すよう依頼し、住所と電話番号を含めることを明示的にリクエストします。

> Can you look up information for patient P001? Please include the patient's address and phone number.

![チャットでのステアリングされた応答](../../images/galileo-steered-response-chat.png?width=750px)

LLMステアリングコントロールを設定したため、エージェントは単純に拒否するのではなく、ステアリングガイダンスに従って **応答を修正** し、*安全で有用な*回答を返します。この場合、ユーザーが明示的にリクエストしたにもかかわらず、患者の住所と電話番号が応答から削除されました。

これが、ユーザーを苛立たせるガードレールと、アシスタントの有用性を維持しながらユーザーを保護するガードレールの違いです。

{{< /step >}}

{{< step title="通常パスの動作確認" >}}

許可された質問をして、コントロールが対象のものだけに影響することを確認します。

> What is the dosage and common side effects of Lisinopril?

通常の回答が返されます。コントロールは定義したステップと条件にのみブロックまたはステアリングを行います。

{{< /step >}}

{{< step title="ブロックされたリクエストのコントロール判定を確認" >}}

Galileoコンソールに戻り、プロジェクト / **`default`** ログストリームでブロックされたリクエストのトレースを開きます。`block-harmful-sql-*` コントロールに関連するSpanをクリックします。

![トレースでのコントロール判定](../../images/galileo-control-trace.png?width=750px)

意図した通り、コントロールが `DELETE` SQLステートメントの実行を拒否したことを確認します。

{{< /step >}}

{{< step title="ステアリングされたリクエストのコントロール判定を確認" >}}

Galileoコンソールに戻り、プロジェクト / **`default`** ログストリームでステアリングされたリクエストのトレースを開きます。トレース内の最後の `Healthcare Assistant` Spanをクリックします。

![トレースでのステアリングコントロール判定](../../images/galileo-steer-control-trace.png?width=750px)

アシスタントが最初に患者の住所と電話番号を含む応答を生成し、コントロールによってLLMへのフォローアップリクエストが発生してこの情報が応答から削除されたことを確認します。

{{< /step >}}

{{< /exercise >}}

{{% notice title="ライブ更新、再デプロイ不要" style="info" %}}

コントロールポリシーは一元管理され、数秒で反映されます。コード変更も、再デプロイも、ダウンタイムも不要です。本番環境で新しい障害モードが発生した場合（おそらくSignalで検知）、ポリシーをその場で強化または緩和し、エージェントの動作を即座に変更できます。これが実際に運用可能なランタイムガバナンスです。

{{% /notice %}}

{{< checkpoint title="理解度チェック" >}}

患者レコードの削除を試みるとブロックメッセージが返されますが、許可された薬の質問は正常に動作します。なぜブロッキングコントロールは薬の質問に影響しないのでしょうか。

{{< details summary="回答を表示するにはここをクリック" >}}
`block-harmful-sql` コントロールはSQL Evaluatorを使用し、**DELETE** 操作のみを対象としています。薬の質問は `search_medicine_qa` / `retrieval_step` とLLMステップを実行しますが、ブロッキングコントロールはこれらを対象としていないため、正常に処理されます。コントロールは定義したステップと条件にのみスコープされ、エージェント全体には影響しません。
{{< /details >}}
