---
title: Creating Alerts in ITSI
linkTitle: 4. Creating Alerts in ITSI
weight: 1
---

# Splunk ITSIでの基本アラートの設定

このセクションでは、Splunk IT Service Intelligence (ITSI) で基本的なアラートを設定する手順を説明します。先ほど作成したサービスがKPIのしきい値を超過した際にトリガーされるアラートを設定します。

**作成したサービスによって、このアラートで使用するKPIは異なります。以下の手順では、サービス名とKPIを適宜置き換えてください**

* **PaymentService2:** Business Workflow Error Rate
* **AD-Ecommerce2:** Availability

**手順:**

1. **KPIへ移動:**
   * ITSIで「Configuration」->「Correlation Searches」へ移動します
   * 「Create New Search」をクリックします

2. **新しいサーチを設定:**
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

**アラート作成後:**

* アラートが実行されるまで5〜10分待つ必要があります
* アラートはITSIの「Alerts and Episodes」ペインに表示されます。

![show-entry](../images/alerts.png?classes=inline)

**重要な考慮事項:**

* **アラート疲労:** アラートを過剰に設定したり、しきい値を過度に敏感にしないようにしてください。これによりアラート疲労が生じ、人々がアラートに鈍感になって重要な問題を見逃す可能性があります。
