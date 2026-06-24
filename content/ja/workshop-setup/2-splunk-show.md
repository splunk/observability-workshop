---
title: Splunk Show の使用方法
weight: 2
time: false
---

## **Observability Workshop テンプレート**

Splunk Show では、Observability ワークショップ向けに2つのテンプレートを提供しています。ニーズに最適なものを選択してください

| ワークショップタイプ | 説明 | テンプレート | |
| --- | --- | --- | --- |
| **Splunk4Rookies - Observability** | このワークショップテンプレートは初心者向けに設計されています。テンプレートは **OpenTelemetry Collector** と **Online Boutique** アプリケーションを事前にデプロイします。参加者はブラウザのみでワークショップに参加し、完了することができます。 | [**Rookies**](https://show.splunk.com/template/262/) | ![Rookies](../images/rookies.png) |
| **Splunk4Ninjas - Observability** | このワークショップテンプレートは**上級**ユーザー向けに設計されています。テンプレートはハンズオン活動に必要なすべてのツールを備えたインスタンスをセットアップします。起動時にはリソースがデプロイまたは実行されていないため、参加者は必要に応じて設定とデプロイを行うことができます。 | [**Ninja**](https://show.splunk.com/template/428/) | ![Ninjas](../images/ninjas.png) |

{{% notice  style="primary" title="**Ninja Workshops のみ**" icon="user-ninja" %}}

**Estimated Participants** を予想される参加者数に設定し、**O11y Shop Quantity** フィールドにも同じ値を入力してください。  

{{% /notice %}}

> [!TIP]
> 直前の参加者に対応するため、**10% - 20%** 多めにプロビジョニングしてください。  

---

### **重要な設定のヒント**

インスタンスをプロビジョニングする際は、以下の点に注意してください

1. **Operating Hours**
   - **Operating hours** を **Run always (24/7)** に設定してください。
   - これにより、インスタンスが一時停止されることを防ぎます。一時停止されると新しい IP アドレスが割り当てられ、RUM と Synthetics の設定が壊れる可能性があります。

2. **DNS Name**
   - インスタンスに **DNS name** を割り当ててください。
   - これにより、ワークショップ中に Splunk Observability Cloud で環境を見つけて管理しやすくなります。

3. **Splunk Observability Cloud Realm と SWiPE ID**
   - Splunk Observability Cloud の **Realm** を選択してください。
   - ワークショップ用に生成された **SWiPE ID** を入力してください。

4. 適切なイベントタイプを選択してください**Normal Workshop**、**Private Event**、または **Public Event**。

---

### **追加リソース**

Splunk Show の使用方法に関する詳細なガイダンスについては、[**Splunk Show User Guide**](https://splunk.show/userguide) を参照してください。
