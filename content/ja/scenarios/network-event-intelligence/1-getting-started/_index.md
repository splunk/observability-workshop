---
title: はじめに
linkTitle: 1. はじめに
weight: 1
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## ワークショップへのアクセス

このワークショップの前に、ワークショップインスタンスへのアクセス情報が提供されているはずです。このワークショップでは、Splunk Enterprise と IT Service Intelligence が含まれる事前構成済みの環境を使用します。インスタンスへのリンクと認証情報は、Splunk Show のインスタンス詳細で確認できます。

このワークショップを完了するために必要なすべてのデータは `netops` インデックスで利用できます。このインデックスには、**Catalyst Center**、**Merkai**、および **Solarwinds** からのアラートのデータが含まれています。

自動化された障害シナリオが30分サイクルで実行されます。Catalyst Center のサイトは15分間正常に動作し、その後15分間パフォーマンスが低下します。環境が異常な状態の間、**Catalyst Center** と **Solarwinds** から Issue とアラートが生成されます。

このワークショップの大部分は IT Service Intelligence で完了します。特に記載がない限り、ナビゲーション手順はそこから開始します。

<div style="max-width: 80%; margin: 0 auto;">
{{% notice style="primary" title="ワークショップインスタンスへのアクセス" %}}
<div style="max-width: 80%; margin: 0 auto;">

**1.** Splunk Show のワークショップ詳細に記載されている URL と認証情報を使用して、Splunk インスタンスにログインします。

**2.** **Apps -> IT Service Intelligence** に移動します。

ITSI を初めて開くときは、Getting Started モーダルを閉じる必要がある場合があります（もちろん、重要な情報をすべて読んだ後に）。
</div>

![ITSI Getting Started Modal](../images/getting-strarted-modal.png?width=30vw)
{{% / notice %}}
</div>

## データの取り込み

このワークショップでは一貫したシナリオを提供するために datagen を使用していますが、実際の環境では、このワークショップで扱うユースケースを実装するために以下の Splunk App とアドオンが必要です。

### 1. [Cisco Catalyst Add-on for Splunk](https://splunkbase.splunk.com/app/7538)

_Cisco Catalyst Add-on for Splunk は、さまざまな Cisco 製品（Cisco Identity Services Engine、Cisco SD-WAN、Cisco Catalyst Center、Cisco Cyber Vision）のデータを収集します。このアドオンは、これらのソースからのデータを解析し、Splunk インデックスに格納します。_

### 2. [Splunk App for Content Packs](https://splunkbase.splunk.com/app/5391)

_Splunk App for Content Packs には、IT Service Intelligence (ITSI) 環境の迅速なセットアップに役立つパッケージ済みコンテンツが含まれています。このパッケージ済みコンテンツは、KPI Base searches、ITSI Glass Tables、テンプレート、その他のオブジェクトで構成されています。_

{{% notice style="info" %}}
このワークショップでは、**Content Pack for Cisco Enterprise Networks** を使用します。これにより、**Cisco Catalyst Add-on for Splunk** が提供するトポロジー情報を使用して、サービスを自動的にインポートできます。
{{% / notice %}}

### 3. [SolarWinds Add-on for Splunk](https://splunkbase.splunk.com/app/3584)（オプション）

_SolarWinds Add-on for Splunk は、SolarWinds のアラートと SolarWinds の資産インベントリ（ネットワークデバイスとそのさまざまな属性）を収集します。このアドオンには、任意の SolarWinds クエリをスケジュールし、対応する出力を Splunk にインデックス化できる汎用入力も含まれています。
その後、データを直接分析したり、Splunk プラットフォーム内の他のアプリケーションパフォーマンス関連データと相関させるためのコンテキストデータフィードとして使用したりできます。_

{{% notice style="info" %}}
このアドオンは、このワークショップで扱うユースケースではオプションです。SolarWinds のアラートは Splunk HTTP Event Collector に直接送信されるため、アドオンは必要ありません。実際のシナリオでは、アドオンは資産インベントリ情報を使用して追加のコンテキストとデータエンリッチメントを提供できます。
{{% / notice %}}

## その他の App/アドオン

### 1. [Cisco Meraki Add-on for Splunk](https://splunkbase.splunk.com/app/5580)

_Splunk Add-on for Cisco Meraki は、Meraki 組織全体にわたる包括的なネットワーク可観測性とセキュリティ監視を提供します。このアドオンは、Cisco Meraki REST API と Webhook を通じて豊富なデータを収集し、ネットワークパフォーマンス、セキュリティ、デバイスの正常性に関するインサイトを提供します。データの探索やカスタムダッシュボードの作成に役立つサンプルビジュアライゼーションも提供されています。_

{{% notice style="info" %}}
このワークショップでは Cisco Meraki は扱いませんが、`netops` インデックスには **Cisco Meraki Add-on for Splunk** を使用して収集される Cisco Meraki データが含まれています。
{{% / notice %}}

### 2. [Cisco Enterprise Networking for Splunk Platform](https://splunkbase.splunk.com/app/7539)

_Cisco Enterprise Networking for Splunk Platform は、さまざまな Cisco 製品（Cisco Identity Services Engine、Cisco SD-WAN、Cisco Catalyst Center、Cisco Cyber Vision、Cisco Meraki、Cisco ThousandEyes）のダッシュボードにビジュアライゼーションを提供します。_
この App は以下によって収集されたデータを使用します

* _Cisco Catalyst Add-on for Splunk_
* _Cisco Catalyst Enhanced Netflow Add-on for Splunk_
* _Cisco Meraki Add-on for Splunk_
* _Cisco ThousandEyes App for Splunk_

![Cisco Enterprise Networking App](../images/cisco-ent-network-overview.png?width=30vw)

</div>
</div>
