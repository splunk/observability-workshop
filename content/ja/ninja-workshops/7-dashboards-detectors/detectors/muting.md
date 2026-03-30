---
title: ミュートルールの操作
linkTitle: 2.1 Creating a Muting Rule
weight: 2.1
---

* ミュートルールの設定方法を学ぶ
* 通知の再開方法を学ぶ

---

## 1. ミュートルールの設定

特定の通知をミュートしたい場合があります。たとえば、サーバーまたはサーバーセットのメンテナンスのためにダウンタイムをスケジュールする場合や、新しいコードや設定をテストする場合などです。そのために、Splunk Observability Cloudでミュートルールを使用できます。作成してみましょう！

サイドバーの **Alerts & Detectors** をクリックし、**Detectors** をクリックしてアクティブなDetectorのリストを表示します。

![detectors list](../../images/detectors.png)

**Creating a Detector** でDetectorを作成した場合は、そのDetectorの右端にあるthree dots **`...`** をクリックできます。作成していない場合は、別のDetectorで同様に行ってください。

ドロップダウンから **Create Muting Rule...** をクリックします。

![Create Muting Rule](../../images/create-muting-rule.png)

**Muting Rule** ウィンドウで **Mute Indefinitely** にチェックを入れ、理由を入力します。

{{% notice title="Important" style="info" %}}
これにより、ここに戻ってこのチェックボックスをオフにするか、このDetectorの通知を再開するまで、通知は永続的にミュートされます。
{{% /notice %}}

![Mute Indefinitely](../../images/mute-indefinitely.png)

**Next** をクリックし、新しいモーダルウィンドウでミュートルールの設定を確認します。

![Confirm Rule](../../images/confirm-rule.png)

{{% button style="blue" %}}Mute Indefinitely{{% /button %}} をクリックして確認します。

![List muted rule](../../images/alert-muted.png)

通知を再開するまで、Detectorからのメール通知は届きません。それでは、その方法を見てみましょう！

---

## 2. 通知の再開

通知を再開するには、**Muting Rules** をクリックすると、**Detector** の見出しの下に通知をミュートしたDetectorの名前が表示されます。

右端のthree dots **`...`** をクリックし、**Resume Notifications** をクリックします。

![Resume](../../images/muting-list.png)

{{% button style="blue" %}}Resume{{% /button %}} をクリックして、このDetectorの通知を確認して再開します。

![Resume](../../images/resume.png)

**おめでとうございます**！アラート通知を再開しました！
