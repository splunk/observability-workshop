---
title: ITSIでのアラート作成
linkTitle: 4. ITSIでのアラート作成
weight: 1
---

# Splunk ITSIでの基本的なアラート設定

このセクションでは、Splunk IT Service Intelligence（ITSI）で基本的なアラートを設定する方法を説明します。以前作成したサービスがKPIの閾値を超えた場合にトリガーされるアラートを設定します。

**作成したサービスに応じて、このアラートに使用するKPIが変わります。以下の手順では、サービス名とKPIを適切に置き換えてください**

* **PaymentService2:** Business Workflow Error Rate
* **AD-Ecommerce2:** Availability

**手順**

1. **KPIに移動します**
   * ITSIで「Configuration」->「Correlation Searches」に移動します
   * 「Create New Search」をクリックします

2. **新しい検索を設定します**
   * **Search Title:** *Service Name* *KPI* Critical
   * **Description:** *Service Name* *KPI* Critical
   * **Search:**

   ```
   index=itsi_summary kpi="*KPI*" alert_severity=critical
   ```

    * **Time Range:** Last 15 minutes
    * **Service:** *Service Name*
    * **Entity Lookup Field:** itsi_service_id
    * **Run Every:** minutes
    * **Notable Event Title:** *Service Name* *KPI* Critical
    * **Severity:** Critical
    * **Notable Event Identified Fields:** source

**アラート作成後**

* アラートが実行されるまで5〜10分待つ必要があります
* アラートはITSIの「Alerts and Episodes」ペインに表示されます

![show-entry](../images/alerts.png?classes=inline)

**重要な考慮事項**

* **アラート疲れ:** アラートを多く設定しすぎたり、閾値を過度に敏感に設定したりすることは避けてください。アラート疲れにつながり、重要な問題を見逃す可能性があります。
