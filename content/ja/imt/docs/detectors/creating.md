---
title: ディテクターを利用する
linkTitle: ディテクターの作成
weight: 2
isCJKLanguage: true
---

* チャートからディテクターを作成する
* アラート条件を設定する
* プリフライトチェックを実行する
* ミューティングルールを設定する

---

## 1. はじめに

Splunk Observability Cloud では、ディテクター（検出器）、イベント、アラート、通知を使用して、特定の条件が満たされたときに情報を提供することができます。たとえば、CPU使用率が95%に達したときや、同時ユーザー数が制限値に近づいてAWSインスタンスを追加で立ち上げなければならない可能性があるときに、Slack チャンネルや Ops チームのメールアドレスにメッセージを送信したいと考えるでしょう。

これらの条件は1つまたは複数のルールとして表現され、ルール内の条件が満たされたときにアラートが発生します。ディテクターに含まれる個々のルールは、重要度に応じてラベル付けされています。Info、Warning、Minor、Major、Criticalとなっています。

## 2. ディテクターの作成

**Dashboards** で、前のモジュールで作成した **Custom Dashboard Group** をクリックし、ダッシュボードの名前をクリックします。

![Custom Dashboard Group](../../../images/custom-dashboard-group.png)

このチャートから、新しいディテクターを作成していきます。**Latency vs Load** チャート上のベルのアイコンをクリックし、 **New Detector From Chart** をクリックします。

![New Detector](../../../images/new-detector.png)

**Detector Name** の横にあるテキストフィールドで、提案されたディテクター名の最初に、**あなたのイニシャル** を追加してください。

{{% alert title="ディテクターの名前を決める" color="primary" %}}
提案されたディテクター名の前に自分のイニシャルを追加することをお忘れなく。

次のような名前にしてください: **XYZ's Latency Chart Detector**
{{% /alert %}}

{{% labelbutton color="ui-button-blue" %}}Create Alert Rule{{% /labelbutton %}} をクリックします。

![Create Alert Rule](../../../images/create-alert-rule.png)

Detector ウィンドウの **Alert signal** の中で、アラートするシグナルは **Alert on** 欄に青のベルが表示されています。このベルは、どのシグナルがアラートの生成に使用されているかを示しています。

{{% labelbutton color="ui-button-blue" %}}Proceed to Alert Condition{{% /labelbutton %}} をクリックします。

![Alert Signal](../../../images/alert-signal.png)

---

## 3. アラート条件の設定

**Alert condition** で、**Static Threshold** をクリックし、{{% labelbutton color="ui-button-blue" %}}Proceed to Alert Settings{{% /labelbutton %}} をクリックしてください。

![Alert Condition](../../../images/alert-condition.png)

**Alert Settings** で、 **Threshold** フィールドに値 **`290`** を入力します。同じウィンドウで、右上の **Time** を過去1日（**-1d**）に変更します。

---

## 4. プリフライトチェックの警告

5秒後にプリフライトチェックが行われます。**Estimated alert count** に、アラート回数の目安が表示されます。現在のアラート設定では、1日に受信するアラート量は **3** となります。

![Alert Threshold](../../../images/alert-threshold.png)

{{% alert title="プリフライトチェックについて" color="primary" %}}
アラート条件を設定すると、UIは現在の設定に基づいて、右上に設定された時間枠（ここでは過去1日）の中で、どのくらいのアラートが発生するかを予測します。

すぐに、プラットフォームは現在の設定でシグナルの分析を開始し、「プリフライトチェック」と呼ばれる作業を行います。これにより、プラットフォーム内の過去のデータを使用してアラート条件をテストし、設定が妥当であり、誤って大量のアラートを発生させないようにすることができます。Splunk Observability Cloud を使用してのみ利用できるシンプルかつ非常に強力な方法で、アラートの設定から推測作業を取り除くことができます。

ディテクターのプレビューについての詳細は、こちらのリンクをご覧ください。
[Preview detector alerts](https://docs.splunk.com/Observability/alerts-detectors-notifications/preview-detector-alerts.html#nav-Preview-detector-alerts)
{{% /alert %}}

{{% labelbutton color="ui-button-blue" %}}Proceed to Alert Message{{% /labelbutton %}} をクリックし、次に進みます。

---

## 5. アラートメッセージ

**Alert message** の **Severity** で **Major** を選択します。

![Alert Message](../../../images/alert-message.png)

{{% labelbutton color="ui-button-blue" %}}Proceed to Alert Recipients{{% /labelbutton %}} をクリックします。

**Add Recipient**（受信者の追加）をクリックし、最初の選択肢として表示されているメールアドレスをクリックします。

![Add Recipient](../../../images/add-recipient.png)

{{% alert title="通知サービス" color="primary" %}}
これは、そのメールアドレスを入力したときと同じです。または、**E-mail...** をクリックして別のメールアドレスを入力することもできます。

これは、予め用意されている多くの **Notification Services** の一例です。全てを確認するには、トップメニューの **Integrations** タブに移動し、**Notification Services** を参照してください。
{{% /alert %}}

---

## 6. アラートの有効化

{{% labelbutton color="ui-button-blue" %}}Proceed to Alert Activation{{% /labelbutton %}} をクリックします。

**Activivate...** で {{% labelbutton color="ui-button-blue" %}}Activate Alert Rule{{% /labelbutton %}} をクリックします。

![Activate Alert](../../../images/activate-alert.png)

アラートをより早く取得したい場合は、**Alert Settings** をクリックして、値を **`290`** から **`280`** に下げてみてください。

**Time** を **-1h** に変更すると、過去1時間のメトリクスに基づいて、選択した閾値でどれだけのアラートを取得できるかを確認できます。

ナビバーにある ![alerts and detectors button](../../../images/alerts-and-detectors.png) ボタンをクリックして、その後 **Detectors** をクリックすると、ディテクターの一覧が表示されます。あなたのイニシャルでフィルタして、作成したディテクターを確認しましょう。表示されない場合は、ブラウザをリロードしてみてください。

![Detector List](../../../images/detectors.png)

**おめでとうございます！** 最初のディテクターが作成され、有効化されました。
