---
title: 2. Splunk Show の利用
weight: 2
---

## **Observability Workshop テンプレート**

Splunk Show では Observability ワークショップ向けに 2 種類のテンプレートを提供しています。ニーズに最も合うものを選択してください。

| Workshop Type | 説明 | テンプレート | |
| --- | --- | --- | --- |
| **Splunk4Rookies - Observability** | このワークショップテンプレートは初心者向けに設計されています。テンプレートには **OpenTelemetry Collector** と **Online Boutique** アプリケーションが事前にデプロイされています。参加者はブラウザだけでワークショップに参加し、完了することができます。 | [**Rookies**](https://show.splunk.com/template/262/) | ![Rookies](../images/rookies.png) |
| **Splunk4Ninjas - Observability** | このワークショップテンプレートは **上級者** 向けに用意されています。テンプレートではハンズオン活動に必要なすべてのツールを備えたインスタンスがセットアップされます。起動時にはリソースはデプロイ・実行されておらず、参加者が必要に応じて構成・デプロイできるようになっています。 | [**Ninja**](https://show.splunk.com/template/428/) | ![Ninjas](../images/ninjas.png) |

{{% notice  style="primary" title="**Ninja Workshops のみ**" icon="user-ninja" %}}

**Estimated Participants** を見込み参加者数に設定し、**O11y Shop Quantity** フィールドにも同じ値を設定してください。

{{% /notice %}}

> [!TIP]
> **ヒント:** 直前の参加者にも対応できるよう、**10% ～ 20%** 多めにプロビジョニングしてください。

---

### **重要な構成のヒント**

インスタンスをプロビジョニングする際は、次の点に留意してください。

1. **Operating Hours**
   - **Operating hours** を **Run always (24/7)** に設定してください。
   - これによりインスタンスがサスペンドされるのを防ぎます。サスペンドされると新しい IP アドレスが割り当てられ、RUM や Synthetics の構成が壊れる可能性があります。

2. **DNS Name**
   - インスタンスに **DNS name** を割り当ててください。
   - これにより、ワークショップ中に Splunk Observability Cloud で環境を見つけて管理しやすくなります。

3. **Splunk Observability Cloud Realm と SWiPE ID**
   - Splunk Observability Cloud の **Realm** を選択してください。
   - ワークショップ用に生成された **SWiPE ID** を入力してください。

4. 適切なイベントタイプを選択してください: **Normal Workshop**、**Private Event**、または **Public Event**。

---

### **追加のリソース**

Splunk Show の利用に関するより詳細なガイダンスは、[**Splunk Show User Guide**](http://go/show/user-guide) を参照してください。
