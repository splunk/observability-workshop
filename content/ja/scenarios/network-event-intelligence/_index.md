---
title: Splunk IT Service Intelligence による Network Event Intelligence
linkTitle: Network Event Intelligence
weight: 10
archetype: chapter
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
description: Cisco Catalyst Center、Solarwinds、Splunk ITSI を統合し、ベンダー横断でネットワークイベントを相関分析することで、アラートノイズを削減し、ネットワークインシデントのビジネスへの影響を把握します。
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## ようこそ

このハンズオンワークショップは、Network Event Intelligence のユースケースにおける IT Service Intelligence (ITSI) の威力を効果的にデモンストレーションし、ポジショニングしたいすべての方を対象に設計されています。参加者は、潜在的なクライアントに響く実際のシナリオやユースケースに焦点を当てながら、これらのプラットフォームを統合する実践的な経験を積むことができます。このワークショップでは、Cisco Networking ポートフォリオ全体およびサードパーティ監視ソリューションにまたがる複数のソースの相関分析を重視しており、ソリューションアーキテクトが、効果的なネットワークイベント相関という顧客の重要な課題に Splunk がどのように対応できるかを自信を持って紹介できるようになります。

## はじめに・概要

今日の複雑な IT 環境において、アプリケーションやサービスのパフォーマンスと可用性を確保することは極めて重要です。このワークショップでは、Cisco Catalyst Center、Solarwinds、Splunk Enterprise、Splunk IT Service Intelligence (ITSI) を含む強力なツールの組み合わせを紹介します。これらのツールが連携することで、包括的な監視およびアラート機能を提供します。

### 現代のネットワークオブザーバビリティにおける課題

現代のエンタープライズネットワークは、Cisco Catalyst Center、Meraki、ThousandEyes などの Cisco ソリューションから、SolarWinds、HPE Aruba Networking、Palo Alto Networks などのサードパーティツールまで、ベンダーやプラットフォームの組み合わせが拡大し続けています。それぞれが独自のフォーマットで、独自のコンソールを通じて、独自のアラートを生成します。ネットワークイベントが発生すると、運用チームは何が起きたのか、どこから始まったのか、どのサービスやユーザーが影響を受けているのかを把握するために、分断されたツール間を手作業で調査しなければなりません。共通の相関レイヤーがなければ、アラートノイズは高く、調査は遅くなり、ネットワークインシデントのビジネスへの影響は、顧客からの問い合わせが入るまで見えないままです。

### ソリューション: Network Event Intelligence

包括的な Network Intelligence 戦略には、さまざまなソースからのデータを統合し、相関分析を行うことで実用的なインサイトを得ることが必要です。このワークショップでは、Splunk Platform と ITSI がどのように連携してこれを実現するかをデモンストレーションします。

* **Cisco Enterprise Networks:** Catalyst Center、Meraki、ThousandEyes などの Cisco Data Fabric からの主要なデータソースを提供します。

* **Splunk:** ログ分析、あらゆるソースからのデータの収集と相関分析の中央プラットフォームとして機能し、強力な検索、可視化、相関分析機能を実現します。Splunk は IT 環境の全体的なビューを提供します。

* **Splunk IT Service Intelligence (ITSI):** 他のすべてのプラットフォームからのデータを相関分析することで、サービスインテリジェンスを提供します。ITSI では、サービスの定義、依存関係のマッピング、サービスの全体的な健全性とパフォーマンスを反映する主要パフォーマンス指標（KPI）の監視が可能です。ITSI は IT の問題がもたらす**ビジネスへの影響**を理解するために不可欠です。

## ワークショップの目標

このワークショップの終了時には、以下の設定が完了します。
* Cisco Catalyst Center のデータを使用して、複数のロケーションからネットワークの健全性を監視する ITSI の設定
* アラートを相関分析するための Catalyst Center と Solarwinds 双方からのインバウンド通知の設定
* Catalyst Center と Solarwinds 双方からの通知を使用した相関エピソードの設定
* 劣化したサービスの健全性が正常に戻った際に自動的に解決するエピソードの設定

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
このワークショップを進めるには、以下の方法が最も簡単です:

* このページの右上にある左右の矢印（**<** | **>**）を使用する
* キーボードの左（◀️）および右（▶️）カーソルキーを使用する
  {{% /notice %}}
  
</div>
