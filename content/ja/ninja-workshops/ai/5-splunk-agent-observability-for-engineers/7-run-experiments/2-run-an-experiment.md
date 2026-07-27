---
title: 実験の実行
linkTitle: 2. 実験の実行
weight: 2
time: 5 minutes
---

データセットがアップロードされたら、実験を実行します。各行について、スクリプトは `input` を `HealthcareAgent` に送信し、レスポンスを収集して、デフォルトのメトリクスでスコアリングします。

{{< exercise title="Galileo実験の実行" >}}

{{< step title="デフォルト設定で実行" >}}

`3-app-with-experiments` から、先ほど作成したデータセットに対して実験を実行します。

```bash
python experiments/run_experiment.py
```

スクリプトは、検出したデータセット、適用するメトリクス、各行の処理進捗を表示します。完了すると、完了した実験のリンクとサマリーが表示されます。

{{< /step >}}

{{< step title="カスタム名とモデルで実行" >}}

設定を比較するために、実行にわかりやすい名前を付け、モデルをオーバーライドします。モデルごとに1つずつ、2つの実験を実行すると、コンソールで並べて比較できます。

```bash
python experiments/run_experiment.py --experiment-name "lisinopril-eval" --model gpt-4o-mini
```

{{< /step >}}

{{< /exercise >}}

{{% notice title="デフォルトメトリクス" style="info" %}}

各実験は、以下のGalileo組み込みメトリクスでレスポンスをスコアリングします。

* **Ground Truth Adherence**: レスポンスが参照 `output` にどれだけ一致しているか。
* **Prompt Injection**: 入力がエージェントの指示を覆そうとしていないか。
* **Chunk Attribution Utilization**: 取得したチャンクが実際に回答でどの程度使用されたか。
* **Context Adherence**: 回答が提供されたコンテキストに基づいているか。

{{% /notice %}}

{{% notice title="実験とトレーシングの関係" style="info" %}}

実験ランナーは、チャットアプリと **同じ `HealthcareAgent`** を再利用します。実験トレースコンテキストが提供されると、エージェントはLangGraphのSpanを別のログストリームトレースではなく実験トレースの下にネストするため、スコアリングされた各行は完全なSpanツリーを保持します。

{{% /notice %}}

{{< checkpoint title="理解度チェック" >}}

`--model gpt-4o-mini` と `--model gpt-4o` で実験を2回実行し、データセットは同じものを使用します。これにより何がわかりますか？

{{< details summary="回答を表示" >}}
両方の実行で **入力とメトリクスが同一** であるため、スコアの差は **モデルの変更** に起因すると判断できます。これが実験の目的です。テストしている1つの変数以外のすべてを一定に保つことです。
{{< /details >}}
