---
title: 基本的なアラートの作成
linkTitle: 2. 基本的なアラートの作成
weight: 1
---

# Splunk Enterprise、AppDynamics、Splunk Observability Cloud での基本的なアラートの設定

このセクションでは、Splunk Enterprise、AppDynamics、Splunk Observability Cloud での基本的なアラートの作成について説明します。これらの例はシンプルさとコアコンセプトのデモンストレーションに重点を置いています。実際のアラートシナリオでは、より複雑な設定としきい値が必要になることが多い点に留意してください。

## 1. Splunk Enterprise アラート

Splunk アラートは、特定の条件に一致するサーチ結果によってトリガーされます。特定の条件が満たされたときに通知するリアルタイムアラートを作成します。

**シナリオ:** 過去5分間に "main" インデックスの "Invalid user" イベント数が100を超えた場合にアラートを発行します。

**手順:**

1. **サーチの作成:** アラートを発行したいイベントを特定する Splunk サーチを作成することから始めます。例

   ```splunk
   index=main "Invalid user"
   ```

    タイムピッカーを使用して "Last 15 minutes" を選択します。

2. **アラートの設定:**
   * "Save As" をクリックし、"Alert" を選択します。
   * アラートにわかりやすい名前を付けます（例："Numerous Invalid User Logins Attempted"）。
   * **Alert type:**
      * **Scheduled:** "Scheduled" を選択して、設定したスケジュールでサーチを評価します。Scheduled の下にある頻度選択ボタンから "Run on Cron Schedule" を選択します。
      * **Cron Expression:** */15* ** *
      * **Triggered when:** "Number of results" "is greater than" "100" を選択します。
      * **Time Range:** "15 minutes" に設定します。
   * **Trigger Actions:**
      * この基本的な例では、"Add to Triggered Alerts" を選択します。実際のシナリオでは、メール通知、Slack 連携、またはその他のアクションを設定します。
   * **Save:** アラートを保存します。

![show-entry](../images/save_as_alert.png?classes=inline)

**説明:** このアラートは15分ごとにサーチを実行し、サーチ結果が100件を超えた場合にトリガーされます。"Add to Triggered Alerts" アクションは、単にアラートを Splunk Triggered Alerts リストに追加します。

**時間範囲と頻度:** Splunk コアではすべてがサーチであるため、以下の点を考慮してサーチの時間範囲と頻度を検討する必要があります。a) 時間範囲の重複により同じデータを複数回検索していないか、b) 時間範囲と頻度のギャップによりイベントを見逃していないか、c) 実行頻度が高すぎてオーバーヘッドが発生していないか、d) 実行頻度が低すぎてアラートに遅延が生じていないか。

## 2. Splunk Observability Cloud アラート（Detectors）

**Detector の作成:**

* 左側メニューの "Detectors & SLOs" をクリックします
* "Create Detector -> Custom Detector" をクリックします
* Detector にわかりやすい名前を付けます（例："High CPU Utilization Alert - INITIALS"）。
* **Signal:**
  * 監視したいメトリクスを選択します（"cpu.utilization"）。
  * ホストを指定するために必要なフィルターを追加します（`service.name:otelshop-loadgenerator`）。
  * "Proceed to Alert Condition" をクリックします
* **Condition:**
  * Static Threshold を選択します
  * しきい値を設定します："is above" "90"
* **Notifications:**
  * この例では、シンプルな通知方法を選択します（例：テスト用 webhook）。実際のシナリオでは、PagerDuty、Slack、またはその他の通知システムとの連携を設定します。
* **Save:** Detector を保存します。

![show-entry](../images/detector_preview.png?classes=inline)

**説明:** この Detector は、指定されたサービスの CPU 使用率メトリクスを監視します。CPU 使用率が設定された "for" 期間中に90%を超えた場合、Detector はアラートをトリガーし、通知を送信します。

**すべてのプラットフォームに関する重要な考慮事項:**

* **しきい値:** アラートに設定するしきい値を慎重に検討してください。しきい値が敏感すぎるとアラート疲れにつながり、しきい値が高すぎると重大な問題を見逃す可能性があります。
* **通知チャネル:** アラートが適切なタイミングで適切な担当者に配信されるように、アラートシステムを適切な通知チャネル（メール、SMS、Slack、PagerDuty）と統合してください。
* **アラートのグループ化と相関:** 複雑なシステムでは、ノイズを削減しアクション可能なインサイトに集中するために、アラートのグループ化と相関を実装してください。ITSI はこの点で重要な役割を果たします。
* **ドキュメント:** アラートをトリガーする条件と適切な対応手順を含め、アラートを明確にドキュメント化してください。

これらの例は、基本的なアラートを作成するための出発点を提供します。これらのプラットフォームに慣れてきたら、特定の監視ニーズに合わせて、より高度なアラート機能と設定を探索できます。
