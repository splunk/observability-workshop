---
title: 基本的なアラートの作成
linkTitle: 2. 基本的なアラートの作成
weight: 1
---

# Splunk Enterprise、AppDynamics、Splunk Observability Cloudでの基本的なアラートの設定

このセクションでは、Splunk Enterprise、AppDynamics、Splunk Observability Cloudでの基本的なアラートの作成について説明します。これらの例はシンプルさとコアコンセプトのデモンストレーションに重点を置いています。実際のアラートシナリオでは、より複雑な設定やしきい値が必要になることが多い点に注意してください。

## 1. Splunk Enterpriseアラート

Splunkアラートは、特定の条件に一致する検索結果によってトリガーされます。ここでは、特定の条件が満たされた場合に通知するリアルタイムアラートを作成します。

**シナリオ:** "main"インデックス内の"Invalid user"イベントの数が過去5分間で100を超えた場合にアラートを発行します。

**手順:**

1. **検索の作成:** アラートの対象となるイベントを特定するSplunk検索を作成します。例:

   ```splunk
   index=main "Invalid user"
   ```

    タイムピッカーで"Last 15 minutes"を選択します。

2. **アラートの設定:**
   * "Save As"をクリックし、"Alert"を選択します。
   * アラートにわかりやすい名前を付けます（例: "Numerous Invalid User Logins Attempted"）。
   * **Alert type:**
      * **Scheduled:** "Scheduled"を選択して、設定したスケジュールで検索を評価します。Scheduledの下に頻度を選択するボタンが表示されるので、"Run on Cron Schedule"を選択します。
      * **Cron Expression:** */15* ** *
      * **Triggered when:** "Number of results" "is greater than" "100"を選択します。
      * **Time Range:** "15 minutes"に設定します。
   * **Trigger Actions:**
      * この基本的な例では、"Add to Triggered Alerts"を選択します。実際のシナリオでは、メール通知、Slack連携、またはその他のアクションを設定します。
   * **Save:** アラートを保存します。

![show-entry](../images/save_as_alert.png?classes=inline)

**説明:** このアラートは15分ごとに検索を実行し、検索結果が100件を超えるとトリガーされます。"Add to Triggered Alerts"アクションは、単にSplunkのTriggered Alertsリストにアラートを追加します。

**時間範囲と頻度:** Splunk coreではすべてが検索であるため、検索の時間範囲と頻度を考慮する必要があります。a）時間範囲の重複により同じデータを複数回検索すること、b）時間範囲と頻度のギャップによりイベントを見逃すこと、c）実行頻度が高すぎてオーバーヘッドが発生すること、d）実行頻度が低すぎてアラートに遅延が生じること、を避ける必要があります。

## 2. Splunk Observability Cloudアラート（Detector）

**Detectorの作成:**

* 左側のメニューで"Detectors & SLOs"をクリックします
* "Create Detector -> Custom Detector"をクリックします
* Detectorにわかりやすい名前を付けます（例: "High CPU Utilization Alert - INITIALS"）。
* **Signal:**
  * モニタリングするメトリクスを選択します（"cpu.utilization"）。
  * ホストを指定するために必要なフィルターを追加します（`service.name:otelshop-loadgenerator`）。
  * "Proceed to Alert Condition"をクリックします
* **Condition:**
  * Static Thresholdを選択します
  * しきい値を設定します: "is above" "90"
* **Notifications:**
  * この例では、シンプルな通知方法を選択します（例: テストWebhook）。実際のシナリオでは、PagerDuty、Slack、またはその他の通知システムとの連携を設定します。
* **Save:** Detectorを保存します。

![show-entry](../images/detector_preview.png?classes=inline)

**説明:** このDetectorは、指定されたサービスのCPU使用率メトリクスをモニタリングします。CPU使用率が設定された"for"期間にわたって90%を超えると、Detectorがアラートをトリガーし、通知を送信します。

**すべてのプラットフォームに関する重要な考慮事項:**

* **しきい値:** アラートに設定するしきい値を慎重に検討してください。しきい値が敏感すぎるとアラート疲れにつながり、しきい値が高すぎると重大な問題を見逃す可能性があります。
* **通知チャネル:** アラートが適切なタイミングで適切な人に配信されるように、アラートシステムを適切な通知チャネル（メール、SMS、Slack、PagerDuty）と連携させてください。
* **アラートのグループ化と相関:** 複雑なシステムでは、ノイズを削減し実用的なインサイトに集中するために、アラートのグループ化と相関を実装してください。ITSIはこの点で重要な役割を果たします。
* **ドキュメント:** アラートをトリガーする条件と適切な対応手順を含め、アラートを明確に文書化してください。

これらの例は、基本的なアラートを作成するための出発点を提供します。これらのプラットフォームに慣れてきたら、特定のモニタリングニーズに合わせて、より高度なアラート機能と設定を検討できます。
