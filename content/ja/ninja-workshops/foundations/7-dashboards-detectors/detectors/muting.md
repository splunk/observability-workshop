---
title: Muting Rules の使用
linkTitle: 2.1 Muting Rule の作成
weight: 2.1
---

* Muting Rules を設定する方法を学びます
* 通知を再開する方法を学びます
  
---

## 1. Muting Rules の設定

特定の通知をミュートしたい場合があります。例えば、サーバーやサーバー群のメンテナンスのためのダウンタイムをスケジュールしたい場合や、新しいコードや設定をテストしている場合などです。そのような場合には、Splunk Observability Cloud の muting rules を使用できます。さっそく作成してみましょう。

サイドバーの **Alerts & Detectors** をクリックし、**Detectors** をクリックしてアクティブな detector の一覧を表示します。

![detectors list](../../images/detectors.png)

**Creating a Detector** で detector を作成済みであれば、その detector の右端にある三点リーダー **`...`** をクリックします。作成していない場合は、別の detector で同じ操作を行ってください。

ドロップダウンから **Create Muting Rule...** をクリックします。

![Create Muting Rule](../../images/create-muting-rule.png)

**Muting Rule** ウィンドウで **Mute Indefinitely** にチェックを入れ、理由を入力します。

{{% notice title="重要" style="info" %}}
これにより、ここに戻ってチェックを外すか、この detector の通知を再開するまで、通知は永続的にミュートされます。
{{% /notice %}}

![Mute Indefinitely](../../images/mute-indefinitely.png)

**Next** をクリックし、新しいモーダルウィンドウで muting rule の設定を確認します。

![Confirm Rule](../../images/confirm-rule.png)

{{% button style="blue" %}}Mute Indefinitely{{% /button %}} をクリックして確定します。

![List muted rule](../../images/alert-muted.png)

通知を再開するまで、この detector からメール通知は届きません。次に、その方法を見ていきましょう。

---

## 2. 通知の再開

通知を再開するには、**Muting Rules** をクリックします。**Detector** という見出しの下に、通知をミュートした detector の名前が表示されます。

右端の三点リーダー **`...`** をクリックし、**Resume Notifications** をクリックします。

![Resume](../../images/muting-list.png)

{{% button style="blue" %}}Resume{{% /button %}} をクリックして確定し、この detector の通知を再開します。

![Resume](../../images/resume.png)

**おめでとうございます！** アラート通知を再開できました。
