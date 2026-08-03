---
title: Signalsの確認
linkTitle: 1. Signalsの確認
weight: 1
time: 5 minutes
---

{{% notice style="warning" title="注意" %}}
このセクションの手順は、ワークショップの講師が実施するのを観察してください。ご自身では実行しないでください。
{{% /notice %}}

ログストリームのSignalsを生成し、プラットフォームに問題のトレンドを表示させます。

{{< exercise title="Signalsの確認" >}}

{{< step title="Signalsの生成" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

Galileoコンソール（`https://console.multitenant.galileocloud.io`、 **`workshop`** org）で、プロジェクト / **`default`** ログストリームを開き、 **Signals** ボタンをクリックします。

![Generate Signals](../../images/sao-generate-signals.png?width=250px)

このログストリーム内のTraceを分析してSignalsを生成するまで、少し時間がかかります。

{{< /step >}}

{{< step title="Signalsの確認" >}}

ログストリームに対していくつかのSignalsが生成されたことが確認できます（具体的なSignalsはログストリームごとに異なります）。

<!-- TODO screenshot: Signals view listing detected failure patterns for the healthcare assistant log stream -->
![Signals overview](../../images/sao-signals-overview.png?width=750px)

{{< /step >}}

{{< step title="Signalを開いてコンテキストを確認する" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact signal-detail steps + screenshot once finalized -->

Signalを選択し、そのアクション可能なコンテキストを確認します。パターンの内容、発生理由、推奨される次のステップが表示されます。

例えば、`Database Metadata Leakage Risk` というSignalをクリックします。

<!-- TODO screenshot: signal detail showing the pattern description, root-cause explanation, and recommended remediation -->
![Signal detail](../../images/sao-signal-detail.png?width=250px)

このSignalは、`get_patient_info` ツールの出力に生のSQLクエリ、データベースソース、テーブル名が含まれており、LLMがこのメタデータをそのまま返した場合にエンドユーザーに漏洩する可能性があることを説明しています。

問題を修正するための推奨アクションとして、ツールの出力からデータベースメタデータ（SQLクエリ、テーブル名、ソース情報）をLLMに返す前に除去することが提案されています。

{{< /step >}}

{{< step title="関連するTraceに移動する" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact pivot steps + screenshot once finalized -->

Signalから、`View Affected Spans in Table` ボタンをクリックすることで、パターンを構成する特定のTraceに移動できます。

<!-- TODO screenshot: a signal expanded to its contributing traces, with one trace opened -->
![Signal to traces](../../images/sao-signal-traces.png?width=750px)

これにより、「繰り返し発生する問題がある」から「その背後にある正確なリクエストはこれだ」まで、数クリックで到達できます。これはまさにSignalsが実現するように設計されたターゲットを絞った修正です。

{{< /step >}}

{{< /exercise >}}

{{% notice title="これが重要な理由" style="info" %}}

Signalsがなければ、この種の分析はエンジニアがインシデント後にTraceを手動で調査することを意味し、数週間かかることもあります。Signalsはそれを数分に短縮し、インシデントになる前に問題を検出します。

{{% /notice %}}

{{< checkpoint title="知識チェック" >}}

Signalsは前の章で有効にしたMetricsをどのように補完しますか？

{{< details summary="ここをクリックして回答を表示" >}}

Metricsは、測定対象として選択した **既知の** 品質次元（例: Context Adherence）をスコアリングします。Signalsは、Metricを作成していない **未知の** 繰り返し発生する障害パターン（計画ループ、ツールエラー、ルーティング障害）を自動的に検出します。両方を組み合わせることで、予想していた問題と予想していなかった問題の両方をカバーできます。

特定のSignalから新しいMetricを作成するオプションもあり、将来同じ問題が再発した際に追跡して適切なアクションを取ることができます。

{{< /details >}}
