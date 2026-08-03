---
title: Log Streamでメトリクスを有効にする
linkTitle: 1. Enable Metrics
weight: 1
time: 5 minutes
---

メトリクスは **log stream** で設定されるため、新しいTraceが到着するたびに自動的にスコアリングされます。ここでは、ヘルスケアアシスタントに重要なすぐに使えるメトリクスのセットを有効にします。

{{< exercise title="すぐに使えるメトリクスを有効にする" >}}

{{< step title="Log streamの設定を開く" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

Galileoコンソール（`https://console.multitenant.galileocloud.io`、**`workshop`** org）で、プロジェクトを開き、**`default`** log streamを選択します。

`Configure Evaluators` ボタンをクリックして、Evaluatorsの設定を開きます。

![Log stream evaluators configuration](../../images/sao-enable-metrics.png?width=750px)

{{< /step >}}

{{< step title="重要なメトリクスを有効にする" >}}

log streamで以下のすぐに使えるメトリクスを有効にします。

* **Context Adherence**: 回答は取得された医療コンテンツに基づいていますか？（「用量を倍にする」スタイルのハルシネーションを検出します）
* **Correctness**: 回答は事実として正しいですか？

![Log stream enable metrics](../../images/sao-enable-two-metrics.png?width=750px)

設定を保存します。これ以降、このlog streamの新しいTraceは自動的にスコアリングされます。

{{< /step >}}

{{< step title="変更を適用する" >}}

`Apply` をクリックして変更を適用します。すでにキャプチャされたTraceに対してメトリクスを計算するオプションがあります。デフォルトオプションの `Last 1 day` を選択します。

![Compute metrics](../../images/sao-compute-metrics.png?width=350px)

`Compute` ボタンをクリックして、既存のTraceのメトリクスを計算します。

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認問題" >}}

Traceを1つずつスコアリングするのではなく、なぜ **log stream** でメトリクスを有効にするのですか？

{{< details summary="ここをクリックして回答を表示" >}}
log streamのメトリクスは **すべての新しいTraceに自動的に適用される** ため、手動のスポットチェックではなく、継続的でスケーラブルな評価が可能になります。Lunaの低コストなスコアリングと組み合わせることで、少数のサンプルではなく、すべてのトラフィックを評価できます。
{{< /details >}}
