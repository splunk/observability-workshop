---
title: ワークショップのセットアップ
weight: 99
linkTitle: ワークショップのセットアップ
hidden: true
---

## **Observability ワークショップ セットアップガイドへようこそ**

このガイドでは、Splunk Observability Cloud でワークショップ環境をセットアップするために必要な手順を説明します。事前設定済みの組織を使用する場合でも、トライアルをセットアップする場合でも、このガイドで対応できます。

### **Splunk4Rookies - Observability Cloud ワークショップ プレゼンテーション**

公式のワークショップ プレゼンテーションは [**Cisco Sharepoint**](https://cisco.sharepoint.com/:p:/s/spk_splunkshowcontentrepo/EVOz38iE_mVU5ejCZMOkQE8BN9YSp5VvabMLhPTGUWddpg) で入手できます。このリソースを使用して、ワークショップの参加者に資料を案内してください。

### **提供済み組織（Splunk 社員専用）**

Splunk の社員の場合は、以下の事前設定済み組織を使用して Observability ワークショップを実施できます。これらの組織には、利用可能なすべてのワークショップをサポートするために必要な機能がすべて有効になっています

- **利用可能なワークショップ組織**
  - **[CoE Workshop EMEA (EU0)](https://app.eu0.signalfx.com/#/home/EsGF1sXAEAA)**
  - **[Observability Workshop EMEA (EU0)](https://app.eu0.signalfx.com/#/home/EaJHc4vAEAA)**
  - **[Observability Workshop AMER (US1)](https://app.us1.signalfx.com/#/home/EPNXccRAwAA)**
  - **[APAC-O11y-Workshop (US1)](https://app.us1.signalfx.com/#/home/FA-6LDcA4AA)**

### **ブロックされた組織**

以下の組織は**ブロックされており**、ワークショップの実施には使用できません

- **EU Splunk Show (EU0)**
- **US Splunk Show (US1)**
- **Show Playground (US1)**

### **トライアル組織**

事前設定済みの組織を使用しない場合は、任意の**トライアル組織**にワークショップ環境を作成できます。デフォルトのトライアルでは、月あたり以下のリソースが提供されます

- 25 ホスト
- 25 APM ホスト
- 25 x 10k RUM セッション

### **トライアル組織の制限事項**

以下の機能はトライアル組織ではデフォルトで**利用できず**、有効にする必要があります

- **Synthetic Monitoring**

### **Splunk Cloud/Enterprise の要件**

Splunk Observability Cloud にログを送信するには、**Splunk Cloud** または **Splunk Enterprise** 環境へのアクセスが必要です。以下を確認してください

- Splunk 環境に **splunk4rookies-workshop** という名前のインデックスが存在すること。  
- Log Observer Connect が設定されていること。**Splunk Enterprise** または **Splunk Cloud Platform** を使用している場合は、[**Log Observer Connect のセットアップ手順**](https://help.splunk.com/en/splunk-observability-cloud/manage-data/view-splunk-platform-logs/introduction-to-splunk-log-observer-connect)に従ってください。

### **トライアル組織の設定**

新しいトライアル組織の場合は、[**トライアル組織の設定**](4-org-configuration) セクションに記載されている手順も完了する必要があります。
