---
title: Detector の活用
linkTitle: 2. Detectors
weight: 2.0
time: 10 minutes
hidden: true
---

* チャートから Detector を作成する
* アラート条件を設定する
* プリフライトチェックを実行する
* ミューティングルールを操作する

---

## 1. はじめに

Splunk Observability Cloud では、特定の条件が満たされたときに通知するために、detector、event、alert、notification を使用します。たとえば、CPU 使用率が 95% に達したときや、同時接続ユーザー数が AWS インスタンスの追加が必要になる可能性のある上限に近づいたときに、Ops チームの Slack チャンネルやメールアドレスにメッセージを送信したい場合などです。

これらの条件は、ルール内の条件が満たされたときにアラートをトリガーする 1 つ以上のルールとして表現されます。detector の個々のルールには、重要度に応じて Info、Warning、Minor、Major、Critical のラベルが付けられます。

## 2. Detector の作成

**Dashboards** で、（前のモジュールで作成した）**Custom Dashboard Group** をクリックし、続いてダッシュボード名をクリックします。

![Custom Dashboard Group](../images/custom-dashboard-group.png)

ここからは、このダッシュボード上のチャートから新しい detector を作成します。**Latency vs Load** チャートのベルアイコンをクリックし、**New Detector From Chart** をクリックします。

![New Detector](../images/new-detector.png)

**Detector Name** の横のテキストフィールドで、提案された detector 名の前に **イニシャルを追加** します。

{{% notice title="detector の命名" style="info" %}}
提案された detector 名の先頭にイニシャルを追加することが重要です。

たとえば次のようになります: **XYZ's Latency Chart Detector**。
{{% /notice %}}

{{% button style="blue" %}}Create Alert Rule{{% /button %}} をクリックします。

![Create Alert Rule](../images/create-alert-rule.png)

Detector ウィンドウの **Alert signal** 内で、アラート対象となる Signal は **Alert on** 列の（青い）ベルでマークされています。このベルは、アラートの生成に使用されている Signal を示します。

{{% button style="blue" %}}Proceed to Alert Condition{{% /button %}} をクリックします。

![Alert Signal](../images/alert-signal.png)

## 3. アラート条件の設定

**Alert condition** で **Static Threshold** をクリックし、続いて {{% button style="blue" %}}Proceed to Alert Settings{{% /button %}} をクリックします。

![Alert Condition](../images/alert-condition.png)

**Alert Settings** の **Threshold** フィールドに値 **`290`** を入力します。同じウィンドウで、右上の **Time** を past day (**-1d**) に変更します。

---

## 4. アラートのプリフライトチェック

5 秒後にプリフライトチェックが実行されます。**Estimated alert count** を確認してください。現在のアラート設定に基づくと、1 日に受け取るアラートの数は **3** 件となります。

![Alert Threshold](../images/alert-threshold.png)

{{% notice title="プリフライトチェックについて" style="info" %}}
アラート条件を設定すると、UI は現在の設定および右上隅で設定された期間（このケースでは過去 1 日間）に基づいて、受け取る可能性のあるアラート数を推定します。

すぐにプラットフォームは現在の設定で signal の分析を開始し、Pre-flight Check と呼ばれる処理を実行します。これにより、プラットフォーム内の過去データを使用してアラート条件をテストできるため、設定が論理的であり、誤ってアラートストームを引き起こさないことを確認できます。Splunk Observability Cloud でのみ利用可能な、シンプルかつ非常に強力な方法でアラート設定の試行錯誤を排除します。

detector のプレビューについて詳しくは、こちらのリンクをご覧ください
[Preview detector alerts.](https://docs.splunk.com/Observability/alerts-detectors-notifications/preview-detector-alerts.html#nav-Preview-detector-alerts)
{{% /notice %}}

{{% button style="blue" %}}Proceed to Alert Message{{% /button %}} をクリックします。

---

## 5. アラートメッセージ

**Alert message** の **Severity** で **Major** を選択します。

![Alert Message](../images/alert-message.png)

{{% button style="blue" %}}Proceed to Alert Recipients{{% /button %}} をクリックします。

**Add Recipient** をクリックし、最初のオプションとして表示されているご自身のメールアドレスをクリックします。

![Add Recipient](../images/add-recipient.png)

{{% notice title="Notification Services" style="info" %}}
これは、そのメールアドレスを入力するのと同じです。または、**E-mail...** をクリックして別のメールアドレスを入力することもできます。

これは、プラットフォームで利用可能な多くの **Notification Services** の一例にすぎません。トップメニューの **Integrations** タブから **Notification Services** を確認できます。
{{% /notice %}}

---

## 6. アラートの有効化

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}} をクリックします。

**Activate...** で {{% button style="blue" %}}Activate Alert Rule{{% /button %}} をクリックします。

![Activate Alert](../images/activate-alert.png)

より早くアラートを受け取りたい場合は、ルールを編集して値を **`290`** から **`280`** などに下げてください。

**Time** を **-1h** に変更すると、過去 1 時間のメトリクスに基づき、選択したしきい値で受け取る可能性のあるアラート数を確認できます。

ナビゲーションバーの ![alerts and detectors button](../images/alerts-and-detectors.png?classes=inline&height=25px) をクリックし、続いて **Detectors** をクリックします。必要に応じてご自身のイニシャルでフィルタリングできます。ここに作成した detector が一覧表示されます。表示されない場合は、ブラウザを更新してください。

![Detector List](../images/detectors.png)

**おめでとうございます**! 最初の detector を作成し、有効化しました!
