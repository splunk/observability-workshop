---
title: 基本的なアラートの作成
linkTitle: 2. 基本的なアラートの作成
weight: 1
---

# Splunk Enterprise、AppDynamics、Splunk Observability Cloud での基本的なアラートのセットアップ

このセクションでは、Splunk Enterprise、AppDynamics、および Splunk Observability Cloud における基本的なアラートの作成について説明します。これらの例はシンプルさを重視し、コアとなる概念を示すことに焦点を当てています。実際のアラートシナリオでは、より複雑な構成としきい値が必要になることが多い点にご留意ください。

## 1. Splunk Enterprise アラート

Splunk のアラートは、特定の条件に一致する検索結果によってトリガーされます。ここでは、特定の条件が満たされたときに通知するリアルタイムアラートを作成します。

**シナリオ:**  "main" インデックス内の "Invalid user" イベント数が直近 5 分間で 100 を超えた場合にアラートを発します。

**手順:**

1. **検索の作成:** まず、アラート対象とするイベントを特定する Splunk 検索を作成します。例:

   ```splunk
   index=main "Invalid user"
   ```

    タイムピッカーで "Last 15 minutes" を選択します。

2. **アラートの構成:**
   * "Save As" をクリックし、"Alert" を選択します。
   * アラートにわかりやすい名前を付けます（例: "Numerous Invalid User Logins Attempted"）。
   * **Alert type:**
      * **Scheduled:** "Scheduled" を選択して、設定したスケジュールに従って検索を評価します。Scheduled の下に頻度を選択するボタンがあるので、"Run on Cron Schedule" を選択します。
      * **Cron Expression:** */15* ** *
      * **Triggered when:** "Number of results" "is greater than" "100" を選択します。
      * **Time Range:** "15 minutes" に設定します。
   * **Trigger Actions:**
      * この基本的な例では、"Add to Triggered Alerts" を選択します。実際のシナリオでは、メール通知、Slack 連携、その他のアクションを構成します。
   * **Save:** アラートを保存します。

![show-entry](../images/save_as_alert.png?classes=inline)

**説明:** このアラートは 15 分ごとに検索を実行し、検索結果が 100 件を超えるとトリガーされます。"Add to Triggered Alerts" アクションは、単にアラートを Splunk の Triggered Alerts リストに追加します。

**時間範囲と頻度:** Splunk core ではすべてが検索であるため、検索の時間範囲と頻度を考慮する必要があります。それは、a) 同じデータを重複した時間範囲で複数回検索しないため、b) 時間範囲と頻度のギャップによってイベントを取りこぼさないため、c) 過度に頻繁に実行してオーバーヘッドを増やさないため、d) 実行頻度が低すぎてアラートに遅延が発生しないようにするためです。

## 2. Splunk Observability Cloud アラート（Detectors）

**Detector の作成:**

* 左側のメニューで "Detectors & SLOs" をクリックします
* "Create Detector -> Custom Detector" をクリックします
* Detector にわかりやすい名前を付けます（例: "High CPU Utilization Alert - INITIALS"）。
* **Signal:**
  * 監視するメトリクス（"cpu.utilization"）を選択します。
  * ホストを指定するために必要なフィルターを追加します（`service.name:otelshop-loadgenerator`）。
  * "Proceed to Alert Condition" をクリックします
* **Condition:**
  * Static Threshold を選択します
  * しきい値を設定します: "is above" "90"
* **Notifications:**
  * この例では、シンプルな通知方法（例: テスト用 webhook）を選択します。実際のシナリオでは、PagerDuty、Slack、その他の通知システムとの連携を構成します。
* **Save:** Detector を保存します。

![show-entry](../images/detector_preview.png?classes=inline)

**説明:** この Detector は、指定されたサービスの CPU 使用率メトリクスを監視します。CPU 使用率が構成された "for" の継続時間にわたって 90% を超えると、Detector がアラートをトリガーし、通知を送信します。

**すべてのプラットフォームで重要な検討事項:**

* **しきい値:** アラートに設定するしきい値は慎重に検討してください。しきい値が敏感すぎるとアラート疲れを招きますが、高すぎると重要な問題を見逃す可能性があります。
* **通知チャネル:**  アラートシステムを適切な通知チャネル（メール、SMS、Slack、PagerDuty）と統合し、適切なタイミングで適切な担当者にアラートが届くようにします。
* **アラートのグループ化と相関:**  複雑なシステムでは、ノイズを減らして実行可能なインサイトに集中するために、アラートのグループ化と相関を実装します。ITSI はこの点で重要な役割を果たします。
* **ドキュメント:** トリガーする条件や適切な対応手順を含め、アラートを明確にドキュメント化してください。

これらの例は、基本的なアラートを作成するための出発点となります。各プラットフォームに慣れてきたら、特定の監視ニーズに合わせて、より高度なアラート機能や構成を探求してみてください。
