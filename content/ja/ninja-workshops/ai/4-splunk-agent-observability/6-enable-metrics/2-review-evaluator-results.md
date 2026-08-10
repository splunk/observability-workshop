---
title: Evaluator結果の確認
linkTitle: 2. Evaluator結果の確認
weight: 2
time: 5 minutes
---

しばらくすると、既存のTraceが `Context Adherence` と `Correctness` のEvaluatorで自動的にスコアリングされる様子を確認できます。
これにより、ハルシネーションによる誤った用量や不正なツール呼び出しが見えないままになることを防ぎます。

{{< exercise title="Evaluator結果の確認" >}}

{{< step title="Evaluatorの計算を待つ" >}}

エージェントのTraceを見ると、Traceに対してEvaluatorが計算されていることがわかります。

![Agent stream evaluator computing](../../images/sao-evaluators-computing.png?width=750px)

{{< /step >}}

{{< step title="エージェントストリームでスコアを確認する" >}}

Splunk Agent Observabilityで **`default`** エージェントストリームに戻り、最近のTraceを確認します。各Traceに、Spanと並んでEvaluatorの結果が表示されるようになりました。

![Evaluator results on traces](../../images/sao-evaluator-scores.png?width=750px)

Traceの1つが `Context Adherence` と `Correctness` の両方で `False` と評価されていることがわかります。
これは、先ほど `Log Hallucination` ボタンを使用して送信したTraceです。

このTraceをクリックして詳しく見てみましょう。

{{< /step >}}

{{< step title="フラグ付きTraceの詳細を確認する" >}}

`LLM Response` Spanをクリックすると、画面右側に2つの新しいEvaluatorカテゴリが表示されていることに注目してください。`Correctness` Evaluatorを含む `Output Quality` と、`Context Adherence` Evaluatorを含む `RAG Quality` です。

`Context Adherence` Evaluatorの横にある `false` にカーソルを合わせると、このSpanがこのスコアを受けた理由の根拠を確認できます。

この場合、アシスタントが1日100 mgの用量と、発疹、かゆみ、腫れの副作用を回答しており、これがコンテキストと直接矛盾し、裏付けのない情報を追加していることが説明されています。

![Flagged trace detail](../../images/sao-evaluator-flagged-trace.png?width=750px)

この種の検出により、「患者からの苦情があった」という状況が「具体的なリクエスト、具体的なSpan、そしてそれを検出した具体的なEvaluator」として特定できるようになります。

{{< /step >}}

{{< step title="Autotuneフィードバック" >}}

Evaluatorが評価を間違えた場合はどうすればよいでしょうか。

`Add feedback` ボタンをクリックすることで、任意のEvaluatorにフィードバックを提供できます。

![Add Feedback Button](../../images/sao-add-feedback-button.png?width=750px)

`Corrected value` と `Rationale` を入力します。

![Autotune Feedback](../../images/sao-autotune-feedback.png?width=750px)

この人間によるフィードバックは、Evaluatorが類似のケースを評価する方法を時間の経過とともに改善するのに役立ちます。最終的には、スコアリングが実際の基準により適合するようになります。

{{< /step >}}

{{< /exercise >}}

{{% notice title="成果" style="info" %}}

これで、すべてのトラフィックに対する自動品質シグナルが手に入りました。しかし、Evaluatorは測定しようと考えた問題のみを検出します。次に、 **Signals** を使用して、探していることすら *知らなかった* 障害パターンを浮き彫りにします。

{{% /notice %}}

{{< checkpoint title="知識チェック" >}}

薬の回答が **Context Adherence** で低スコアになったが、検索のSpanでは正しい情報が取得されていた場合、これはどのような問題であり、Careful Health Providerにとってなぜ重要なのでしょうか。

{{< details summary="クリックして回答を表示" >}}
これは **ハルシネーション/グラウンディング** の問題です。正しいコンテキストは利用可能でしたが、モデルの回答がそれに忠実ではありませんでした。医療アシスタントにとってこれはハイリスクです。「用量を倍にしてください」という回答がまさにこのようにして発生するため、後ほどこれに対するランタイムガードレールを追加します。
{{< /details >}}
