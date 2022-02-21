# ディテクターを使ってみよう - ラボ概要

* チャートからディテクターを作成する
* アラート条件を設定する
* プレフライトチェックを実行する
* ミューティングルールを設定する

---

## 1. はじめに

Splunk Observability Cloud では、ディテクター、イベント、アラート、通知を使用して、特定の条件が満たされたときに情報を提供します。たとえば、CPU使用率が95%に達したときや、同時ユーザー数が制限値に近づいてAWSインスタンスを追加で立ち上げなければならない可能性があるときに、Slack チャンネルや Ops チームのメールアドレスにメッセージを送信したいと考えるでしょう。

これらの条件は1つまたは複数のルールとして表現され、ルール内の条件が満たされたときにアラートが発生します。ディテクターに含まれる個々のルールは、重要度に応じてラベル付けされています。Info、Warning、Minor、Major、Criticalとなっています。

## 2. ディテクターの作成

**Dashboards** で、前のモジュールで作成した **カスタムダッシュボードグループ** をクリックし、ダッシュボードの名前をクリックします。

![Custom Dashboard Group](../images/detectors/custom-dashboard-group.png)
このチャートから、新しいディテクターを作成していきます。

チャートが表示されたら、チャート上のベルのアイコンをクリックし、 **New Detector From Chart** をクリックします。

![New Detector](../images/detectors/new-detector.png)

**Detector Name** の横にあるテキストフィールドで、提案されたディテクター名の最初に、**あなたののイニシャル** を追加してください。

!!! important "ディテクターの名前を決める"
    提案されたディテクター名の前に自分のイニシャルを追加することが重要です。
    それは次のようなものでなければなりません: **XYZ's Latency Chart Detector**

**Create Alert Rule**{: .label-button .sfx-ui-button-blue} をクリックします。

![Create Alert Rule](../images/detectors/create-alert-rule.png)

Detector ウィンドウの **Alert signal** の中で、アラートするシグナルは **Alert on** 欄に青のベルが表示されています。このベルは、どの信号がアラートの生成に使用されているかを示しています。

**Proceed to Alert Condition**{: .label-button .sfx-ui-button-blue} をクリックします。

![Alert Signal](../images/detectors/alert-signal.png)

---

## 3. アラート条件の設定

**Alert condition** で、**Static Threshold** をクリックし、**Proceed to Alert Settings**{: .label-button .sfx-ui-button-blue} をクリックしてください。

![Alert Condition](../images/detectors/alert-condition.png)

**Alert Settings** で、 **Threshold** フィールドに値 **`290`** を入力します。同じウィンドウで、右上の **Time** を過去1日（**-1d**）に変更します。

---

## 4. プリフライトチェックの警告

5秒後にプレフライトチェックが開始されます。**Estimated alert count** を参照してください。現在のアラート設定に基づくと、1日に受け取るアラートの量は約 **18** でした。

![Alert Threshold](../images/detectors/alert-threshold.png)

!!! note "プリフライトチェックについて"
    アラート条件を設定すると、UIは現在の設定に基づいて、右上に設定された時間枠（ここでは過去1日）の中で、どのくらいのアラートが発生するかを予測します。

    すぐに、プラットフォームは現在の設定でシグナルの分析を開始し、「プリフライトチェック」と呼ばれる作業を行います。これにより、プラットフォーム内の過去のデータを使用してアラート条件をテストし、設定が妥当であり、誤って大量のアラートを発生させないようにすることができます。Splunk Observability Cloud を使用してのみ利用できるシンプルかつ非常に強力な方法で、アラートの設定から推測作業を取り除くことができます。

    ディテクターのプレビューについての詳細は、以下のリンクをご覧ください。
    [Preview detector alerts](https://docs.splunk.com/Observability/alerts-detectors-notifications/preview-detector-alerts.html#nav-Preview-detector-alerts){: target=_blank}

**Proceed to Alert Message**{: .label-button .sfx-ui-button-blue} をクリックし、次に進みます。

---

## 5. アラートメッセージ

**Alert message** の **Severity** で **Major** を選択します。

![Alert Message](../images/detectors/alert-message.png)

**Proceed to Alert Recipients**{: .label-button .sfx-ui-button-blue} をクリックします。

**Add Recipient**（受信者の追加）をクリックし、最初の選択肢として表示されているメールアドレスをクリックします。

![Add Recipient](../images/detectors/add-recipient.png)

!!! note "通知先のサービス"
    これは、そのメールアドレスを入力したときと同じです。または、**E-mail...** をクリックして別のメールアドレスを入力することもできます。

    これは、予め用意されている多くの **通知先サービス**の 一例です。全てを確認するには、トップメニューの **Integrations** タブに移動し、**Notification Services** を参照してください。

---

## 6. アラートの有効化

**Proceed to Alert Activation**{: .label-button .sfx-ui-button-blue} をクリックします。

**Activivate...** で **Activate Alert Rule**{: .label-button .sfx-ui-button-blue} をクリックします。

![Activate Alert](../images/detectors/activate-alert.png)

アラートをより早く取得したい場合は、**Alert Settings** をクリックして、値を **`290`** から **`280`**に 下げてください。

**Time** を **-1h** に変更すると、過去1時間のメトリクスに基づいて、選択した閾値でどれだけのアラートを取得できるかを確認できます。

トップメニューの **Alerts** にカーソルを合わせて、**Detectors** をクリックします。

![Detectors](../images/detectors/detectors-menu.png)

ディテクターのリストが表示されます。表示されない場合は、ブラウザを更新してください。

![Detector List](../images/detectors/detectors.png)

**おめでとうございます**。最初のディテクターが作成され、起動されました。
