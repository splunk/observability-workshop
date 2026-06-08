---
title: ログの中から針を見つける
linkTitle: 6. ログの中から針を見つける
weight: 6
archetype: chapter
time: 45 minutes
description: ログのみを出発点としてインシデントをトリアージします — フィルタリング、グループ化、パターンの発見を通じて根本原因を特定します。
params:
  images:
    - images/lo.png
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは**オンコールの SRE** で、Astronomy Shop アプリケーションのエラー率増加に関するアラートを受信しました。ログを主な出発点として調査を行うことが課題です — トレースもメトリクスダッシュボードもありません。ログだけです。

> [!splunk] **Log Observer** は、ログデータを探索・分析するための Splunk Observability Cloud のノーコードインターフェースです。このモジュールでは、APM や RUM から到達するのではなく、ログから直接調査を開始するスタンドアロンの調査ツールとしての使い方を学びます。

{{% /notice %}}

このモジュールには2つのシナリオが含まれています

- **シナリオ 1: ログファーストトリアージ** — Log Observer から調査を開始するインシデント調査の完全なウォークスルー
- **シナリオ 2: TBD** — 2番目の調査シナリオ（開発中）

<!-- TODO screenshot: Log Observer hero image -->

{{< pager prev="/ja/splunk4rookies/o11y-rookies-26/1-modules/"  prevLabel="レッスン一覧に戻る" >}}
