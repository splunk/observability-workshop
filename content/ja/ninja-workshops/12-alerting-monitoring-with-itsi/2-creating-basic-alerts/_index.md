---
title: 基本的なアラートの作成
linkTitle: 2. 基本的なアラートの作成
weight: 1
---

# Splunk Enterprise、AppDynamics、および Splunk Observability Cloud での基本的なアラートの設定

このセクションでは、Splunk Enterprise、AppDynamics、およびSplunk Observability Cloudでの基本的なアラートの作成について説明します。これらの例は、シンプルさと核となる概念のデモンストレーションに焦点を当てています。実際のアラートシナリオでは、より複雑な設定としきい値が必要になることが多いことを覚えておいてください。

## 1. Splunk Enterprise アラート

Splunkアラートは、特定の条件に一致する検索結果によってトリガーされます。特定の条件が満たされたときに通知するリアルタイムアラートを作成します。

**シナリオ:** 過去5分間に "main" インデックス内の "Invalid user" イベントの数が100を超えた場合にアラートを発生させます。

**手順:**

1. **検索を作成:** アラートを発生させたいイベントを特定するSplunk検索を作成することから始めます。例えば:

   ```splunk
   index=main "Invalid user"
   ```

    タイムピッカーを使用して "Last 15 minutes" を選択します。

2. **アラートを設定:**
   * **Save As** をクリックし、**Alert** を選択します。
   * アラートにわかりやすい名前を付けます（例: "Numerous Invalid User Logins Attempted"）。
   * **Alert type:**
      * **Scheduled:** 設定されたスケジュールで検索を評価するには **Scheduled** を選択します。Scheduledの下に頻度を選択するボタンがあるので、**Run on Cron Schedule** を選択します。
      * **Cron Expression:** */15* ** *
      * **Triggered when:** **Number of results** **is greater than** **100** を選択します。
      * **Time Range:** "15 minutes" に設定します。
   * **Trigger Actions:**
      * この基本的な例では、**Add to Triggered Alerts** を選択します。実際のシナリオでは、メール通知、Slack統合、またはその他のアクションを設定することになります。
   * **Save:** アラートを保存します。

![show-entry](../images/save_as_alert.png?classes=inline)

**説明:** このアラートは15分ごとに検索を実行し、検索結果が100件を超えるとトリガーされます。**Add to Triggered Alerts** アクションは、単にSplunkのTriggered Alertsリストにアラートを追加します。

**時間範囲と頻度:** Splunkコアのすべては検索であるため、検索の期間と頻度を考慮する必要があります。これにより、a) 期間の重複により同じデータを複数回検索すること、b) 期間と頻度のギャップによりイベントを見逃すこと、c) 頻繁に実行しすぎてオーバーヘッドが増加すること、d) 実行頻度が低すぎてアラートに遅延が発生すること、を防ぐことができます。

## 2. Splunk Observability Cloud アラート (Detectors)

**Detector を作成:**

* 左側のメニューで **Detectors & SLOs** をクリックします
* **Create Detector -> Custom Detector** をクリックします
* Detectorにわかりやすい名前を付けます（例: "High CPU Utilization Alert - INITIALS"）。
* **Signal:**
  * 監視したいメトリクスを選択します ("cpu.utilization")。
  * ホストを指定するために必要なフィルターを追加します (`service.name:otelshop-loadgenerator`)。
  * **Proceed to Alert Condition** をクリックします
* **Condition:**
  * Static Thresholdを選択します
  * しきい値を設定します: **is above** **90**
* **Notifications:**
  * この例では、シンプルな通知方法を選択します（例: テスト用のWebhook）。実際のシナリオでは、PagerDuty、Slack、またはその他の通知システムとの統合を設定することになります。
* **Save:** Detectorを保存します。

![show-entry](../images/detector_preview.png?classes=inline)

**説明:** このDetectorは、指定されたサービスのCPU使用率メトリクスを監視します。CPU使用率が設定された "for" 期間にわたって90% を超えると、Detectorがアラートをトリガーして通知を送信します。

**すべてのプラットフォームに関する重要な考慮事項:**

* **しきい値:** アラートに設定するしきい値を慎重に検討してください。しきい値が敏感すぎるとアラート疲れにつながる可能性があり、しきい値が高すぎると重大な問題を見逃す可能性があります。
* **通知チャネル:** アラートシステムを適切な通知チャネル（メール、SMS、Slack、PagerDuty）と統合して、アラートが適切な人に適切なタイミングで配信されるようにしてください。
* **アラートのグループ化と相関:** 複雑なシステムでは、ノイズを減らし、実用的なインサイトに焦点を当てるために、アラートのグループ化と相関を実装してください。ITSIはこれにおいて重要な役割を果たします。
* **ドキュメント:** アラートをトリガーする条件と適切な対応手順を含め、アラートを明確に文書化してください。

これらの例は、基本的なアラートを作成するための出発点を提供します。これらのプラットフォームに慣れてきたら、特定の監視ニーズに合わせて、より高度なアラート機能と設定を探索することができます。
