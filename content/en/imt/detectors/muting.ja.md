# ミューティングルールを設定する - ラボ概要

* ミューティングルールを設定する
* 通知を再開する
  
---

## 1. ミューティングルールの設定

特定の通知をミュートする必要がある場合があります。例えば、サーバーやサーバー群のメンテナンスのためにダウンタイムを設定したい場合や、新しいコードや設定をテストしている場合などがあります。このような場合には、Splunk Observability Cloud でミューティングルールを使用できます。それでは作成してみましょう。

左上のハンバーガーメニューアイコンから、メニューの **Alerts** をクリックし、**Detectors** を選択します。

![Detectors](/images/detectors/detectors-menu.png)

アクティブなディテクターのリストが表示されます。

![Detectors](/images/detectors/detector-list.png)

**Creating a Detector** でディテクターを作成した場合は、右端の3つの点 **`...`** をクリックすると、そのディテクターが表示されます。

ドロップダウンから **Create Muting Rule...** をクリックします。

![Create Muting Rule](/images/detectors/create-muting-rule.png)

**Muting Rule** ウィンドウで、 **Mute Indefinitely** をチェックし、理由を入力します。

!!! important
    これにより、ここに戻ってきてこのボックスのチェックを外すか、このディテクターの通知を再開するまで、通知が永久的にミュートされます。

![Mute Indefinitely](/images/detectors/mute-indefinitely.png){: .shadow .center}

**Next** をクリックして、新しいモーダルウィンドウでミュートルールの設定を確認します。

![Confirm Rule](/images/detectors/confirm-rule.png){: .shadow .center}

**Mute Indefinitely**{: .label-button .sfx-ui-button-blue} をクリックして、設定を確定させます。

![List muted rule](/images/detectors/alert-muted.png)

再び通知を再開するまで、ディテクターからのEメール通知は受け取れません。では、再開する方法を見てみましょう。

---

## 2. 通知を再開する

通知を再開するには、 **Muting Rules** をクリックして、**Detector** の見出しの下に、通知をミュートしたディテクターの名前が表示されます。

![Resume](/images/detectors/muting-rules-menu.png)

右端にあるドット **`...`** をクリックします。

**Resume Notifications**をクリックします。

![Resume](/images/detectors/muting-list.png)

**Resume**{: .label-button .sfx-ui-button-blue} をクリックして、このディテクターの通知を確認し、再開します。

![Resume](/images/detectors/resume.png){: .shadow .center}

**おめでとうございます！** これでアラート通知が再開されました。
