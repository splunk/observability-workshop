---
title: Network Event Intelligence with Splunk IT Service Intelligence
linkTitle: Network Event Intelligence
weight: 10
archetype: chapter
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
description: Cisco Catalyst Center と SolarWinds のイベントを Splunk ITSI で相関させ、アラートノイズを削減し、ネットワークインシデントのビジネスへの影響を可視化します。
time: 30 minutes
---

## ようこそ

このハンズオンワークショップは、Network Event Intelligence のユースケースにおける IT Service Intelligence (ITSI) の力を効果的にデモンストレーションし、ポジショニングしたい方を対象に設計されています。参加者は、潜在的なクライアントに響く実世界のシナリオとユースケースに焦点を当てながら、これらのプラットフォームを統合する実践的な経験を得ることができます。このワークショップでは、Cisco Networking ポートフォリオ全体およびサードパーティ監視ソリューションにおける複数のソースの相関に重点を置いており、ソリューションアーキテクトが Splunk による効果的なネットワークイベント相関という重要な顧客課題への対応を自信を持って紹介できるようになります。

## はじめに・概要

今日の複雑な IT 環境において、アプリケーションやサービスのパフォーマンスと可用性を確保することは極めて重要です。このワークショップでは、Cisco Catalyst Center、Solarwinds、Splunk Enterprise、および Splunk IT Service Intelligence (ITSI) を含む強力なツールの組み合わせを紹介します。これらのツールが連携することで、包括的な監視およびアラート機能を提供します。

### 現代のネットワークオブザーバビリティの課題

現代のエンタープライズネットワークは、Cisco Catalyst Center、Meraki、ThousandEyes などの Cisco ソリューションから、SolarWinds、HPE Aruba Networking、Palo Alto Networks などのサードパーティツールまで、拡大し続けるベンダーとプラットフォームの組み合わせにまたがっています。それぞれが独自のフォーマットで、独自のコンソールを通じて、独自のアラートを生成します。ネットワークイベントが発生すると、運用チームは何が起きたのか、どこから始まったのか、どのサービスやユーザーが影響を受けているのかを把握するために、接続されていないツール間を手動で調査しなければなりません。共通の相関レイヤーがなければ、アラートノイズは高くなり、調査は遅くなり、ネットワークインシデントのビジネスへの影響は顧客から問い合わせがあるまで見えないままとなります。

### ソリューション: Network Event Intelligence

包括的な Network Intelligence 戦略には、さまざまなソースからのデータを統合し、それを相関させてアクション可能なインサイトを得ることが必要です。このワークショップでは、Splunk Platform と ITSI がどのように連携してこれを実現するかをデモンストレーションします。

* **Cisco Enterprise Networks:** Catalyst Center、Meraki、ThousandEyes などの Cisco Data Fabric からの主要なデータソースを提供します。

* **Splunk:** ログ分析およびあらゆるソースからのデータ収集・相関のための中央プラットフォームとして機能し、強力な検索、可視化、および相関機能を実現します。Splunk は IT 環境の全体像を提供します。

* **Splunk IT Service Intelligence (ITSI):** 他のすべてのプラットフォームからのデータを相関させることでサービスインテリジェンスを提供します。ITSI では、サービスの定義、依存関係のマッピング、およびサービスの全体的な健全性とパフォーマンスを反映する重要業績評価指標（KPI）の監視が可能です。ITSI は IT の問題による*ビジネスへの影響*を理解するために不可欠です。

## ワークショップの目標

このワークショップを終了すると、以下の設定が完了します:

* Cisco Catalyst Center からのデータを使用して、複数のロケーションからネットワークの健全性を監視する ITSI の設定
* アラートを相関させるための Catalyst Center と Solarwinds の両方からのインバウンド通知の設定
* Catalyst Center と Solarwinds の両方からの通知を使用した相関エピソードの設定
* 劣化したサービスの健全性が正常に戻った際にエピソードが自動的に解決される設定
