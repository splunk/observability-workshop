---
title: アプリに Agent Control を追加する
linkTitle: 1. アプリに Agent Control を追加する
weight: 1
time: 8 minutes
---

まず、Agent Control SDKをアプリに組み込みます。設定の追加、パッケージのインストール、制御可能なステップの登録を行います。

{{< exercise title="Agent Control の追加" >}}

{{< step title="環境のセットアップ" >}}

agent controlsフォルダに移動します

```bash
cd ~/workshop/healthcare-assistant/4-app-with-controls
```

{{< /step >}}

{{< step title="Galileo Agent Controls Config Map の作成" >}}

以下のコマンドを実行してKubernetes config mapを作成します。アプリケーションはこれを使用してGalileo Agent Controlsを設定します。

```bash
kubectl create configmap galileo-agent-control-config \
  --from-literal=GALILEO_API_URL="https://api.multitenant.galileocloud.io" \
  --from-literal=AGENT_CONTROL_URL="https://console.multitenant.galileocloud.io/api/agent-control" \
  --from-literal=AGENT_CONTROL_AGENT_NAME="agent-control-example" \
  --from-literal=AGENT_CONTROL_API_KEY_HEADER="Galileo-API-Key" \
  --from-literal=AGENT_CONTROL_RUNTIME_AUTH_MODE="jwt" \
  --from-literal=AGENT_CONTROL_TARGET_TYPE="log_stream"
```

{{% notice title="環境に合わせて変更してください" style="tip" icon="exclamation-triangle" %}}

`GALILEO_API_URL`、`AGENT_CONTROL_URL`、`AGENT_CONTROL_AGENT_NAME` をお使いの環境に合わせて更新してください。ここで設定する `AGENT_CONTROL_AGENT_NAME` は、次のセクションでGalileoコンソールに作成するエージェントと一致する必要があります。

{{% /notice %}}

{{< /step >}}

{{< step title="Agent Control パッケージの追加" >}}

`requirements.txt` にAgent Control SDKとGalileo evaluatorsが含まれていることを確認します。

```text
agent-control-sdk[galileo]>=7.10.0
agent-control-evaluators>=7.10.0
agent-control-evaluator-galileo>=7.10.0
```

{{< /step >}}

{{< step title="インポートの追加とステップのデコレート" >}}

`agent.py` のインポートセクションの末尾に、Agent Controlのインポートを追加しています。

```python
from agent_control import ControlSteerError, ControlViolationError, control
```

controlsステージでは、これらを3箇所で使用しています（このフォルダでは既に設定済み）。

* LLM呼び出しは `@control(step_name=LLM_STEP_NAME)` でラップされています。ここで `LLM_STEP_NAME = "Healthcare Assistant"` とし、モデルの応答を評価、ブロック、またはステアリングできるようにします。
* 各ツールは制御可能なステップとして登録されています（`get_patient_info`、`delete_patient_record`、および検索ツール用の共有 `retrieval_step`）。これは `helpers/agent_control_helpers.py` のヘルパーを通じて行われます。
* エージェントはGalileo loggerでcontrol spanを有効化し（`galileo_logger.enable_agent_control()`）、`init_agent_control(...)` でステップを登録することで、コンソールがこのエージェントにどのステップが存在するかを認識できるようにします。

{{% notice title="ブロックとステアリングのコード上での処理方法" style="info" %}}

controlが発火すると、SDKは例外を発生させ、エージェントがそれをキャッチします。

* `ControlViolationError` → ステップが **ブロック** されます。アクションは停止し、ユーザーにはブロックメッセージが表示されます。
* `ControlSteerError` → ステップが **ステアリング** されます。エージェントはステアリングガイダンスを含めてプロンプトを再構築し、リトライします（最大 `MAX_STEER_RETRIES` 回）。それでも準拠できない場合は、安全なメッセージにフォールバックします。

{{% /notice %}}

{{< /step >}}

{{< step title="新しい Docker Image のビルド" >}}

ベースアプリディレクトリに移動し、以下のコマンドを実行して、最近の変更を含むアプリケーションの新しいDocker imageをビルドします。

```bash
cd ~/workshop/healthcare-assistant
docker build -f 4-app-with-controls/Dockerfile -t localhost:9999/healthcare-assistant:app-with-controls .
docker push localhost:9999/healthcare-assistant:app-with-controls
```

{{% notice title="うまくいかない場合" style="info" %}}

Docker imageのビルドに問題がある場合や、ビルドに時間がかかりすぎる場合は、ビルド済みのdocker imageを代わりに使用できます。`~/workshop/healthcare-assistant/4-app-with-controls/k8s.yaml` ファイルを編集し、imageを `ghcr.io/splunk/healthcare-assistant:app-with-controls` に変更してください。

{{% /notice %}}

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="理解度チェック" >}}

アプリが `ControlViolationError` と `ControlSteerError` を処理する方法の違いは何ですか？

{{< details summary="回答を表示" >}}
`ControlViolationError` はステップを **ブロック** します。アクションは停止し、ユーザーにはブロックメッセージが表示されます。`ControlSteerError` はステップを **ステアリング** します。エージェントはステアリングガイダンスをプロンプトに追加してリトライし（数回まで）、修正された応答を生成しようとします。それでも準拠できない場合にのみ、安全なメッセージにフォールバックします。
{{< /details >}}
