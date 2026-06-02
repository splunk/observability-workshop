---
title: ダッシュボード入門
linkTitle: 1. Dashboards
weight: 1.0
time: 10 minutes
---

## 1. Dashboards

ダッシュボードとは、主要なメトリクスを一箇所に表示するチャートやビジュアライゼーションの集合です。よく設計されたダッシュボードは、システムの健全性とパフォーマンスに関する、迅速で実用的なインサイトを提供します。ダッシュボードは、必要に応じてシンプルにも詳細にもでき、いくつかの焦点を絞ったチャートから、複数のサービスにまたがる複雑なビューまで、さまざまな構成が可能です。

このモジュールでは、いくつかのチャートを作成し、それらをまとめて以下のカスタムダッシュボードを構築します。

![Example Dashboard](../images/example-dashboard.png)

---

## 2. Accessing Dashboards

まず、Splunk Observability suite 内のダッシュボードの場所を確認しましょう。

左側のナビゲーションメニューにある **Dashboards (1)** ボタンをクリックします。メニューが折りたたまれている場合は、画面左上のハンバーガーアイコンをクリックして展開できます。

これにより、メインの Dashboard ビューが表示され、Splunk Observability が提供するビルトインのダッシュボードを含む、利用可能なすべてのダッシュボードが表示されます。

組織が Cloud API インテグレーションや Splunk OpenTelemetry Agent を介して既にデータを取り込んでいる場合は、それらのサービスに関連する追加のダッシュボードも表示されることがあります。

![Sample Data](../images/sample-data.png)
