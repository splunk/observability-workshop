---
title: Muting Ruleの使い方
linkTitle: 2.1 Muting Ruleの作成
weight: 2.1
---

* Muting Ruleの設定方法を学びます
* 通知の再開方法を学びます
  
---

## 1. Muting Ruleの設定

サーバーのメンテナンスのためにダウンタイムをスケジュールしたい場合や、新しいコードや設定をテストしている場合など、特定の通知をミュートしたいことがあります。そのような場合、Splunk Observability CloudのMuting Ruleを使用できます。実際に作成してみましょう。

サイドバーの **Alerts & Detectors** をクリックし、次に **Detectors** をクリックしてアクティブなDetectorの一覧を表示します。

![detectors list](../../images/detectors.png)

**Creating a Detector** でDetectorを作成した場合は、そのDetectorの右端にある三点リーダー **`...`** をクリックします。作成していない場合は、別のDetectorで同様に操作します。

ドロップダウンから **Create Muting Rule...** をクリックします。

![Create Muting Rule](../../images/create-muting-rule.png)

**Muting Rule** ウィンドウで **Mute Indefinitely** にチェックを入れ、理由を入力します。

{{% notice title="Important" style="info" %}}
これにより、このチェックボックスを解除するか、このDetectorの通知を再開するまで、通知が永続的にミュートされます。
{{% /notice %}}

![Mute Indefinitely](../../images/mute-indefinitely.png)

**Next** をクリックし、新しいモーダルウィンドウでMuting Ruleの設定を確認します。

![Confirm Rule](../../images/confirm-rule.png)

{{% button style="blue" %}}Mute Indefinitely{{% /button %}} をクリックして確認します。

![List muted rule](../../images/alert-muted.png)

通知を再開するまで、Detectorからのメール通知は届きません。次に、通知を再開する方法を見てみましょう。

---

## 2. 通知の再開

通知を再開するには、 **Muting Rules** をクリックします。 **Detector** 見出しの下に、通知をミュートしたDetectorの名前が表示されます。

右端にある三点リーダー **`...`** をクリックし、 **Resume Notifications** をクリックします。

![Resume](../../images/muting-list.png)

{{% button style="blue" %}}Resume{{% /button %}} をクリックして確認し、このDetectorの通知を再開します。

![Resume](../../images/resume.png)

**おめでとうございます！** アラート通知が再開されました。
