---
title: Detectorの操作
linkTitle: 2. Detectors
weight: 2.0
time: 10 minutes
hidden: true
---

* チャートからDetectorを作成する
* アラート条件の設定
* プリフライトチェックの実行
* ミューティングルールの操作

---

## 1. はじめに

Splunk Observability Cloudは、Detector、イベント、アラート、通知を使用して、特定の条件が満たされたときに通知します。たとえば、CPU使用率が95%に達したときにSlackチャンネルやOpsチームのメールアドレスにメッセージを送信したい場合や、同時接続ユーザー数が追加のAWSインスタンスを起動する必要があるかもしれない上限に近づいている場合に通知を受け取ることができます。

これらの条件は、ルール内の条件が満たされたときにアラートをトリガーする1つ以上のルールとして表現されます。Detector内の個々のルールは、重要度に応じてラベル付けされます: Info、Warning、Minor、Major、Critical。

## 2. Detectorの作成

**Dashboards** で **Custom Dashboard Group**（前のモジュールで作成したもの）をクリックし、ダッシュボード名をクリックします。

![Custom Dashboard Group](../images/custom-dashboard-group.png)

次に、このダッシュボードのチャートから新しいDetectorを作成します。**Latency vs Load** チャートのベルアイコンをクリックし、**New Detector From Chart** をクリックします。

![New Detector](../images/new-detector.png)

**Detector Name** の横のテキストフィールドに、提案されたDetector名の前に **イニシャルを追加** します。

{{% notice title="Detectorの命名" style="info" %}}
提案されたDetector名の前にイニシャルを追加することが重要です。

次のようになります: **XYZ's Latency Chart Detector**
{{% /notice %}}

{{% button style="blue" %}}Create Alert Rule{{% /button %}} をクリックします。

![Create Alert Rule](../images/create-alert-rule.png)

Detectorウィンドウ内の **Alert signal** で、アラート対象のSignalは **Alert on** 列の（青い）ベルでマークされています。ベルは、アラートの生成に使用されるSignalを示しています。

{{% button style="blue" %}}Proceed to Alert Condition{{% /button %}} をクリックします。

![Alert Signal](../images/alert-signal.png)

## 3. アラート条件の設定

**Alert condition** で **Static Threshold** をクリックし、{{% button style="blue" %}}Proceed to Alert Settings{{% /button %}} をクリックします。

![Alert Condition](../images/alert-condition.png)

**Alert Settings** で、**Threshold** フィールドに値 **`290`** を入力します。同じウィンドウで右上の **Time** を過去1日（**-1d**）に変更します。

---

## 4. アラートのプリフライトチェック

5秒後にプリフライトチェックが実行されます。**Estimated alert count** を確認します。現在のアラート設定に基づくと、1日間に受信したであろうアラートの数は **3** 件です。

![Alert Threshold](../images/alert-threshold.png)

{{% notice title="プリフライトチェックについて" style="info" %}}
アラート条件を設定すると、UIは現在の設定と右上に設定された時間枠（この場合は過去1日）に基づいて、受信する可能性のあるアラート数を推定します。

すぐにプラットフォームは現在の設定でシグナルの分析を開始し、プリフライトチェックと呼ばれる処理を実行します。これにより、プラットフォーム内の履歴データを使用してアラート条件をテストでき、設定が論理的であり、意図せずアラートストームを発生させないことを確認できます。アラート設定から推測を排除するシンプルかつ非常に強力な方法で、Splunk Observability Cloudでのみ利用可能です。

Detectorプレビューの詳細については、次のリンクを参照してください
[Preview detector alerts](https://docs.splunk.com/Observability/alerts-detectors-notifications/preview-detector-alerts.html#nav-Preview-detector-alerts)
{{% /notice %}}

{{% button style="blue" %}}Proceed to Alert Message{{% /button %}} をクリックします。

---

## 5. アラートメッセージ

**Alert message** の **Severity** で **Major** を選択します。

![Alert Message](../images/alert-message.png)

{{% button style="blue" %}}Proceed to Alert Recipients{{% /button %}} をクリックします。

**Add Recipient** をクリックし、最初のオプションとして表示されている自分のメールアドレスをクリックします。

![Add Recipient](../images/add-recipient.png)

{{% notice title="Notification Services" style="info" %}}
これはそのメールアドレスを入力するのと同じです。または **E-mail...** をクリックして別のメールアドレスを入力することもできます。

これはプラットフォームで利用可能な多くの **Notification Services** の一例にすぎません。トップメニューの **Integrations** タブに移動し、**Notification Services** を確認してください。
{{% /notice %}}

---

## 6. アラートの有効化

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}} をクリックします。

**Activate...** で {{% button style="blue" %}}Activate Alert Rule{{% /button %}} をクリックします。

![Activate Alert](../images/activate-alert.png)

アラートをより早く受信したい場合は、ルールを編集して値を **`290`** から **`280`** に下げます。

**Time** を **-1h** に変更すると、過去1時間のメトリクスに基づいて、選択したしきい値でどれだけのアラートを受信する可能性があるかを確認できます。

ナビゲーションバーの ![alerts and detectors button](../images/alerts-and-detectors.png?classes=inline&height=25px) をクリックし、**Detectors** をクリックします。オプションでイニシャルでフィルタリングできます。ここにDetectorが一覧表示されます。表示されない場合は、ブラウザを更新してください。

![Detector List](../images/detectors.png)

**おめでとうございます！** 最初のDetectorを作成し、有効化しました！
