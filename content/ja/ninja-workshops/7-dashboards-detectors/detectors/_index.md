---
title: Detector の操作
linkTitle: 2. Detectors
weight: 2.0
time: 10 minutes
hidden: true
---

* チャートからDetectorを作成する
* アラート条件の設定
* プリフライトチェックの実行
* ミュートルールの操作

---

## 1. はじめに

Splunk Observability Cloudは、特定の条件が満たされたときに通知するために、Detector、イベント、アラート、および通知を使用します。たとえば、CPU使用率が95% に達したとき、または同時ユーザー数が追加のAWSインスタンスを起動する必要があるかもしれない制限に近づいているときに、SlackチャンネルまたはOpsチームのメールアドレスにメッセージを送信したい場合があります。

これらの条件は、ルール内の条件が満たされたときにアラートをトリガーする1つ以上のルールとして表現されます。Detector内の個々のルールは、重要度に応じてラベル付けされます：Info、Warning、Minor、Major、およびCritical。

## 2. Detector の作成

**Dashboards** で、（前のモジュールで作成した）**Custom Dashboard Group** をクリックし、ダッシュボード名をクリックします。

![Custom Dashboard Group](../images/custom-dashboard-group.png)

このダッシュボードのチャートから新しいDetectorを作成します。**Latency vs Load** チャートのベルアイコンをクリックし、次に **New Detector From Chart** をクリックします。

![New Detector](../images/new-detector.png)

**Detector Name** の横にあるテキストフィールドで、提案されたDetector名の前に **イニシャルを追加** してください。

{{% notice title="Naming the detector" style="info" %}}
提案されたDetector名の前にイニシャルを追加することが重要です。

次のようになるはずです：**XYZ's Latency Chart Detector**。
{{% /notice %}}

{{% button style="blue" %}}Create Alert Rule{{% /button %}} をクリックします。

![Create Alert Rule](../images/create-alert-rule.png)

Detectorウィンドウの **Alert signal** 内で、アラートを発するシグナルは **Alert on** 列に（青い）ベルでマークされています。ベルは、アラートの生成に使用されているシグナルを示しています。

{{% button style="blue" %}}Proceed to Alert Condition{{% /button %}} をクリックします。

![Alert Signal](../images/alert-signal.png)

## 3. アラート条件の設定

**Alert condition** で、**Static Threshold** をクリックし、次に {{% button style="blue" %}}Proceed to Alert Settings{{% /button %}} をクリックします。

![Alert Condition](../images/alert-condition.png)

**Alert Settings** で、**Threshold** フィールドに値 **`290`** を入力します。同じウィンドウで、右上の **Time** を過去1日（**-1d**）に変更します。

---

## 4. アラートのプリフライトチェック

5秒後にプリフライトチェックが実行されます。**Estimated alert count** を確認してください。現在のアラート設定に基づくと、1日で受信したはずのアラート数は **3** です。

![Alert Threshold](../images/alert-threshold.png)

{{% notice title="About pre-flight checks" style="info" %}}
アラート条件を設定すると、UIは現在の設定と、右上隅に設定された時間枠（この場合は過去1日）に基づいて、受信する可能性のあるアラート数を推定します。

すぐに、プラットフォームは現在の設定でシグナルの分析を開始し、プリフライトチェックと呼ばれるものを実行します。これにより、プラットフォーム内の履歴データを使用してアラート条件をテストでき、設定が論理的であり、意図せずアラートストームを生成しないことを確認できます。これは、Splunk Observability Cloudでのみ利用可能な、シンプルでありながら非常に強力な方法でアラートの設定から当て推量を取り除きます。

Detectorのプレビューについて詳しくは、このリンクを参照してください
[Preview detector alerts.](https://docs.splunk.com/Observability/alerts-detectors-notifications/preview-detector-alerts.html#nav-Preview-detector-alerts)
{{% /notice %}}

{{% button style="blue" %}}Proceed to Alert Message{{% /button %}} をクリックします。

---

## 5. アラートメッセージ

**Alert message** で、**Severity** の下で **Major** を選択します。

![Alert Message](../images/alert-message.png)

{{% button style="blue" %}}Proceed to Alert Recipients{{% /button %}} をクリックします。

**Add Recipient** をクリックし、最初のオプションとして表示されているメールアドレスをクリックします。

![Add Recipient](../images/add-recipient.png)

{{% notice title="Notification Services" style="info" %}}
これは、そのメールアドレスを入力するのと同じです。または、**E-mail...** をクリックして別のメールアドレスを入力することもできます。

これは、プラットフォームで利用可能な多くの **Notification Services** の一例にすぎません。トップメニューの **Integrations** タブに移動し、**Notification Services** を確認することで、これを確認できます。
{{% /notice %}}

---

## 6. アラートの有効化

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}} をクリックします。

**Activate...** で {{% button style="blue" %}}Activate Alert Rule{{% /button %}} をクリックします。

![Activate Alert](../images/activate-alert.png)

アラートをより早く受け取りたい場合は、ルールを編集して値を **`290`** から **`280`** などに下げることができます。

**Time** を **-1h** に変更すると、過去1時間のメトリクスに基づいて、選択したしきい値でいくつのアラートを受け取る可能性があるかを確認できます。

ナビゲーションバーの ![alerts and detectors button](../images/alerts-and-detectors.png?classes=inline&height=25px) をクリックし、次に **Detectors** をクリックします。オプションでイニシャルでフィルターできます。ここにDetectorがリストされているはずです。表示されない場合は、ブラウザを更新してください。

![Detector List](../images/detectors.png)

**おめでとうございます**！最初のDetectorを作成し、有効化しました！
