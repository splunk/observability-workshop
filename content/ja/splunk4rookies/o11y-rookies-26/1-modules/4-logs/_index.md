---
title: ログから針を見つけ出す
linkTitle: 6. ログから針を見つけ出す
weight: 6
archetype: chapter
time: 45 minutes
description: ログだけを起点にインシデントをトリアージします。フィルタリング、グループ化、パターンの発見によって根本原因を突き止めます。
params:
  images:
    - images/lo.png
---

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは **SRE on-call** であり、Astronomy Shop アプリケーションでエラー率が増加しているというアラートを受け取りました。トレースもメトリクスダッシュボードも使わず、ログだけを主要な起点として調査することがタスクです。使うのはログのみです。

> [!splunk] **Log Observer** は、ログデータを探索・分析するための Splunk Observability Cloud のノーコードインターフェースです。本モジュールでは、APM や RUM から遷移してくるのではなく、ログから直接調査を始めるスタンドアロンの調査ツールとして使う方法を学びます。

{{% /notice %}}

このモジュールには2つのシナリオが含まれています:

- **Scenario 1: Log-First Triage** — Log Observer を起点にインシデントを調査するフルウォークスルー
- **Scenario 2: TBD** — もう1つの調査シナリオ（開発中）

<!-- TODO screenshot: Log Observer hero image -->

{{< pager prev="/ja/splunk4rookies/o11y-rookies-26/1-modules/"  prevLabel="Back to Lessons" >}}
