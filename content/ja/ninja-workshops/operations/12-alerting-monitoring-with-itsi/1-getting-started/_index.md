---
title: Getting Started
linkTitle: 1. Getting Started
weight: 1
---

# Splunk、AppDynamics、Splunk Observability Cloud によるモニタリングとアラート

## はじめにと概要

今日の複雑な IT 環境において、アプリケーションやサービスのパフォーマンスと可用性を確保することは最重要課題です。本ワークショップでは、Splunk、AppDynamics、Splunk Observability Cloud、Splunk IT Service Intelligence (ITSI) という強力なツールの組み合わせをご紹介します。これらが連携することで、包括的なモニタリングとアラートの機能を提供します。

### 現代のモニタリングにおける課題

現代のアプリケーションは、分散アーキテクチャ、マイクロサービス、クラウドインフラストラクチャに依存することが多くなっています。この複雑さにより、パフォーマンス問題や障害の根本原因を特定することが困難になっています。従来のモニタリングツールは個々のコンポーネントに焦点を当てがちで、サービス全体の健全性とパフォーマンスを把握する上で隙間が生じます。

### 解決策: 統合された Observability

包括的な Observability 戦略には、さまざまなソースからのデータを統合し、それらを相関させて実用的なインサイトを得ることが必要です。本ワークショップでは、Splunk、AppDynamics、Splunk Observability Cloud、ITSI がどのように連携してこれを実現するかをご紹介します。

* **Splunk:** ログ分析、セキュリティ情報イベント管理 (SIEM)、より広範なデータ分析のための中心的なプラットフォームとして機能します。AppDynamics、Splunk Observability Cloud、その他のソースからデータを取り込み、強力な検索、可視化、相関分析の機能を提供します。Splunk は IT 環境の全体像を提供します。

* **Splunk Observability Cloud:** インフラストラクチャメトリクス、分散トレース、ログを網羅するフルスタックの Observability を提供します。サーバーやコンテナからクラウドサービス、カスタムアプリケーションまで、インフラストラクチャ全体の健全性とパフォーマンスを統一されたビューで提供します。Splunk Observability Cloud はスタック全体にわたるパフォーマンス問題の相関分析を支援します。

* **AppDynamics:** 深い Application Performance Monitoring (APM) を提供します。アプリケーションを計装することで、トランザクショントレース、コードレベルの診断、ユーザーエクスペリエンスデータなど、詳細なパフォーマンスメトリクスを収集します。AppDynamics は、アプリケーション *内部* のパフォーマンスのボトルネックを特定することに優れています。

* **Splunk IT Service Intelligence (ITSI):** 他のすべてのプラットフォームからのデータを相関させることで、サービスインテリジェンスを提供します。ITSI を使用すると、サービスを定義し、依存関係をマッピングし、それらのサービスの全体的な健全性とパフォーマンスを反映する Key Performance Indicator (KPI) をモニタリングできます。ITSI は、IT 問題の *ビジネスインパクト* を理解するために不可欠です。

### データフローと統合

理解しておくべき重要な概念は、これらのプラットフォーム間でデータがどのように流れるかです。

1. **Splunk Observability Cloud と AppDynamics がデータを収集:** アプリケーションとインフラストラクチャをモニタリングし、パフォーマンスメトリクスとトレースを収集します。

2. **データが Splunk に送信される:** AppDynamics と Splunk Observability Cloud は Splunk と統合され、収集したデータを Splunk に直接送信されるログとともに転送します。

3. **Splunk がデータを分析しインデックス化:** Splunk はデータを処理して保存し、検索および分析可能にします。

4. **ITSI が Splunk のデータを活用:** ITSI は Splunk のデータを使用してサービスを作成し、KPI を定義し、IT 運用全体の健全性をモニタリングします。

### ワークショップの目的

本ワークショップ終了時には、以下のことができるようになります。

* Splunk、AppDynamics、Splunk Observability Cloud、ITSI の補完的な役割を理解する。
* Splunk、Observability Cloud、AppDynamics で基本的なアラートを作成する。
* ITSI で新しいサービスとシンプルな KPI およびアラートを設定する。
* ITSI における episode の概念を理解する。

本ワークショップは、堅牢な Observability の実践を構築するための基盤を提供します。アラート設定のワークフローに焦点を当て、ご自身の環境でより高度な機能や設定を探求するための準備を整えます。ITSI またはアドオンのインストールおよび設定については扱い**ません**。

事前設定済みの [Splunk Enterprise Cloud](./1-access-cloud-instances/) インスタンスへのアクセス手順は次のとおりです。
