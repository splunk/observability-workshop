---
title: アラートとモニタリング
linkTitle: アラートとモニタリング
weight: 2
archetype: chapter
authors: ["Doug Erkkila"]
time: 90 minutes
description: Splunk Enterprise、AppDynamics、Observability Cloud、ITSIを組み合わせたエンドツーエンドのアラートとサービスレベルモニタリング — 基本的なアラートからDetectorドリブンのITSIエピソードまで。
hidden: false
aliases:
  - /ninja-workshops/12-alerting-monitoring-with-itsi/
product: "ITSI"
---

## ワークショップ: Splunk IT Service Intelligenceによるモニタリングとアラート

このハンズオンワークショップは、Splunk Enterprise、AppDynamics、Splunk Observability Cloud、およびSplunk IT Service Intelligence（ITSI）の組み合わせによる強力な機能を効果的にデモンストレーションし、ポジショニングしたい方を対象としています。参加者は、潜在的なクライアントに響く実際のシナリオやユースケースに焦点を当て、これらのプラットフォームを統合する実践的な経験を積むことができます。このワークショップでは、技術的な機能をビジネス価値に変換することに重点を置き、ソリューションアーキテクトがこれらのソリューションが重要な顧客課題にどのように対応するかを自信を持って紹介できるようにします。

### はじめに

今日の複雑なIT環境では、アプリケーションとサービスのパフォーマンスと可用性を確保することが最も重要です。このワークショップでは、包括的なモニタリングとアラート機能を提供するために連携する強力なツールの組み合わせ — Splunk、AppDynamics、Splunk Observability Cloud、およびSplunk IT Service Intelligence（ITSI） — を紹介します。

### 現代のモニタリングにおける課題

現代のアプリケーションは、分散アーキテクチャ、マイクロサービス、クラウドインフラストラクチャに依存していることが多くあります。この複雑さにより、パフォーマンス問題や障害の根本原因を特定することが困難になっています。従来のモニタリングツールは個々のコンポーネントに焦点を当てることが多く、サービス全体の正常性とパフォーマンスの把握にギャップが生じます。

### ソリューション: 統合オブザーバビリティ

包括的なオブザーバビリティ戦略には、さまざまなソースからのデータを統合し、相関分析を行って実用的なインサイトを得ることが必要です。このワークショップでは、Splunk、AppDynamics、Splunk Observability Cloud、およびITSIがどのように連携してこれを実現するかを示します。

* **AppDynamics:** 深いApplication Performance Monitoring（APM）を提供します。アプリケーションを計装して、トランザクショントレース、コードレベルの診断、ユーザーエクスペリエンスデータを含む詳細なパフォーマンスメトリクスをキャプチャします。AppDynamicsは、アプリケーション *内部* のパフォーマンスボトルネックの特定に優れています。

* **Splunk Observability Cloud:** インフラストラクチャメトリクス、分散トレース、ログを包括するフルスタックオブザーバビリティを提供します。サーバーやコンテナからクラウドサービスやカスタムアプリケーションまで、インフラストラクチャ全体の正常性とパフォーマンスの統一されたビューを提供します。Splunk Observability Cloudは、スタック全体にわたるパフォーマンス問題の相関分析を支援します。

* **Splunk:** ログ分析、セキュリティ情報およびイベント管理（SIEM）、より広範なデータ分析のための中央プラットフォームとして機能します。AppDynamics、Splunk Observability Cloud、およびその他のソースからデータを取り込み、強力な検索、可視化、相関分析機能を実現します。SplunkはIT環境の全体的なビューを提供します。

* **Splunk IT Service Intelligence（ITSI）:** すべてのプラットフォームからのデータを相関分析することで、サービスインテリジェンスを提供します。ITSIでは、サービスの定義、依存関係のマッピング、サービス全体の正常性とパフォーマンスを反映するKey Performance Indicator（KPI）のモニタリングが可能です。ITSIは、IT問題の *ビジネスへの影響* を理解するために不可欠です。

## ワークショップの目標

このワークショップを終了すると、参加者は以下のことができるようになります。

* 包括的なオブザーバビリティ戦略における、Splunk、AppDynamics、Splunk Observability Cloud、およびSplunk IT Service Intelligenceの補完的な価値提案を明確に説明する。
* これらのプラットフォーム間の統合ポイントを自信を持ってデモンストレーションし、データフローと相関分析機能を強調する。
* Splunk Enterprise、AppDynamics、およびSplunk Observability Cloudで基本的なアラートを作成・設定し、実践的なアラートシナリオを紹介する。
* Splunk ITSIでのKey Performance Indicator（KPI）の作成とアラートの説得力あるデモンストレーションを構築・提示し、サービス中心のモニタリングを強調する。
* インシデント管理の改善とMTTR短縮のための、Splunk ITSIにおけるエピソードの価値を説明しデモンストレーションする。
* 技術的な機能をビジネス成果に変換し、ROIと特定の顧客ペインポイントへの対応に焦点を当てる。
