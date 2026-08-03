---
title: Metricスコアの確認
linkTitle: 2. Metricスコアの確認
weight: 2
time: 5 minutes
---

しばらくすると、既存のトレースが `Context Adherence` と `Correctness` のMetricで自動的にスコアリングされる様子を確認できます。
ここで、ハルシネーションによる誤った用量や不正なツール呼び出しが可視化されます。

{{< exercise title="Metricスコアの確認" >}}

{{< step title="Metricの計算を待つ" >}}

ログトレースを見ると、トレースに対してMetricが計算されていることが確認できます。

![Log stream metrics computing](../../images/sao-metrics-computing.png?width=750px)

{{< /step >}}

{{< step title="ログストリームでスコアを確認する" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

Splunk Agent Observabilityで **`default`** ログストリームに戻り、最近のトレースを確認します。各トレースにはSpanと一緒にMetricスコアが表示されています。

![Metric scores on traces](../../images/sao-metric-scores.png?width=750px)

トレースの1つが `Context Adherence` と `Correctness` の両方で `False` と評価されていることが確認できます。
これは先ほど `Log Hallucination` ボタンを使用して送信したトレースです。

このトレースをクリックして詳しく見てみましょう。

{{< /step >}}

{{< step title="フラグ付きトレースの詳細を確認する" >}}

`LLM Response` Spanをクリックすると、画面の右側に2つの新しいMetricカテゴリが表示されていることに気づきます。`Correctness` Metricを含む `Output Quality` と、`Context Adherence` Metricを含む `RAG Quality` です。

`Context Adherence` Metricの横にある `false` にカーソルを合わせると、このSpanがこのスコアを受けた理由の根拠を確認できます。

この場合、アシスタントが1日100 mgの用量と、発疹、かゆみ、腫れという副作用を回答しており、これがコンテキストと直接矛盾し、裏付けのない情報を追加していると説明されています。

![Flagged trace detail](../../images/sao-metric-flagged-trace.png?width=750px)

この種の検出により、「患者からの苦情があった」という状況が「特定のリクエスト、特定のSpan、そしてそれを検出した特定のMetric」として具体化されます。

{{< /step >}}

{{< step title="Autotune Feedback" >}}

Metricの評価が間違っている場合はどうすればよいでしょうか。

`Add feedback` ボタンをクリックして、任意のMetricにフィードバックを提供できます。

![Add Feedback Button](../../images/sao-add-feedback-button.png?width=750px)

`Corrected value` と `Rationale` を入力します。

![Autotune Feedback](../../images/sao-autotune-feedback.png?width=750px)

この人間によるフィードバックは、Metricが類似のケースを時間の経過とともにより正確に評価できるよう改善に役立ちます。最終的に、スコアリングが実際の基準により適合するようになります。

{{< /step >}}

{{< /exercise >}}

{{% notice title="成果" style="info" %}}

これで、すべてのトラフィックに対する自動品質シグナルが得られました。しかし、Metricは測定しようと考えた問題しか検出できません。次に、**Signals** を使用して、予期していなかった障害パターンを発見します。

{{% /notice %}}

{{< checkpoint title="知識チェック" >}}

ある薬に関する回答が **Context Adherence** で低スコアを記録していますが、検索Spanには正しい情報が取得されたことが示されています。これはどのような問題であり、Careful Health Providerにとってなぜ重要なのでしょうか。

{{< details summary="ここをクリックして回答を確認" >}}
これは **ハルシネーション/グラウンディング** の問題です。正しいコンテキストは利用可能でしたが、モデルの回答がそれに忠実ではありませんでした。医療アシスタントにとってこれは重大なリスクです。「用量を2倍にしてください」といった回答が生まれるのはまさにこのケースであり、後のステップでランタイムガードレールを追加する理由でもあります。
{{< /details >}}
