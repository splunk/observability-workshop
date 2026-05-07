---
title: 1. クエリメトリクスの時系列推移
weight: 1
---

**Query metrics** タブは、選択した時間範囲におけるクエリごとのトレンド（実行回数、平均実行時間、CPU 時間、読み取り行数）をプロットします。**Queries** タブの集計値はクエリが*合計で*何を行ってきたかを示しますが、metrics タブは*それがどのように変化したか*を示します。

これが重要なのは、トレンドを見るまでは2つの問題が同じに見えるからです。

- 「このクエリはずっと遅い」→ インデックスの欠落や初期からの設計上の問題の可能性が高いです。
- 「このクエリは先週まで速かったのに今は遅い」→ データ増加の問題、統計情報の問題、または最近のコード変更の可能性が高いです。

{{% notice title="演習" style="green" icon="running" %}}

- Navigator で **Query metrics** タブをクリックします。
- タイムピッカーでより長い時間範囲（例**Last 24 hours**）を選択し、トレンドが見えるようにします。
- 調査対象のクエリの **Average duration** チャートを確認します。

<!-- TODO screenshot: Query metrics tab showing trend charts for execution count, average duration and CPU time over 24 hours -->
![クエリメトリクス](../images/query-metrics.png)

{{< tabs >}}
{{% tab title="質問" %}}
**クエリの平均実行時間は安定していますか、上昇傾向にありますか、それとも特定の時間帯にスパイクしていますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**上昇傾向は通常、データ増加や統計情報の陳腐化を意味します。特定の時間帯のスパイクは通常、スケジュールジョブとの競合を意味します — 例えば、バックアップや ETL 実行などです。**
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
