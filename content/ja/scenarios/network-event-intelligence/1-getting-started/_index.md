---
title: はじめに
linkTitle: 1. はじめに
weight: 1
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---


## ワークショップへのアクセス

このワークショップの前に、ワークショップインスタンスへのアクセス情報が提供されているはずです。このワークショップでは、Splunk Enterprise と IT Service Intelligence が含まれた事前設定済みの環境を使用します。インスタンスへのリンクと認証情報は、Splunk Show のインスタンス詳細で確認できます。

このワークショップを完了するために必要なすべてのデータは `netops` インデックスで利用可能です。このインデックスには、**Catalyst Center**、**Merkai**、および **Solarwinds** からのアラートのデータが含まれています。

自動化された障害シナリオが30分サイクルで実行されます。Catalyst Center のサイトは15分間正常に動作し、その後15分間パフォーマンスが低下します。環境が異常な状態の間、**Catalyst Center** と **Solarwinds** から Issue とアラートが生成されます。

このワークショップの大部分は IT Service Intelligence で完了します。特に記載がない限り、ナビゲーション手順はそこから開始します。

{{% notice style="primary" title="ワークショップインスタンスにアクセスする" %}}

**1.** Splunk Show のワークショップ詳細に記載された URL と認証情報を使用して、Splunk インスタンスにログインします。

**2.** **Apps -> IT Service Intelligence** に移動します。

ITSI を初めて開く際に、Getting Started モーダルを閉じる必要がある場合があります（もちろん、重要な情報をすべて読んでからです）。

![ITSI Getting Started Modal](../images/getting-strarted-modal.png?width=30vw)
{{% / notice %}}

## データの取り込み

このワークショップでは一貫したシナリオを提供するために datagen を使用していますが、実際の環境では、このワークショップで扱うユースケースを実装するために以下の Splunk Apps および Add-on が必要です。

### 1. [Cisco Catalyst Add-on for Splunk](https://splunkbase.splunk.com/app/7538)

_Cisco Catalyst Add-on for Splunk は、さまざまな Cisco 製品（Cisco Identity Services Engine、Cisco SD-WAN、Cisco Catalyst Center、Cisco Cyber Vision）のデータを収集します。この Add-on は、これらのソースからのデータを解析し、Splunk インデックスに保存します。_

### 2. [Splunk App for Content Packs](https://splunkbase.splunk.com/app/5391)

_Splunk App for Content Packs には、IT Service Intelligence (ITSI) 環境の迅速なセットアップに役立つパッケージ済みコンテンツが含まれています。このパッケージ済みコンテンツは、KPI Base searches、ITSI Glass Tables、テンプレート、およびその他のオブジェクトで構成されています。_

{{% notice style="info" %}}
このワークショップでは **Content Pack for Cisco Enterprise Networks** を使用します。これにより、**Cisco Catalyst Add-on for Splunk** が提供するトポロジー情報を使用してサービスを自動的にインポートできます。
{{% / notice %}}

### 3. [SolarWinds Add-on for Splunk](https://splunkbase.splunk.com/app/3584) (Optional)

_SolarWinds Add-on for Splunk は、SolarWinds のアラートと SolarWinds の資産インベントリ（ネットワークデバイスとそのさまざまな属性）を収集します。この Add-on には、任意の SolarWinds クエリをスケジュールし、対応する出力を Splunk にインデックスできる汎用入力も含まれています。
データを直接分析したり、Splunk プラットフォーム内の他のアプリケーションパフォーマンス関連データと相関させるためのコンテキストデータフィードとして使用したりできます。_

{{% notice style="info" %}}
この Add-on は、このワークショップで扱うユースケースではオプションです。SolarWinds のアラートは Splunk HTTP Event Collector に直接送信されるため、Add-on は不要です。実際のシナリオでは、Add-on は資産インベントリ情報を使用して追加のコンテキストやデータエンリッチメントを提供できます。
{{% / notice %}}

## 追加の Apps/Add-on

### 1. [Cisco Meraki Add-on for Splunk](https://splunkbase.splunk.com/app/5580)

_Splunk Add-on for Cisco Meraki は、Meraki 組織全体にわたる包括的なネットワークオブザーバビリティとセキュリティ監視を提供します。この Add-on は、Cisco Meraki REST API と Webhook を介してリッチなデータを収集し、ネットワークパフォーマンス、セキュリティ、およびデバイスの健全性に関するインサイトを提供します。データの探索やカスタムダッシュボードの作成に役立つサンプルビジュアライゼーションも提供されています。_

{{% notice style="info" %}}
Cisco Meraki はこのワークショップでは扱いませんが、`netops` インデックスには **Cisco Meraki Add-on for Splunk** を使用して収集される Cisco Meraki データが利用可能です。
{{% / notice %}}

### 2. [Cisco Enterprise Networking for Splunk Platform](https://splunkbase.splunk.com/app/7539)

_Cisco Enterprise Networking for Splunk Platform は、さまざまな Cisco 製品（Cisco Identity Services Engine、Cisco SD-WAN、Cisco Catalyst Center、Cisco Cyber Vision、Cisco Meraki、Cisco ThousandEyes）のダッシュボードにビジュアライゼーションを表示します。_
この App は以下によって収集されたデータを使用します

* _Cisco Catalyst Add-on for Splunk_
* _Cisco Catalyst Enhanced Netflow Add-on for Splunk_
* _Cisco Meraki Add-on for Splunk_
* _Cisco ThousandEyes App for Splunk_

![Cisco Enterprise Networking App](../images/cisco-ent-network-overview.png?width=30vw)
