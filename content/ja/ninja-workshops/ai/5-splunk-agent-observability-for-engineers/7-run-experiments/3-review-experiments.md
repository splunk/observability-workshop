---
title: 実験結果の確認
linkTitle: 3. 実験結果の確認
weight: 3
time: 5 minutes
---

{{% notice style="warning" title="TODO" %}}
ワークショップで使用する組織を確認してください。
{{% /notice %}}

Galileoコンソールで実験を確認します。行ごとのスコアを検査し、個別のTraceにドリルダウンし、2つの実行を比較します。

{{< exercise title="Galileoで実験を確認する" >}}

{{< step title="Experimentsビューを開く" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

Galileoコンソール（`https://console.multitenant.galileocloud.io`、 **`ORGANIZATION_PLACEHOLDER`** org）で、 **`healthcare-assistant`** プロジェクトを開き、 **Experiments** ビューに移動します。先ほど実行した実験（例: `healthcare-experiment` または `lisinopril-eval`）が表示されます。

<!-- TODO screenshot: Experiments list in the healthcare-assistant project showing the experiment run(s) with aggregate metric columns -->
![Experiments list](../../images/galileo-experiments-list.png?width=750px)

{{< /step >}}

{{< step title="集計メトリクスを確認する" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact metric-panel steps + screenshot once finalized -->

実験を開き、各メトリクスの集計スコアを確認します。Ground Truth Adherence、Prompt Injection、Chunk Attribution Utilization、Context Adherenceの各スコアは、データセット全体でエージェントがどのように動作したかを要約しています。

<!-- TODO screenshot: experiment summary showing aggregate metric scores across the dataset -->
![Experiment aggregate metrics](../../images/galileo-experiment-metrics.png?width=750px)

{{< /step >}}

{{< step title="個別の行にドリルダウンする" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact row-drilldown steps + screenshot once finalized -->

個別の行を選択して、入力、エージェントの生成出力、参照出力、および行ごとのメトリクススコアを確認します。ここから基礎となるTraceを開くと、第4章で探索したものと同じネストされたSpanが表示されます。今回はスコア付きの実験行に紐付けられています。

<!-- TODO screenshot: single experiment row detail showing input, generated output, reference output, per-row metric scores, and a link to the underlying trace -->
![Experiment row detail](../../images/galileo-experiment-row-detail.png?width=750px)

{{< /step >}}

{{< step title="2つの実行を比較する" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact comparison steps + screenshot once finalized -->

2つの異なるモデルで実験を実行した場合、実行結果を並べて比較し、各メトリクスでどちらの構成がより高いスコアを得たかを確認します。これが、この章の最初に目指していた客観的な比較です。

<!-- TODO screenshot: side-by-side comparison of two experiment runs (e.g., gpt-4o vs gpt-4o-mini) with metric deltas highlighted -->
![Experiment comparison](../../images/galileo-experiment-comparison.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="リリースゲートとしての実験（CI/CD）" style="info" %}}

実験はコードから実行できるため（`python experiments/run_experiment.py`）、CI/CDパイプラインに直接組み込むことができます。すべてのプルリクエストやプレリリースビルドで実験を実行し、主要なメトリクス（例: *Context Adherence* や *Correctness*）がしきい値を下回った場合に **ビルドを失敗** させます。これにより、「このプロンプト変更は問題ないだろう」という推測が、自動化されたエビデンスベースの品質ゲートに変わり、リグレッションが患者に届くことを未然に防ぎます。

{{% /notice %}}

{{< checkpoint title="知識チェック" >}}

ある行が高い *Prompt Injection* スコアを示しています。これは何を意味し、次にどこを確認しますか？

{{< details summary="回答を表示" >}}
高い *Prompt Injection* スコアは、 **入力** がエージェントの指示を上書きしようとする試みであることを示しています。その行のTraceを開いて、エージェントがどのように対処したか（注入された指示に従ったのか、それともタスクに留まったのか）を確認します。これはまさに、次の章の **agent controls** で防御する種類の動作です。
{{< /details >}}
