---
title: Agent StreamでEvaluatorを有効にする
linkTitle: 1. Evaluatorの有効化
weight: 1
time: 5 minutes
---

Evaluatorは **agent stream** に設定されるため、新しいTraceが到着するたびに自動的にスコアリングされます。ここでは、ヘルスケアアシスタントに重要な組み込みEvaluatorのセットを有効にします。

{{< exercise title="組み込みEvaluatorを有効にする" >}}

{{< step title="Agent streamの設定を開く" >}}

Galileoコンソール（`https://console.multitenant.galileocloud.io`、**`workshop`** org）でプロジェクトを開き、**`default`** agent streamを選択します。

`Configure Evaluators` ボタンをクリックして、Evaluatorの設定を開きます。

![Agent stream evaluators configuration](../../images/sao-enable-evaluators.png?width=750px)

{{< /step >}}

{{< step title="必要なEvaluatorを有効にする" >}}

agent streamで以下の組み込みEvaluatorを有効にします。

* **Context Adherence**: 回答が取得された医療コンテンツに基づいているか確認します（「用量を2倍にする」タイプのハルシネーションを検出します）
* **Correctness**: 回答が事実として正しいか確認します

![Agent stream enable evaluators](../../images/sao-enable-two-evaluators.png?width=750px)

設定を保存します。これ以降、このagent streamの新しいTraceは自動的にスコアリングされます。

{{< /step >}}

{{< step title="変更を適用する" >}}

`Apply` をクリックして変更を適用します。すでにキャプチャされたTraceに対してEvaluatorを実行するオプションがあります。デフォルトオプションの `Last 1 day` を選択します。

![Compute metrics](../../images/sao-compute-metrics.png?width=350px)

`Compute` ボタンをクリックして、既存のTraceに対してEvaluatorを実行します。

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認問題" >}}

Traceを1つずつスコアリングするのではなく、**agent stream** でEvaluatorを有効にするのはなぜですか？

{{< details summary="ここをクリックして回答を表示" >}}
agent streamのEvaluatorは **すべての新しいTraceに自動的に適用** されるため、手動のスポットチェックではなく、継続的かつスケーラブルな評価が可能になります。Lunaの低コストなスコアリングと組み合わせることで、少数のサンプルではなくすべてのトラフィックを評価できます。
{{< /details >}}
